from utils.file_handler import load_json, save_json
from utils.helpers import ask_side_effects, suggest_medicine_from_side_effects, get_dosage_by_medicine_name
import datetime
import os
from colorama import Fore
from tabulate import tabulate
from colorama import Fore

def doctor_menu(doctor):
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 37)
    print(Fore.LIGHTWHITE_EX + f"{"==== DOCTOR PANEL ====":^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 37 + "\n")
    while True:
        print("1. View My Appointments")
        print("2. Add Diagnosis & Prescription")
        print("3. View Patient Medical History")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_doctor_appointments(doctor['name'])
        elif choice == "2":
            add_diagnosis_and_prescription(doctor['name'])
        elif choice == "3":
            view_patient_history()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def login_doctor():
    print("\n--- Doctor Login ---")
    doctors = load_json("data/doctors.json")

    for attempts in range(3):
        doctor_name = input("Enter your full name: ").strip()
        password = input("Enter your password: ").strip()

        doctor = next((d for d in doctors if d["name"].lower() == doctor_name.lower() and d["password"] == password), None)

        if doctor:
            print(f" \nWelcome, DR.{doctor['name']}!")
            doctor_menu(doctor)
            return
        else:
            print(" Invalid name or password.")

    print("Too many failed attempts. Returning to main menu.")


def view_doctor_appointments(doctor_name):
    appointments = load_json("data/appointments.json")
    
    my_appointments = [a for a in appointments if a["doctor"].lower() == doctor_name.lower()]

    print(f"\n==== {doctor_name}'s Appointments ====")
    if not my_appointments:
        print(Fore.RED + "\nNo appointments today.")
        return
    
    table_data = []
    for i, app in enumerate(my_appointments, 1):
        table_data.append([
            i,
            app["patient"],
            app["status"],
            app["day"],
            app["appointment_id"]
        ])

    headers = ["#", "Patient", "Status", "Day", "Appointment ID"]

    print(Fore.LIGHTCYAN_EX + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
'''
def suggest_medicine_from_diagnosis(diagnosis):
    diagnosis_words = diagnosis.lower().split()
    medicines = load_json("data/medicines.json")

    suggestions = set()
    for med in medicines:
        for condition in med.get("used_for", []):
            if any(word in condition.lower() for word in diagnosis_words):
                suggestions.add(med["name"])

    return list(suggestions)
'''

def add_diagnosis_and_prescription(doctor_name):
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 48)
    print(Fore.LIGHTWHITE_EX + f"{"==== Add Prescription Based on Effects ====":^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 48 + "\n")

    patient = input("\nEnter patient full name: ").strip().lower()
    if not patient:
        print(Fore.RED +" Patient username is required.")
        return

    #using helper.py function for side effects
    effects = ask_side_effects()
    if not effects:
        print(Fore.RED +" No side effects selected. Cannot continue.")
        return

    #suggest medicine based on side effects
    suggestions = suggest_medicine_from_side_effects(effects)
    if suggestions:
        print(Fore.LIGHTCYAN_EX + "\nSuggested medicines based on side effects:")
        table_data = [[i + 1, med] for i, med in enumerate(suggestions)]
        headers = ["#", "Medicine"]
        print(Fore.LIGHTGREEN_EX + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print(Fore.RED + "No medicines found for the reported side effects.")

    # Let doctor to leave a note
    prescription = input("\nEnter prescription (or leave a note): ").strip()
    if not prescription:
        print(Fore.RED + " Prescription cannot be empty.")
        return
    
    #use the helper.py method to get the medicine dosage
    medicine_name = prescription.split()[0]
    diagnosis = get_dosage_by_medicine_name(medicine_name)

    os.makedirs("data/records", exist_ok=True)
    #save data to records
    clean_name = patient.strip().replace(" ", "").lower()
    record_file = f"data/records/{clean_name}.json"
    records = load_json(record_file) if os.path.exists(record_file) else []

    entry = {
    "date": str(datetime.date.today()),
    "doctor": doctor_name,
    "diagnosis": diagnosis,  # Now this holds the dosage
    "prescription": prescription
    }

    records.append(entry)
    save_json(record_file, records)
    print(Fore.LIGHTGREEN_EX + f"\n Prescription saved to {patient}'s record.")

def view_patient_history():
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 39)
    print(Fore.LIGHTWHITE_EX + f"{"==== VIEW PATIENT MEDICAL HISTORY ====":^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 39 + "\n")
    username = input("Enter the patient full name: ").strip().lower()

    clean_name = username.replace(" ", "").lower()
    filepath = f"data/records/{clean_name}.json"    
    
    if not os.path.exists(filepath):
        print(" No record found for this patient. ")
        return
        
    history = load_json(filepath)

    if not history:
        print(Fore.YELLOW + "No medical records yet for this patient.")
        return

    print(Fore.LIGHTCYAN_EX + f"\nMedical history for {username.capitalize()}\n")

    table_data = []
    for i, record in enumerate(history, 1):
        table_data.append([
            i,
            record.get("date", "N/A"),
            record.get("doctor", "-"),
            record.get("diagnosis", "-"),
            record.get("prescription", "-")
        ])

    headers = ["#", "Date", "Doctor", "Diagnosis", "Prescription"]

    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    print('\n')

