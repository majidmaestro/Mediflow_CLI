from __future__ import annotations

from src.persistence import StorageManager
from src.patient_manager import PatientManager
from src.auth import Authenticator


def print_header():
    print("=" * 40)
    print("   Mediflow CLI - Clinic Management")
    print("=" * 40)


def register_flow(authenticator: Authenticator):
    print("\n-- Patient Registration --")
    username = input("Username: ").strip()
    password = input("Password (min 8 chars): ").strip()
    age_input = input("Age (optional, press enter to skip): ").strip()
    contact = input("Contact (optional): ").strip() or None

    age = int(age_input) if age_input.isdigit() else None

    patient = authenticator.register_patient(
        username=username,
        password=password,
        age=age,
        contact=contact,
    )
    if patient:
        print(f"[✓] Patient '{username}' registered successfully.")
    else:
        print("[X] Registration failed.")


def login_flow(authenticator: Authenticator):
    print("\n-- Login --")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    patient = authenticator.login(username, password)
    if patient:
        print(f"[✓] Welcome back, {patient.username}!")
        return patient
    print("[X] Login failed.")
    return None


def main():
    storage = StorageManager()
    data = storage.load_data()

    patient_manager = PatientManager()
    # TODO: once PatientManager's load/hydrate method is confirmed,
    # load existing patients from `data` into patient_manager here.

    authenticator = Authenticator(patient_manager=patient_manager)

    print_header()

    while True:
        print("\n1. Register as Patient")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_flow(authenticator)
        elif choice == "2":
            logged_in_patient = login_flow(authenticator)
            if logged_in_patient:
                # TODO: show patient menu (view appointments, book, etc.)
                pass
        elif choice == "3":
            print("Saving data and exiting...")
            # TODO: confirm how patient_manager exposes all patients
            # e.g. storage.save_data({"patients": patient_manager.to_dict_all()})
            break
        else:
            print("[X] Invalid option, try again.")


if __name__ == "__main__":
    main()