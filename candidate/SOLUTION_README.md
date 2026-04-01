# TASK SOLUTION

## Overview
This repository contains an automated test suite for a Vulnerability Management Dashboard composed of:
- Dashboard API (port 8000)
- Scanner Service (port 8001)
- PostgreSQL database

The goal was to validate system behavior, ensure data integrity, and identify existing bugs.

## Expected Test Outcome

The suite contains both validation tests and bug-exposing regression tests.
At the moment, several tests are expected to fail because they document confirmed defects in the application.
These defects are described in `BUG_REPORT.md`.

---

## Scope Covered

### 1. API Testing
- Full findings lifecycle:
  - create / read / update status / dismiss
- Error handling:
  - invalid inputs
  - non-existing resources
- Edge cases:
  - invalid status transitions
  - boundary conditions
- Search endpoint validation

### 2. Database Validation
- Verification of persistence after API operations
- Validation of relationships:
  - findings - assets
  - findings - vulnerabilities
- Constraint validation (e.g. invalid CVSS values)

### 3. Integration Testing
- Scanner - Dashboard flow:
  - running scan creates findings
- Cross-service consistency validation

### 4. UI Smoke Tests (Playwright)
- Dashboard page load
- Basic interaction validation

### 5. Bug Detection
Additional regression tests were added to expose hidden issues:
- invalid state transitions
- duplicate findings creation
- improper filtering / search handling
- missing validation in API / DB layer

See: `BUG_REPORT.md`

---

## Project Structure

candidate/
├── clients/        # API clients
├── db/             # DB helpers
├── tests/          # Test suite
├── pytest.ini
├── requirements.txt
├── BUG_REPORT.md
└── SOLUTION_README.md

---

## Setup

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

pip install -r requirements.txt
playwright install chromium

---

## Run Tests

pytest tests -v

---

## Notes

- Tests are designed to be deterministic and independent
- Fixtures and reusable clients are used for maintainability
- Focus was placed on real bug detection, not only happy paths
- Additional negative and edge-case tests were intentionally introduced to uncover issues
