# VeriPy

English · [Русский](README.ru.md)

**REST API test automation with Python and pytest.**

VeriPy is a test automation framework for the Restful Booker
booking API. It covers authentication, booking CRUD operations, access control,
filtering, response schema validation, and a complete booking lifecycle.

The suite currently collects **25 test cases**, including parametrized scenarios.
Tests use real HTTP requests, generate their own booking data, and clean up
created records through pytest fixtures. Parallel execution and repeated runs
are available through pytest plugins.

Learn more about the target service in the
[Restful Booker API documentation](https://restful-booker.herokuapp.com/apidoc/index.html).

## Technology stack

| Tool | Purpose |
| --- | --- |
| Python | API client, fixtures, and test scenarios |
| pytest | Test execution, assertions, fixtures, and parametrization |
| requests | HTTP requests with explicit timeouts |
| Faker and UUID | Synthetic booking data and unique guest names |
| jsonschema | Required fields, value types, and date format validation |
| pytest-xdist | Parallel test execution |
| pytest-repeat | Repeated execution for investigating intermittent failures |
| GitHub Actions | Automatic and manual test execution in CI |

## Getting started

Use **Python 3.13**, Git, and an internet connection to the public demo API.
Run the commands below from a terminal.

### Windows PowerShell

```powershell
git clone https://github.com/DenisBogdanenko/VeriPy.git
cd VeriPy
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

If you already have the project locally, start from its root directory and
create the virtual environment if needed. The commands use the environment's
Python directly, so activation is optional.

### Linux and macOS

```bash
git clone https://github.com/DenisBogdanenko/VeriPy.git
cd VeriPy
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -v
```

In PyCharm, open the repository root and select `.venv` as the project
interpreter. Run the examples from the terminal in that directory.

## Running tests

The examples below use Windows PowerShell. On Linux or macOS, use
`.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

### Collect test cases

List the collected cases without sending requests to the API.

```powershell
.\.venv\Scripts\python.exe -m pytest --collect-only -q
```

### Run a file or a single test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_get_booking.py -v
.\.venv\Scripts\python.exe -m pytest tests/test_booking_flow.py::test_booking_lifecycle -v
```

### Run in parallel

Choose the number of worker processes with `-n`.

```powershell
.\.venv\Scripts\python.exe -m pytest -n 2 -v
```

For example, `-n 10` uses ten workers. Each test creates its own data, and
requests within a single test execute in their written order. Actual runtime
depends on the API's response times and availability.

### Repeat test cases

Run every collected case five times, distributed across two workers.

```powershell
.\.venv\Scripts\python.exe -m pytest -n 2 --count=5 -v
```

With 25 collected cases, this produces 125 executions. To run five complete
rounds sequentially, use session repetition with parallel execution disabled.

```powershell
.\.venv\Scripts\python.exe -m pytest -n 0 --count=5 --repeat-scope=session -v
```

Add `-x` to stop the run on the first failure or error.

## GitHub Actions

The `API tests` workflow runs automatically for pushes to `main` and pull
requests targeting `main`. It installs the dependencies and runs the suite
on Ubuntu with Python 3.13 and two pytest workers.

### Run tests from your browser

1. Open the [API tests workflow](https://github.com/DenisBogdanenko/VeriPy/actions/workflows/tests.yml).
2. Click **Run workflow**, select the `main` branch, and click **Run workflow** again.
3. Open the new run, select **api-tests**, and expand **Run API tests** to view
   the pytest output and any failures.

A green check marks a successful run. A red cross marks a failed run.
Manual runs require a signed-in GitHub account with write access to the repository.

## Configuration

| Setting | Value |
| --- | --- |
| `BOOKER_BASE_URL` | Defaults to `https://restful-booker.herokuapp.com` |
| Demo username | `admin` |
| Demo password | `password123` |
| Request connect/read timeout | `10` seconds |

Set a different API address in the current PowerShell terminal before running
the tests. The target must implement the Restful Booker endpoints and support
the demo account used by the authentication fixture.

```powershell
$env:BOOKER_BASE_URL = "http://localhost:3001"
.\.venv\Scripts\python.exe -m pytest -v
```

On Linux or macOS, set the variable for a single run.

```bash
BOOKER_BASE_URL=http://localhost:3001 .venv/bin/python -m pytest -v
```

The examples above require a running Restful Booker instance at that address.
Credentials are currently defined in `conftest.py` and the authentication tests.

## Test coverage

| Area | Cases | Checks |
| --- | --- | --- |
| Health | 1 | API availability |
| Authentication | 2 | Token creation and invalid password |
| Booking creation | 8 | Valid payload, missing required fields, missing dates |
| Booking retrieval | 4 | ID list, reading by ID, schema validation, name filtering |
| Booking updates | 6 | PUT and PATCH, persisted changes, missing or invalid tokens |
| Booking deletion | 3 | Successful deletion, missing or invalid tokens |
| Booking lifecycle | 1 | Create, read, PUT, PATCH, delete, and verify absence |
| **Total** | **25** | |

The schema check is part of the read-by-ID test. Parametrized inputs count as
separate test cases.

## Project structure

```text
VeriPy/
├── .github/
│   └── workflows/
│       └── tests.yml
├── api/
│   ├── __init__.py
│   └── booking_client.py
├── schemas/
│   ├── __init__.py
│   └── booking_schema.py
├── tests/
│   ├── test_auth.py
│   ├── test_booking_flow.py
│   ├── test_create_booking.py
│   ├── test_delete_booking.py
│   ├── test_get_booking.py
│   ├── test_health.py
│   └── test_update_booking.py
├── utils/
│   ├── __init__.py
│   └── data_generator.py
├── .gitignore
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── README.ru.md
```

- `api/` builds HTTP requests and returns response objects for test assertions.
- `schemas/` defines the booking response structure and date formats.
- `utils/` generates guest data, prices, future booking dates, and unique names.
- `conftest.py` provides the API client, data, authentication token, and booking
  setup and teardown fixtures.
- `tests/` contains assertions about API responses and persisted data.
- `pytest.ini` sets the test directory, summary options, and strict marker checks.

## Test data and cleanup

Every test requesting `booking_data` receives a fresh payload. Guest names
include a UUID, prices are generated between 100 and 200, and checkout is two
days after checkin.

The `created_booking` fixture obtains a token and creates a booking before the
test. During teardown, it checks whether the booking still exists and deletes
it with a valid token. If the test has already deleted the record, teardown
accepts its absence. Cleanup also runs after an assertion failure in the test.

## Interpreting results

The suite records several responses specific to the target API.

| Scenario | Expected response in the current tests |
| --- | --- |
| Health check | HTTP `201` |
| Successful booking creation | HTTP `200` |
| Successful booking deletion | HTTP `201` |
| Invalid login password | HTTP `200` with `reason` and no token |
| Protected operation without a valid token | HTTP `403` |
| Reading a deleted booking | HTTP `404` |
| Creating a booking with missing required data | HTTP `500`, `Internal Server Error` |

The missing-data tests capture the demo API's observed server-error response.
These cases document its current behavior. The error-handling design is a
separate subject for investigation and bug reporting.

The public API is shared and can reset its records. A reset between creation
and retrieval can cause a failure. Network interruptions or HTTP `503`
responses can also produce test or teardown errors. If teardown fails, a test
record may remain on the service.

When a run fails, inspect the reported phase and HTTP response. An error in
fixture setup or teardown identifies a different failing step from an
assertion in the test body. Re-run the affected case on its own to investigate
whether the failure is reproducible. Pytest includes the exact node ID in the
failure summary.
