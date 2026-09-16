from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config["SECRET_KEY"] = "av-room-development-key"
LATE_FEE_PER_DAY = 25

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///av_room.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    daily_late_fee = db.Column(db.Float, default=LATE_FEE_PER_DAY)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    equipment_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    deposit = db.Column(db.Float, default=0)
    return_date = db.Column(db.Date)
    late_fee = db.Column(db.Float, default=0)
    refund = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="Borrowed")


@app.route("/")
def index():
    equipment = Equipment.query.all()
    bookings = Booking.query.filter_by(status="Borrowed").all()

    overdue = [
        b for b in bookings
        if b.due_date < date.today()
    ]

    return render_template(
        "index.html",
        equipment=equipment,
        bookings=bookings,
        overdue=overdue,
        current_date=date.today()
    )


@app.route("/book/<int:equipment_id>", methods=["GET", "POST"])
def book(equipment_id):

    equipment = Equipment.query.get_or_404(equipment_id)

    if request.method == "POST":

        quantity = int(request.form["quantity"])
        borrow_date = date.fromisoformat(request.form["borrow_date"])
        due_date = date.fromisoformat(request.form["due_date"])
        deposit = float(request.form["deposit"])
        email = request.form["email"].strip().lower()

        if quantity < 1:
            return "Quantity must be at least 1!"

        if borrow_date < date.today():
            return "Borrow date cannot be before the current date!"

        if due_date < borrow_date:
            return "Return date cannot be before the borrow date!"

        if deposit < 0:
            return "Deposit cannot be negative!"

        if not email.endswith("@poornima.edu.in"):
            return "Please use a valid @poornima.edu.in email address!"

        # Reserve stock and create the booking in one transaction. The quantity
        # condition makes concurrent requests compete safely for the remaining units.
        reserved = (
            Equipment.query
            .filter(
                Equipment.id == equipment.id,
                Equipment.available_quantity >= quantity
            )
            .update(
                {Equipment.available_quantity: Equipment.available_quantity - quantity},
                synchronize_session=False
            )
        )

        if reserved != 1:
            db.session.rollback()
            return "Not enough equipment available!"

        booking = Booking(
            student_name=request.form["student_name"],
            email=email,
            equipment_id=equipment.id,
            quantity=quantity,
            borrow_date=borrow_date,
            due_date=due_date,
            deposit=deposit
        )

        db.session.add(booking)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template(
        "book.html",
        equipment=equipment,
        current_date=date.today(),
        late_fee_per_day=LATE_FEE_PER_DAY
    )


@app.route("/returns")
def returns():
    bookings = Booking.query.filter_by(status="Borrowed").all()
    return render_template("returns.html", bookings=bookings, current_date=date.today())


@app.route("/transfer/<int:booking_id>", methods=["POST"])
def transfer_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.status != "Borrowed":
        return "Only active bookings can be transferred!"

    if date.today() >= booking.due_date:
        return "A booking can only be transferred before its due date!"

    new_student_name = request.form.get("student_name", "").strip()
    new_email = request.form.get("email", "").strip().lower()
    due_date_value = request.form.get("due_date", "")

    try:
        new_due_date = date.fromisoformat(due_date_value)
    except ValueError:
        return "A valid new due date is required!"

    if not new_student_name or not new_email:
        return "New borrower name and email are required!"

    if not new_email.endswith("@poornima.edu.in"):
        return "Please use a valid @poornima.edu.in email address!"

    if new_due_date < date.today():
        return "The new due date cannot be before the current date!"

    previous_student_name = booking.student_name
    booking.student_name = new_student_name
    booking.email = new_email
    booking.due_date = new_due_date
    db.session.commit()

    flash(
        f"Booking transferred from {previous_student_name} to {new_student_name}. "
        f"Due date updated to {new_due_date.strftime('%d %b %Y')}. "
        "Availability was unchanged, and no fee was charged.",
        "success"
    )

    return redirect(url_for("returns"))


@app.route("/return/<int:booking_id>", methods=["POST"])
def return_equipment(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    equipment = Equipment.query.get_or_404(booking.equipment_id)

    return_date = date.today()

    late_days = max(
        0,
        (return_date - booking.due_date).days
    )

    late_fee = late_days * LATE_FEE_PER_DAY

    refund = max(
        0,
        booking.deposit - late_fee
    )

    booking.return_date = return_date
    booking.late_fee = late_fee
    booking.refund = refund
    booking.status = "Returned"

    equipment.available_quantity += booking.quantity

    db.session.commit()

    flash(
        f"{booking.student_name}'s return was recorded. "
        f"Late fee: Rs {late_fee:.2f}. Refund: Rs {refund:.2f}.",
        "success"
    )

    return redirect(url_for("returns"))


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        if Equipment.query.count() == 0:

            equipment = [
                Equipment(
                    name="DSLR Camera",
                    total_quantity=5,
                    available_quantity=5,
                    daily_late_fee=LATE_FEE_PER_DAY
                ),
                Equipment(
                    name="Projector",
                    total_quantity=3,
                    available_quantity=3,
                    daily_late_fee=LATE_FEE_PER_DAY
                ),
                Equipment(
                    name="Microphone",
                    total_quantity=8,
                    available_quantity=8,
                    daily_late_fee=LATE_FEE_PER_DAY
                ),
                Equipment(
                    name="Tripod",
                    total_quantity=6,
                    available_quantity=6,
                    daily_late_fee=LATE_FEE_PER_DAY
                )
            ]

            db.session.add_all(equipment)
            db.session.commit()

    app.run(host="0.0.0.0", port=5000, debug=True)