from utils.file_handler import load_json, save_json
from utils.helpers import view_doctors
import symptom_checker
import re
import uuid
import os
from colorama import Fore, Style, init
from art import tprint
from tabulate import tabulate
from colorama import Fore

init(autoreset=True)  

def patient_menue(patient):
        
    print("\n" + Fore.CYAN + "=" * 60)
    tprint("Welcome!", font="stander") 
    print(Fore.CYAN + "=" * 60)

    while True:
        print(Fore.GREEN + f"\n{'PATIENT MENU':^50}\n")
        print(Fore.YELLOW + "1. 🩺  View Available Doctors")
        print(Fore.YELLOW + "2. 📅  Book Appointment")
        print(Fore.YELLOW + "3. 📖  View My Appointments")
        print(Fore.YELLOW + "4. ❌  Cancel Appointments")
        print(Fore.YELLOW + "5. 🗂️   View My Medical History")
        print(Fore.RED +    "6. 🔒  Logout")
        print(Fore.CYAN + "=" * 60)

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
             view_doctors()
        elif choice == "2":
            specialties = symptom_checker.symptom_checker()
            book_appointment(patient["full_name"], specialties)
        elif choice == "3":
            view_my_appointments(patient["full_name"])
        elif choice == "4":
            cancel_appointment(patient["full_name"])
        elif choice == "5":
            view_medical_history(patient["full_name"])
        elif choice == "6":
            return
        else:
            print("Invalid input, choose: 1-6")

    

