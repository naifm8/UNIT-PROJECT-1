from users.patient import register_patient, login_patient, patient_menue
from users.doctor import login_doctor

while True:
    print("\n1. Register as Patient\n2. Login as Patient\n3. Login as a doctor")
    choise = input("Choose (1-3): ")

    if choise == "1":
        register_patient()
    elif choise == "2":
        patient = login_patient()
        if patient:
            patient_menue(patient)
    elif choise == "3":
        login_doctor()
    elif choise == "4":
        exit()
    else: print("Invalid input")