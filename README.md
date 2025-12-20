# 🚗 Python Car Rental Management System (Gallery Edition)

A high-end, modular desktop application built with **Python and PyQt5**. Version 3.0 introduces a modern **Card-Based Gallery UI**, replacing traditional tables with a dynamic, visual fleet management experience.

## ✨ New & Advanced Features

### 🖼️ Dynamic Gallery Interface (New!)
* **Card-Based UI:** Vehicles are now displayed as individual visual cards rather than simple text rows.
* **Image Integration:** Each vehicle supports custom image uploads (`.png`, `.jpg`), stored locally in the `assets/` directory.
* **Smart Grid Logic:** The interface uses a dynamic `QGridLayout` within a `QScrollArea`, automatically organizing vehicle cards based on window size.
* **Custom Backgrounds:** The login terminal features a professional high-definition background rendered via `QPainter` for maximum compatibility.

### 🛠️ Fleet & Data Management
* **Interactive Controls:** Each vehicle card features integrated "Rent", "Edit", and "Delete" actions with intuitive icons.
* **Modular Backend:** Powered by a decoupled `core/database.py` that handles JSON serialization and image path persistence.
* **Instant Filtering:** Real-time search by Plate, Make, or Model, with status-based filtering (Available/Rented).

### 📊 Professional Analytics
* **Enhanced History:** The transaction log now tracks **Make and Model** along with plate numbers for better auditing.
* **Financial Overview:** Real-time calculation of total cumulative revenue.
* **Utilization Pie Chart:** Visual representation of fleet occupancy using `matplotlib`.

## 💻 Technical Architecture

This project is built using a **Code-First (Pure Python) approach**, eschewing Qt Designer to maintain full programmatic control over dynamic widget generation.

* **GUI:** PyQt5 (Custom Widgets, QPainter, QSS)
* **Data:** JSON (Persistent local storage)
* **Plotting:** Matplotlib (Integrated into PyQt via FigureCanvas)
* **Architecture:** Modular MVC-style separation (`core` for logic, `gui` for views).

## 🚀 Getting Started

```bash
# Install dependencies
pip install PyQt5 PyQt5-stubs matplotlib

# Ensure assets are present
# Place vehicle images (arac1.png, etc.) and background.jpg in /assets

# Run the system
python main.py
```
Field	Value
Username	admin
Password	1234
Developed as a professional semester project focusing on Dynamic UI Management and Object-Oriented Programming.
