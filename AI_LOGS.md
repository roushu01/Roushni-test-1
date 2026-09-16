# AI Request Log

This document records the user requirements and change requests made during the development of the College AV Room Gear Tracker. Requests are rewritten for clarity while preserving their original intent.

## 1. Define the AV Room Lending System

Design and build an application for a college AV room that lends DSLR cameras, projectors, microphones, tripods, and other equipment. The application should:

- Track multiple units of popular equipment.
- Show current availability so students can determine whether equipment is free.
- Prevent conflicting bookings for the same equipment.
- Record borrowers and booking dates.
- Support sensible return dates.
- Apply a per-day late fee.
- Hold a refundable deposit and calculate the refund as the deposit minus applicable late fees.
- Prevent a single borrower from reserving an excessive amount of equipment.
- Help staff monitor and encourage timely returns.

## 2. Design the Flask Templates

Create and style `book.html`, `base.html`, and `returns.html` according to the routes, models, and data provided by `app.py`.

## 3. Explain the Refundable Deposit

Explain the purpose of the refundable deposit feature and how it supports responsible equipment returns.

## 4. Fix the Refundable Deposit Workflow

Review and correct the refundable deposit implementation so that deposits are collected during booking and refunds are calculated correctly when equipment is returned.

## 5. Provide the Current Date to Templates

Add a backend variable that provides the current date to the templates so overdue bookings can be identified reliably.

## 6. Validate Booking Dates

Ensure that a booking date cannot be earlier than the current date. The validation should work in both the browser form and the Flask backend.

## 7. Document the Implementation Rationale

Create a structured reasoning document that explains the project requirements, implementation decisions, data model, validation rules, and possible future improvements.

## 8. Analyze Simultaneous Booking Requests

Explain how the system should behave when five DSLR cameras are available and ten users attempt to book them at the same time.

## 9. Prevent Concurrent Overbooking

Implement concurrency protection so that when five DSLR units are available, exactly five valid booking requests can succeed and remaining requests are rejected without creating overbookings.

## 10. Use a Fixed Daily Late Fee

Set the late fee to a fixed rate of Rs 25 per overdue day and use the same rate consistently in calculations, forms, messages, and equipment defaults.

## 11. Add Borrower-to-Borrower Booking Transfers

Allow an active borrower to transfer their booking to another borrower without changing equipment availability. If the transfer occurs before the due date, the original borrower should not receive a late fee.

## 12. Allow Due-Date Changes During Transfers

Allow the incoming borrower to choose a new due date while transferring a booking. Validate the new date and use it for future overdue and late-fee calculations.

## 13. Restrict Student Email Addresses

Require borrowers to use an official email address ending in `@poornima.edu.in` when booking or receiving a transferred booking. Apply the restriction in both the browser and backend validation.

## 14. Improve the Dashboard Frontend

Improve the frontend of `index.html` so that it follows the visual style and layout conventions used by the other application pages.

## 15. Restore the Previous Dashboard

Restore the earlier Bootstrap-based version of `index.html`, including its dashboard cards, equipment cards, availability controls, borrowing table, overdue styling, and equipment search.

## 16. Search Current Borrowings

Add a search feature for active borrowed equipment. The search must support:

- Student name.
- Equipment name.
- Borrowed date.

## 17. Document Project Setup and Debugging

Update `README.md` with professional instructions for:

- Installing project dependencies.
- Creating and activating a virtual environment.
- Running the Flask application.
- Accessing the application locally.
- Understanding database initialization.
- Validating the application.
- Debugging with VS Code and `pdb`.

## 18. Create an AI Request Log

Create `AI_LOGS.md` and record all user requests made during the project conversation.

## 19. Improve the AI Request Log

Rewrite the recorded requests in a structured and professional format while preserving their meaning and chronological order.
