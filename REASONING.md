## AV Room Gear Tracker

### Problem Summary

The college AV room needs a reliable way to track cameras, projectors, microphones, tripods, and other equipment. The system must show availability, prevent conflicting bookings, record borrowers, manage due dates, calculate late fees, and support refundable deposits.

### Implementation Decisions

1. Use Flask with SQLAlchemy and SQLite so the application is simple to run and the booking history persists between requests.
2. Use an `Equipment` table to store each gear type, total quantity, available quantity, and daily late fee.
3. Use a `Booking` table to store the borrower, contact email, equipment, quantity, borrow date, due date, deposit, return date, late fee, refund, and status.
4. Reduce `available_quantity` when a booking is created and restore it when the equipment is returned.
5. Treat a booking as overdue when its due date is before the current date.
6. Calculate the return amount with:

	```python
	late_fee = late_days * equipment.daily_late_fee
	refund = max(0, booking.deposit - late_fee)
	```

	This means an on-time borrower receives the full deposit, while a late borrower receives the deposit minus the applicable fee. The refund cannot become negative.
7. Require the booking date to be today or later. The browser receives a `min` date, and Flask validates the same rule on the server so it cannot be bypassed.
8. Require the return date to be on or after the booking date.
9. Show the calculated late fee and refund after a return is processed so the result is visible to the AV room manager.

### Main User Flows

- **Dashboard:** View equipment quantities, current borrowings, and overdue bookings.
- **Book equipment:** Select a quantity, borrower, dates, email, and refundable deposit.
- **Return equipment:** Mark an active booking as returned. The application calculates the late fee, refund, return date, and updates availability.
- **Search:** Filter equipment on the dashboard by name.

### Validation

- The Flask application compiles successfully.
- The dashboard, booking page, and returns page render through Flask’s test client.
- Past booking dates are rejected.
- Negative deposits are rejected.
- Return dates before booking dates are rejected.
- Return processing stores the late fee and refund and displays the result to the user.

### Remaining Improvements

- Replace plain validation responses with reusable form error messages.
- Add authentication for AV room staff.
- Add email or in-app reminders for upcoming and overdue returns.
- Add a booking conflict check if bookings need to be made in advance rather than only tracking currently borrowed equipment.