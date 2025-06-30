<div align="center">

# 🏥 Clinic Management System (Doctor & Patient)

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-Complete-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey)]()
[![Made with JSON](https://img.shields.io/badge/Data-JSON-yellow)]()

</div>

---

This project is a command-line-based Clinic Management System developed in Python.  
It models real-world workflows between **doctors** and **patients**, including user authentication and authorization, appointment booking, and integration with multiple JSON files.  
This project is my way of applying what I’ve learned in previous lessons, including file handling, functions, and user interaction using Python.

The system focuses on:
- Booking appointments  
- Recommending doctor specialty based on symptoms  
- Helping doctors choose the right medicine based on side effects  
- Saving patient history with dosage and prescriptions

---

## 📋 How the System Works

When you run the program, a main menu appears:

```
1. Register as Patient  
2. Login as Patient  
3. Login as Doctor  
4. Exit
```

---

### 👨‍💻 Patient Menu

After logging in, a patient can:

- View Available Doctors  
- Book Appointment  
- View My Appointments  
- Cancel Appointments  
- View My Medical History  
- Logout

---

### 🧑‍⚕️ Doctor Menu

After logging in, a doctor can:

- View My Appointments  
- Add Diagnosis & Prescription  
- View Patient Medical History  
- Logout

---

## 🧠 Smart Medicine Suggestion

When adding a diagnosis, the doctor answers a few **yes/no side effect questions** (e.g., nausea, headache, rash).  
The system then:

- Suggests relevant medicines from `medicines.json`
- Retrieves the correct **dosage**
- Saves everything to the patient’s record file

---

## 🗂 Data Structure

- `data/doctors.json` → List of doctors with specialties and availability  
- `data/medicines.json` → Medicines with type, dosage, and side effects  
- `data/records/<username>.json` → Patient medical history saved per visit  
- `data/appointments.json` → Booked appointment information

---

## 🧪 Example Scenario

1. A patient registers and books an appointment.
2. The doctor logs in, selects the patient, and answers symptom questions.
3. The system suggests a medicine (e.g., **Losartan**) and shows the dosage.
4. The doctor saves the prescription.
5. Later, the patient can view their full medical history.

---

## 🛠 Built With

- Python 3  
- JSON files (no external database)  
- Terminal-based menus (no GUI)

---

## 👨‍💻 About the Project

This was created during a Python Bootcamp to practice:

- Real-world programming logic  
- User input and validation  
- File handling and structured data  
- Role-based systems

> ✅ All major features tested and fully functional.
