from utils.file_handler import load_json, save_json

def view_doctors():
    print("\n==== AVAILABLE DOCTORS ====\n")
    doctors = load_json('data/doctors.json')
    if not doctors:
        print("No doctors found.")
        return
    for doc in doctors:
        print(f"{doc["name"]} - {doc["specialty"]} (Available: {', '.join(doc["available_days"])})")

def suggest_medicine_from_side_effects(reported_effects):
    medicines = load_json("data/medicines.json")
    reported_effects = [e.lower() for e in reported_effects]

    suggestions = []

    for med in medicines:
        med_side_effects = [se.lower() for se in med.get("side_effects", [])]
        if all(effect in med_side_effects for effect in reported_effects):
            suggestion = f"{med['name']} ({med['type']}) - {med['dosage']}"
            if med.get("prescription_required"):
                suggestion += " [Prescription Required]"
            suggestions.append(suggestion)

    return suggestions

def ask_side_effects():
    print("\n==== Side Effect Checker ====\n")
    
    SIDE_EFFECT_QUESTIONS = {
        "Dizziness": "Is the patient experiencing dizziness?",
        "Headache": "Is the patient experiencing a headache?",
        "Dry mouth": "Does the patient have dry mouth?",
        "Nausea": "Is the patient feeling nausea?",
        "Skin rash": "Does the patient have a skin rash?"
    }

    reported = []
    for effect, question in SIDE_EFFECT_QUESTIONS.items():
        answer = input(question + " (yes/no): ").strip().lower()
        if answer == "yes":
            reported.append(effect)

    return reported

def get_dosage_by_medicine_name(medicine_name):
    medicines = load_json("data/medicines.json")
    for med in medicines:
        if med["name"].lower() == medicine_name.lower():
            return med.get("dosage", "N/A")
    return "N/A"