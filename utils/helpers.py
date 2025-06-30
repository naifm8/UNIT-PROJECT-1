from utils.file_handler import load_json, save_json

def view_doctors():
    print("\n==== AVAILABLE DOCTORS ====\n")
    doctors = load_json('data/doctors.json')
    if not doctors:
        print("No doctors found.")
        return
    for doc in doctors:
        print(f"{doc["name"]} - {doc["specialty"]} (Available: {', '.join(doc["available_days"])})")