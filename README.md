# College AV Room Gear Tracker

A Flask application for tracking AV equipment, bookings, returns, borrower transfers, deposits, and late fees.

## Requirements

- Python 3.10 or newer
- `pip`

## Project Setup

Open a terminal in the project directory:

```bash
cd /workspaces/Roushni-test-1
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Application

Start Flask with:

```bash
python app.py
```

Open the application at [http://127.0.0.1:5000](http://127.0.0.1:5000).

The first startup creates the SQLite database and inserts the default equipment when the database has no equipment records. The database is stored at `instance/av_room.db`.

## Main Pages

- `/` — dashboard, inventory, availability, and active bookings
- `/book/<equipment_id>` — create a booking
- `/returns` — process returns and transfer active bookings

Bookings require a `@poornima.edu.in` email address. Late returns use a fixed fee of Rs 25 per day. The refund is calculated as the deposit minus the late fee, never below zero.

## Validate the Project

Compile the Flask application:

```bash
python -m py_compile app.py
```

Render the main pages without starting a server:

```bash
python - <<'PY'
from app import app

with app.test_client() as client:
	for path in ["/", "/returns", "/book/1"]:
		response = client.get(path)
		print(path, response.status_code)
		assert response.status_code == 200
PY
```

## Debug in VS Code

1. Open the project folder in VS Code.
2. Select the Python interpreter from `.venv` using **Python: Select Interpreter**.
3. Open `app.py` and place breakpoints inside a route such as `book()`, `transfer_booking()`, or `return_equipment()`.
4. Open **Run and Debug**, choose the Python file configuration, and press **F5**.
5. Submit a booking or return form in the browser. Execution will pause at the breakpoint.

For a terminal debugger, run:

```bash
python -m pdb app.py
```

Useful values to inspect include `equipment.available_quantity`, `booking.due_date`, `late_fee`, and `refund`.

## Stop the Server

Press `Ctrl+C` in the terminal running Flask.