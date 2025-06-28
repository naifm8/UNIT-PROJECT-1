from utils.file_handler import load_json, save_json
import re
import uuid

def patient_menue(patient):
    while True:
        print("\n   ==== WELCOM! ====   ")
        print("==== PATIENT MENU ====\n")
        print("1. View Available Doctors")
        print("2. Use Symptom Checker")
        print("3. Book Appointment")
        print("4. Cancel Appointments")
        print("5. View My Appointments")
        print("6. View My Medical History")
        print("7. Update My Profile")
        print("8. Logout")

        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            pass 
        elif choice == "2":
            pass 
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            pass
        elif choice == "7":
            pass
        elif choice == "8":
            pass
        else:
            break

    

def register_patient():
    print("\n====PATIENT REGISTRATION====\n")
    patients = load_json('data/patients.json')

    #To validate username
    while True:
        username  = input("Enter your username: ").strip()
        if not username:
            print("username can't be empty.")
            continue
        if username.isdigit():
            print("User name can't be only numbers.")
            continue
        if any(p['username'].lower() == username.lower() for p in patients):
            print("username already exists.")
            continue
        break

    #To validate full name
    while True:
           full_name = input("Enter your full name: ").strip()
           if not full_name:
               print("Full name can't be empty.")
               continue
           if any(char.isdigit() for char in full_name):
               print("Full name can't contain numbers.")
           break
    
    #To validate email address
    while True:
            email = input("Email address: ").strip()
            if not email:
                print("Email can't be empty.")
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
    print("Registered successfully!")

def login_patient():
    print("\n====PATIENT LOGIN====\n")
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
                print(f"Welcome {matched_user['full_name']}!")
                return matched_user
    
    print("Too many failed attempts. returning to menu")
    return None

def view_doctors():
    doctors = load_json('data/doctors.json')
    if not doctors:
        print("No doctors found.")
    
    for doc in doctors:
        print(f"{doc["name"]} - {doc["specialty"]} (Available: {', '.join(doc["available_days"])})")


def book_appointment(patient_name):
    doctors = load_json('data/doctors.json')
    view_doctors()

    while True:
        doctor_name = input("Enter the name of the doctor you want to book: ")
        #Validation for the doctor input
        if not doctor_name:
            print("Doctor name can't be empty")
            continue
        doctor = next((d for d in doctors if d['name'].lower() == doctor_name.lower()), None)
        if doctor:
            break
        print("Doctor not found. please try again.")
    
    while True:
        day = input("Enter the day: ")
        if not day:
            print("Day cant be empty")
            continue
        #Check if day is in doctor's available days
        if day in doctor.get('available_days', []):
            break
        print(f"Doctor is not available on {day}. Doctor availability days: {", ".join(doctor.get('available_days', []))}")

    appointment = {
        "appointment_id" : str(uuid.uuid4()),
        "patient" : patient_name,
        "doctor" : doctor['name'],
        "day" : day,
        "status" : "pending"
    }

    appointments = load_json('data/appointments.json')
    if not isinstance(appointments, list):
        appointments = []
    appointments.append(appointment)
    save_json('data/appointments.json', appointments)
    print("Appointment booked.")