from utils.file_handler import load_json
from colorama import Fore
from art import tprint


DOCTORS_FILE = "data/doctors.json"

def symptom_checker():
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 30)
    print(Fore.LIGHTWHITE_EX + f"{'Symptom Checker':^30}")
    print(Fore.LIGHTCYAN_EX + "-" * 30 + "\n")

    def ask_yes_no(q):
        while True:
            a = input(q + " (yes/no): ").strip().lower()
            if a in ["yes", "no"]:
                return a
            print(" Please enter 'yes' or 'no'.")

    # Ask questions
    skin = ask_yes_no("Do you have skin issues?")
    chest = ask_yes_no("Do you feel chest pain?")
    stomach = ask_yes_no("Do you have stomach pain?")
    fever = ask_yes_no("Do you have fever or cough?")
    headache = ask_yes_no("Do you have headache or dizziness?")

    specialties = []

    # Priority combos
    if fever == "yes" and skin == "yes":
        specialties = ["Dermatologist"]
    elif chest == "yes" and headache == "yes":
        specialties = ["Cardiologist"]
    elif stomach == "yes" and fever == "yes":
        specialties = ["Gastroenterologist"]

    # Fallback
    if not specialties:
        if skin == "yes":
            specialties.append("Dermatologist")
        if chest == "yes":
            specialties.append("Cardiologist")
        if stomach == "yes":
            specialties.append("Gastroenterologist")
        if fever == "yes":
            specialties.append("General Physician")
        if headache == "yes":
            specialties.append("Neurologist")
        if not specialties:
            specialties = ["General Physician"]

    print("\n Based on your symptoms, we recommend:")
    for s in specialties:
        print(f" - {s}")

    return specialties