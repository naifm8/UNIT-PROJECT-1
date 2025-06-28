from users.patient import register_patient, login_patient, patient_menue, view_doctors, book_appointment

while True:
    print("\n1. Register as Patient\n2. Login as Patient\n3. Exit")
    chice = input("Choose (1-3):  ")

    if chice == "1":
        register_patient()
    elif chice == "2":
        patient = login_patient()
        if patient:
            patient_menue(patient)
    elif chice == "3":
        break




#patient.register_patient()
#patient.login_patient()
#patient.view_doctors()

#patient.patient_menue()

#patient.book_appointment("Naif Alghamdi")
#patient.book_appointment("Faisla Alghamdi")