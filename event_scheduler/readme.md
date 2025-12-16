# Event Scheduling & Resource Allocation System

## Project Overview

This project is a Flask-based web application developed as part of a hiring/assessment test. The system allows organizations such as colleges, training centers, or offices to schedule events (seminars, workshops, meetings) and allocate shared resources (rooms, instructors, equipment) without conflicts.

The application ensures that no resource is double-booked by validating time overlaps during event creation and resource allocation.

---

## 🎯 Objectives

- Schedule events with start and end times
- Manage shared resources
- Allocate resources to events
- Detect and prevent scheduling conflicts
- Generate resource utilization reports

---

## 🛠️ Technologies Used

- Python
- Flask (Web Framework)
- SQLite (Database)
- HTML & CSS (Frontend)
- Jinja2 (Templating Engine)

---

## 📂 Project Structure

```
event-scheduling-system/
│
├── app.py
├── requirements.txt
├── database.db
│
├── templates/
│   ├── base.html
│   ├── events.html
│   ├── resources.html
│   ├── allocate.html
│   ├── conflicts.html
│   └── report.html
│
├── static/
│   └── style.css
│
├── screenshots/
│   ├── events.png
│   ├── resources.png
│   ├── allocation.png
│   ├── conflict.png
│   └── report.png
│
└── README.md
```

---

## 🗄️ Database Design

### 1. Event Table

- event_id (Primary Key)
- title
- start_time
- end_time
- description

### 2. Resource Table

- resource_id (Primary Key)
- resource_name
- resource_type (Room / Instructor / Equipment)

### 3. EventResourceAllocation Table

- allocation_id (Primary Key)
- event_id (Foreign Key)
- resource_id (Foreign Key)

---

## 🔑 Features Implemented

- Add / Edit / View Events
- Add / Edit / View Resources
- Allocate Resources to Events
- Conflict Detection (No double booking)
- Edge Case Handling (Exact match, partial overlap, nested events)
- Resource Utilization Report (based on date range)

---

## ⚙️ How to Run the Project

### Step 1: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 2: Run the Flask Application

```bash
python app.py
```

### Step 3: Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📊 Use Case Demonstration

- Create 3–4 resources (rooms, instructors, equipment)
- Create multiple events with overlapping time slots
- Allocate resources to events
- Display conflict error messages when overlaps occur
- Generate resource utilization report for a selected date range

---

## 📸 Screenshots

Screenshots of the application are available in the **screenshots/** folder:

- Event Management Page
- Resource Management Page
- Resource Allocation Page
- Conflict Detection Message
- Resource Utilization Report

---

## 🎥 Demo Video

A screen-recorded demo video showing the working of the application is included via an external link:

🔗 https://drive.google.com/drive/u/0/folders/16k1qT49utrVgRPsVcce02HHad0e0ndyd

---

## 🚀 Future Enhancements

- User authentication and roles
- Calendar-based event view
- Email notifications for conflicts
- Export reports to PDF/Excel

---

## 👤 Author

Name: Suba Harichandran
Project Type: Event scheduler
