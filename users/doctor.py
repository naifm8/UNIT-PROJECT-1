from utils.file_handler import load_json, save_json
from users.patient import view_medical_history 
import datetime
import os

def login_doctor():
    print("\n--- Doctor Login ---")
    doctors = load_json("data/doctors.json")

    for attempts in range(3):
        doctor_name = input("Enter your name: ").strip()
        password = input("Enter your password: ").strip()

        doctor = next((d for d in doctors if d["name"].lower() == doctor_name.lower() and d["password"] == password), None)

        if doctor:
            print(f" Welcome, DR.{doctor['name']}!")
            doctor_menu(doctor)
            return
        else:
            print(" Invalid name or password.")

    print("Too many failed attempts. Returning to main menu.")


def doctor_menu(doctor):
    while True:
        print(f"\n==== DOCTOR PANEL DR.({doctor['name']}) ====")
        print("1. View My Appointments")
        print("2. View Patient Medical History")
        print("3. Add Diagnosis & Prescription")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_doctor_appointments(doctor['name'])
        elif choice == "2":
            view_patient_history()
        elif choice == "3":
            add_diagnosis_and_prescription(doctor['name'])
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def view_doctor_appointments(doctor_name):
    appointments = load_json("data/appointments.json")
    today = datetime.datetime.today().strftime("%A")  # e.g., "Sunday"

    my_appointments = [a for a in appointments if a["doctor"].lower() == doctor_name.lower() and a["day"].lower() == today.lower()]

    print(f"\n--- {doctor_name}'s Appointments for Today ({today}) ---")
    if not my_appointments:
        print("No appointments today.")
        return

    for i, app in enumerate(my_appointments, 1):
        print(f"{i}. Patient: {app['patient']} | Status: {app['status']} | Day: {app['day']} | ID: {app['appointment_id']}")


def suggest_medicine_from_diagnosis(diagnosis):
    diagnosis_words = diagnosis.lower().split()
    medicines = load_json("data/medicines.json")

    suggestions = set()
    for med in medicines:
        for condition in med.get("used_for", []):
            if any(word in condition.lower() for word in diagnosis_words):
                suggestions.add(med["name"])

    return list(suggestions)


def add_diagnosis_and_prescription(doctor_name):
    patient = input("Enter patient full name: ").strip().lower()
    if not patient:
        print(" Patient username is required.")
        return

    diagnosis = input("Enter diagnosis: ").strip()
    if not diagnosis:
        print(" Diagnosis cannot be empty.")
        return

    suggestions = suggest_medicine_from_diagnosis(diagnosis)
    if suggestions:
        print("\n Suggested medicines based on diagnosis:")
        for med in suggestions:
            print(f" - {med}")
    else:
        print("\nNo medicine suggestions found for this diagnosis.")

    prescription = input("Enter prescription (can include suggested meds): ").strip()
    if not prescription:
        print(" Prescription cannot be empty.")
        return
     # Save to patient's record file
    record_file = f"data/records/{patient}.json"
    records = load_json(record_file) if os.path.exists(record_file) else []

    entry = {
        "date": str(datetime.date.today()),
        "doctor": doctor_name,
        "diagnosis": diagnosis,
        "prescription": prescription
    }

    records.append(entry)
    save_json(record_file, records)

    print(f" Diagnosis and prescription saved to {patient}'s record.")

def view_patient_history():
    print("\n==== VIEW PATIENT MEDICAL HISTORY ====")
    username = input("Enter the patient full name: ").strip().lower()

    filepath = f"data/records/{username}.json"
    if not os.path.exists(filepath):
        print(" No record found for this patient. ")
        return
    
    history = load_json(filepath)

    if not history:
        print(" No medical records yet for this patient.")
        return
    
    print(f" Medical history for {username}")
    for i, record in enumerate(history, 1):
        print(f"\n Record #{i}")
        print(f"Date: {record.get('date', 'N/A')}")
        print(f"Doctor: {record.get('doctor', '-')}")
        print(f"Diagnosis: {record.get('diagnosis', '-')}")
        print(f"Prescription: {record.get('prescription', '-')}")

