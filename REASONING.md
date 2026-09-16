## AV Room Gear Tracker

### Problem Summary

The college AV room needs a reliable way to track cameras, projectors, microphones, tripods, and other equipment. The system must show availability, prevent conflicting bookings, record borrowers, manage due dates, calculate late fees, and support refundable deposits.

### Implementation Decisions

1. Use Flask with SQLAlchemy and SQLite so the application is simple to run and the booking history persists between requests.
2. Use an `Equipment` table to store each gear type, total quantity, available quantity, and daily late fee metadata.
3. Use a `Booking` table to store the borrower, contact email, equipment, quantity, borrow date, due date, deposit, return date, late fee, refund, and status.
4. Use a `User` table to store login names, official Poornima email addresses, password hashes, and roles.
5. Reduce `available_quantity` when a booking is created and restore it when the equipment is returned.
6. Reserve inventory with a conditional database update so concurrent requests cannot reserve more units than are available.
7. Treat a booking as overdue when its due date is before the current date.
8. Use a fixed late fee of Rs 25 per overdue day. Calculate the return amount with:

	```python
	late_fee = late_days * 25
	refund = max(0, booking.deposit - late_fee)
	```

	This means an on-time borrower receives the full deposit, while a late borrower receives the deposit minus the applicable fee. The refund cannot become negative.
9. Require booking and transfer dates to be today or later. The browser receives a `min` date, and Flask validates the same rule on the server so it cannot be bypassed.
10. Require the return date to be on or after the booking date.
11. Require all login and borrower emails to end in `@poornima.edu.in`.
12. Store passwords with secure hashes rather than plaintext values.
13. Restrict issuing, returns, transfers, and user creation to administrators. Students can view inventory availability and booking due dates.
14. Show the calculated late fee and refund after a return is processed so the result is visible to the AV room manager.

### Main User Flows

- **Dashboard:** View equipment quantities, current borrowings, and overdue bookings.
- **Authentication:** Sign in as an administrator or student. The dashboard and actions are protected by role.
- **User management:** An administrator creates student or administrator accounts with an official Poornima email and assigned password.
- **Book equipment:** An administrator selects a quantity, borrower, dates, email, and refundable deposit.
- **Return equipment:** Mark an active booking as returned. The application calculates the late fee, refund, return date, and updates availability.
- **Transfer booking:** An administrator transfers an active booking to another borrower and may update the due date without changing inventory. Late responsibility moves to the new borrower.
- **Search:** Filter equipment and current borrowings by equipment name, student name, or borrowed date.

### Validation

- The Flask application compiles successfully.
- The dashboard, booking page, and returns page render through Flask’s test client.
- Past booking dates are rejected.
- Negative deposits are rejected.
- Return dates before booking dates are rejected.
- Return processing stores the late fee and refund and displays the result to the user.
- Concurrent booking protection prevents overbooking when multiple requests arrive together.
- Students are denied access to admin-only routes, while administrators can access booking and management routes.
- Gmail addresses are rejected for user creation; valid `@poornima.edu.in` accounts are accepted.
- User passwords are stored as hashes.

### Remaining Improvements

- Add email or in-app reminders for upcoming and overdue returns.
- Add a booking conflict check if bookings need to be made in advance rather than only tracking currently borrowed equipment.
- Add password reset and forced password change for administrator-created temporary passwords.
- Move the development secret key and default account credentials into environment variables.
- Add database migrations for future schema changes.