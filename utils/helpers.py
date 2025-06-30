from utils.file_handler import load_json, save_json

def view_doctors():
    print("\n==== AVAILABLE DOCTORS ====\n")
    doctors = load_json('data/doctors.json')
    if not doctors:
        print("No doctors found.")
        return
    for doc in doctors:
        print(f"{doc["name"]} - {doc["specialty"]} (Available: {', '.join(doc["available_days"])})")

def suggest_medicine_from_diagnosis(diagnosis):
    diagnosis = diagnosis.strip().lower()
    medicines = load_json("data/medicines.json")

    suggestions = []

    for med in medicines:
        if diagnosis in med.get("used_for", "").lower():
            suggestion_text = (
                f"{med['name']} ({med['type']}) - {med['dosage']}"
            )
            if med.get("prescription_required", False):
                suggestion_text += " [Prescription Required]"
            suggestions.append(suggestion_text)

    return suggestions