def register_patient():
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 30)
    print(Fore.LIGHTWHITE_EX + f"{"==== PATIENT REGISTRATION ====":^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 30 + "\n")
    patients = load_json('data/patients.json')

    #To validate username
    while True:
        username  = input("Enter your username: ").strip()
        if not username:
            print(Fore.RED +"username can't be empty.")
            continue
        if username.isdigit():
            print(Fore.RED +"User name can't be only numbers.")
            continue
        if any(p['username'].lower() == username.lower() for p in patients):
            print(Fore.RED +"username already exists.")
            continue
        break

    #To validate full name
    while True:
           full_name = input("Enter your full name: ").strip()
           if not full_name:
               print(Fore.RED +"Full name can't be empty.")
               continue
           if any(char.isdigit() for char in full_name):
               print(Fore.RED +"Full name can't contain numbers.")
               continue
           break
    
    #To validate email address
    while True:
            email = input("Email address: ").strip()
            if not email:
                print(Fore.RED +"Email can't be empty.")
                continue
            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                print("Invalid email format")
                continue
            break
    
     #To validate phone number
    while True:
            phone = input("Phone number: ").strip()
            if not phone:
                print("Phone number can't be empty.")
                continue
            if not phone.isdigit():
                print("Phone number must contain only digits.")
                continue
            break

    #To validate password
    while True:
        password  = input("Enter your password: ").strip()
        if not password:
            print("The password can't be empty.")
            continue
        if len(password) < 6:
            print("Password must be at least 6 characters.")
            continue
        break

    #To validate age
    while True:
        age = input("Enter your age: ").strip()
        if not age:
            print("The age can't be empty.")
            continue
        if not age.isdigit():
            print("Age must be a number. ")
            continue
        age = int(age)
        if age < 1 or age > 120:
            print("Age must be between 1 and 120")
            continue
        break

    #To validate gender
    while True:
        gender = input("Enter your gender (Male/Female): ").strip().capitalize()
        if not gender:
            print("The gender can't be empty.")
            continue
        if gender not in ["Male" , "Female"]:
            print("Gender must be 'Male" or 'Female')
            continue
        break
    

    # Saving the patient information
    new_patient = {
        "username" : username,
        "full_name" : full_name,
        "email" : email,
        "phone" : phone,
        "password" : password,
        "age" : age,
        "gender" : gender
    }

    #Appending the new registerd patient into the .json file
    patients.append(new_patient)
    save_json('data/patients.json', patients)
    print(Fore.LIGHTGREEN_EX +"Registered successfully!")

def login_patient():
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 30)
    print(Fore.LIGHTWHITE_EX + f"{"==== PATIENT LOGIN ====":^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 30 + "\n")
    patients = load_json('data/patients.json')
    if not patients:
        print("No registerd patients found.")
        return None
    
    for attempt in range(3):
        username = input("Username: ").strip().lower()
        password = input("Password: ").strip()

        if not username or not password:
            print("Both username and password are required. ")
            continue

        matched_user = None
        for patient in patients:
            if patient['username'].lower() == username.lower():
                matched_user = patient
                break
        if matched_user is None or matched_user['password'] != password:
                print("Username not found or incorrect password")
        else:
                print(Fore.LIGHTGREEN_EX +f"Welcome {matched_user['full_name']}!")
                return matched_user
    
    print("Too many failed attempts. returning to menu")
    return None


def book_appointment(patient_name, specialties=None):
    doctors = load_json('data/doctors.json')
    if not doctors:
        print(Fore.LIGHTRED_EX +" No doctors available at the moment.")
        return

    # Filter doctors based on specialties
    if specialties:
        doctors = [d for d in doctors if d['specialty'] in specialties]
    if not doctors:
        print(Fore.RED + "No doctors to recommend.")
    else:
        print(Fore.LIGHTGREEN_EX + "\nThese doctors are recommended:\n")

        table_data = []
        for i, doc in enumerate(doctors, 1):
            table_data.append([
                i,
                doc["name"],
                doc["specialty"],
                ", ".join(doc["available_days"])
                  ])

        headers = ["#", "Name", "Specialty", "Available Days"]
        print(Fore.LIGHTWHITE_EX + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


    # Choose doctor
    while True:
        doctor_name = input("Enter the name of the doctor you want to book: ").strip()
        if not doctor_name:
            print(Fore.LIGHTRED_EX +" Doctor name can't be empty.")
            continue
        def normalize_name(name):
            return name.replace("-", " ").replace("_", " ").lower().strip()
        doctor = next((d for d in doctors if normalize_name(d['name']) == normalize_name(doctor_name)),None)
        if doctor:
            break
        print(Fore.LIGHTRED_EX +" Doctor not found. Please try again.")

    # Choose day
    available_days = [d.lower() for d in doctor.get('available_days', [])]

    while True:
        day = input("Enter the day you want to book: ").strip()
        if not day:
            print(Fore.LIGHTRED_EX +" Day can't be empty.")
            continue

        if day.lower() in available_days:
            break
        print(Fore.LIGHTRED_EX +f" Doctor is not available on {day}. Available: {', '.join(doctor.get('available_days', []))}")

    # Save appointment
    import uuid
    appointment = {
        "appointment_id": str(uuid.uuid4()),
        "patient": patient_name,
        "doctor": doctor["name"],
        "day": day.capitalize(),
        "status": "pending"
    }

    appointments = load_json("data/appointments.json")
    if not isinstance(appointments, list):
        appointments = []
    appointments.append(appointment)
    save_json("data/appointments.json", appointments)

    print(Fore.LIGHTGREEN_EX +f"\n Appointment booked with {doctor['name']} on {day.capitalize()}.\n")

def view_my_appointments(patient_name):
    appointments = load_json("data/appointments.json")

    my_appointments = [a for a in appointments if a['patient'].lower() == patient_name.lower()]
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 30)
    print(Fore.LIGHTWHITE_EX + f"{'==== My Appointments ====':^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 30 + "\n")

    if not my_appointments:
        print(Fore.LIGHTYELLOW_EX +"You have no appointments yet")
        return
    
    table_data = []
    for i, app in enumerate(my_appointments, 1):
        table_data.append([
          i,
          app["doctor"],
          app["day"],
          app["status"],
          app["appointment_id"]
        ])

    # Define headers
    headers = ["#", "Doctor", "Day", "Status", "Appointment ID"]

    # Print the table with color
    print(Fore.LIGHTCYAN_EX +  tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    #for i, app in enumerate(my_appointments, 1):
    #    print(Fore.LIGHTGREEN_EX +f"\n{i}. Doctor: {app['doctor']} | Day: {app['day']} | Status: {app['status']} | ID: {app['appointment_id']}")

def cancel_appointment(patient_name):
    appointments = load_json("data/appointments.json")
    my_appointments = [a for a in appointments if a["patient"].lower() == patient_name.lower()]

    if not my_appointments:
        print(Fore.LIGHTRED_EX +"\nYou have no appointments to cancel")
        return
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 30)
    print(Fore.LIGHTWHITE_EX + f"{'==== Your Appointments ====':^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 30 + "\n")

    table_data = []
    for i, app in enumerate(my_appointments, 1):
        table_data.append([
            i,
            app["doctor"],
            app["day"],
            app["status"],
            app["appointment_id"]
        ])

    headers = ["#", "Doctor", "Day", "Status", "Appointment ID"]

    print(Fore.LIGHTCYAN_EX + tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    while True:
        appointment_id = input("\nEnter the Appointment ID you want to cancel (or '0' to go back): ").strip()
        if appointment_id == "0":
            return
        if not appointment_id:
            print(Fore.LIGHTRED_EX +" Appointment ID cannot be empty.")
            continue

        # Find matching appointment
        match = next((a for a in appointments if a["appointment_id"] == appointment_id and a["patient"].lower() == patient_name.lower()), None)

        if not match:
            print(Fore.LIGHTRED_EX +" No appointment found with that ID for your account.")
            continue

        appointments.remove(match)
        save_json("data/appointments.json", appointments)
        print(Fore.LIGHTGREEN_EX + " \nAppointment canceled successfully.")
        break

def view_medical_history(paitent_name):
    clean_name = paitent_name.replace(" ", "").lower()
    record_file = f"data/records/{clean_name}.json"

    if not os.path.exists(record_file):
        print(Fore.LIGHTYELLOW_EX + "\n You have no medical history yet.")
        return
    
    records = load_json(record_file)

    if not records:
        print("\n Your medical history is empty.")
        return
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 30)
    print(Fore.LIGHTWHITE_EX + f"{'==== YOUR MEDICAL HISTORY ====':^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 30 + "\n")
    for i, record in enumerate(records, 1):
        print(f"\n{i}. Date: {record['date']}")
        print(f"   Doctor: {record['doctor']}")
        print(f"   Diagnosis: {record['diagnosis']}")
        print(f"   Prescription: {record['prescription']}")