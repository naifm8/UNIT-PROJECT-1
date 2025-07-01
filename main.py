from users.patient import register_patient, login_patient, patient_menue
from users.doctor import login_doctor
from colorama import Fore, Style, init
from art import tprint

init(autoreset=True)

while True:
    print("\n")
    print(Fore.LIGHTCYAN_EX + "=" * 70)
    tprint("Clinic   System", font="standard")  
    print(Fore.LIGHTGREEN_EX + f"{'MAIN MENU':^70}")
    print(Fore.LIGHTCYAN_EX + "=" * 70)

    print(Fore.LIGHTWHITE_EX + "1. 📝  Register as Patient")
    print(Fore.LIGHTWHITE_EX + "2. 👤  Login as Patient")
    print(Fore.LIGHTWHITE_EX + "3. 🩺  Login as Doctor")
    print(Fore.LIGHTWHITE_EX + "4. ❌  Exit")
    print(Fore.LIGHTCYAN_EX + "=" * 70)

    choice = input(Fore.LIGHTYELLOW_EX + "Choose (1-4): ").strip()

    if choice == "1":
        register_patient()
    elif choice == "2":
        patient = login_patient()
        if patient:
            patient_menue(patient)
    elif choice == "3":
        login_doctor()
    elif choice == "4":
        print(Fore.LIGHTRED_EX + "\nExiting the system. Goodbye!\n")
        break
    else:
        print(Fore.RED + "Invalid input. Please enter a number between 1 and 4.")