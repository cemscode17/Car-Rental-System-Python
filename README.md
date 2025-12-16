# 🚗 Python Car Rental Management System (v2.4)

A robust, modular desktop application developed using **Python and PyQt5** for managing vehicle rentals, fleet inventory, and financial reporting. Designed with clean architecture principles to ensure maintainability and scalability.

## ✨ Key Features

### User Interface & Experience
* **Modular Architecture:** Project code is professionally separated into `core`, `gui`, and `assets` directories (simulating an MVC pattern).
* **Dynamic Theming:** Seamless one-click transition between **Dark Mode** and **Light Mode** across the entire application interface.
* **Modern GUI:** Clean, contemporary design with custom Qt Style Sheets (QSS), providing a highly intuitive user experience.
* **Efficient Search:** Instant filtering across the main fleet table by **License Plate, Make, Model, and Status**.

### Operations and Data Integrity
* **Comprehensive CRUD:** Full functionality to **C**reate, **R**ead, **U**pdate (edit), and **D**elete vehicle inventory records.
* **Rental Workflow:** Automated fee calculation and instantaneous status updates (`Available` ↔ `Rented`).
* **Data Persistence:** Vehicle inventory and all transaction history are stored locally in a persistent **JSON** file (`araclar.json`).

## 📊 Detailed Financial and Fleet Analytics

The dedicated analysis panel provides critical business intelligence:

* **Revenue Tracking:** Displays the cumulative total revenue (`Toplam Gelir`).
* **Fleet Utilization:** A **pie chart** visualization showing the exact percentage distribution of **Available vs. Rented** vehicles.
* **Immutable Transaction History:** A detailed, chronological record of every past rental transaction, including the **Customer, Total Amount, and Rental Duration (Days)**. *(Ensures data integrity even after vehicles are removed from the fleet.)*

## 🚀 Getting Started

### Requirements 

The project requires Python 3 and the following dependencies:

```bash
pip install PyQt5 PyQt5-stubs matplotlib
```
Starting the Application
Follow these steps to clone and run the system:

1. Clone the repository and navigate to the project root directory.
2. Ensure your logo file (logo.png) is correctly placed inside the assets folder.
3. Execute the application using the command below:
```bash
python main.py
```
## 🔑 Access Credentials

The application uses a single administrator login with full privileges:

| Field | Value |
| :--- | :--- |
| **Username** | `admin` |
| **Password** | `1234` |
