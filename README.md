# Expense Tracker Dashboard

A lightweight local web application built with Python and Flask to enter, track, and analyze your daily finances. This application replaces manual spreadsheets with a clean and structured dashboard keeping data safely using a local SQLite database.

---

## Features

* **Real-time Financial Metrics:** View your total monthly spendings, current month's total, and total entry count at a glance
* **Dynamic Expense Logging:** Easily log expenses with detailed fields
* **Automated Categorization:** View a live "Category Summary" breakdown that groups your spending habits dynamically.
* **Persistent SQLite Storage:** Uses structured SQL instead of volatile local memory or flat CSV files, protecting against data corruption
* **OneDrive Path Protection:** Includes absolute path routing (`os.path`) to ensure smooth performance even when running inside synced cloud environments

---

## Tech Stack

* **Backend:** Python 3.13, Flask (Web Framework)
* **Database:** SQLite3 (Embedded Relational DB)
* **Frontend:** HTML5, CSS3

---

## Architecture & Data Flow

The diagram below illustrates how your interactions on the frontend dashboard communicate with the Python backend server to execute query actions inside your database:
