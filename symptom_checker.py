from utils.file_handler import load_json

DOCTORS_FILE = "data/doctors.json"

def symptom_checker():
    print("\n==== Symptom Checker ====")
    print("Please answer the following questions (yes/no): ")

    #collect responses
    skin = input("Skin issues (rash, acne, itchiness)? ").strip().lower()
    chest = input("Chest pain or breathing difficulty? ").strip().lower()
    stomach = input("Stomach ache or nausea? ").strip().lower()
    fever = input("Fever, cough, or cold? ").strip().lower()
    headache = input("Headache or dizziness? ").strip().lower()

    specialties = []

    #if tow symptoms occured
    if fever == "yes" and skin == "yes":
        specialties = ["Dermatologist"]
    elif chest == "yes" and headache == "yes":
        specialties = ["Cardiologist"]
    elif stomach == "yes" and fever == "yes":
        specialties = ["Gastroenterologist"]

    #if one symptom occured
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

    #default if still empty
    if not specialties:
        specialties.append("General Physician")

    #result
    print("\n🩺 Suggested specialties based on your symptoms:")
    for s in specialties:
        print(f" - {s}")

    recommend_doctors_by_specialties(specialties)

def recommend_doctors_by_specialties(specialties):
    doctors = load_json(DOCTORS_FILE)

    for specialty in specialties:
        print(f"\n📋 Available {specialty}s:")
        matching = [d for d in doctors if d["specialty"].lower() == specialty.lower()]
        if not matching:
            print(" No doctors found.")
        else:
            for doc in matching:
                name = doc.get("name")
                days = ", ".join(doc.get("available_days", []))
                print(f" {name} (Available: {days})")
