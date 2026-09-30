import datetime


# Displays the main menu and gets the user's role choice.
def display_main_menu():
    print("\n--- Welcome to the Clinic Management System ---")
    print("Please select your role:")
    print("1. Receptionist")
    print("2. Doctor")
    print("3. Nurse")
    print("4. Patient")
    print("0. Exit")

    # Loop to ensure valid input.
    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 0 <= choice <= 4:
                return choice
            else:
                print("Invalid choice. Please enter a number from 0 to 4.")
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 4.")


# Reads doctor data from the 'doctors.txt' file.
def get_doctors_data():
    doctors = []
    try:
        with open("doctors.txt", 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    doctors.append({'id': parts[0], 'name': parts[1], 'availability': parts[2]})
                else:
                    print(f"Skipping malformed doctor record: {line.strip()} (Incorrect number of parts)")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"An error occurred while reading doctor data: {e}")
    return doctors


# Registers a new doctor and saves their details.
def register_new_doctor():
    doctors = get_doctors_data()
    while True:
        doctor_id = input("Enter New Doctor ID: ").strip()
        if not doctor_id.isdigit() or int(doctor_id) <= 0:
            print("Error: Doctor ID must be a positive whole number.")
            continue
        if any(d['id'] == doctor_id for d in doctors):
            print("Error: Doctor ID already exists. Please enter a unique ID.")
            continue
        break

    while True:
        doctor_name = input("Enter Doctor's Name: ").strip()
        if not doctor_name:
            print("Error: Doctor name cannot be empty.")
        elif doctor_name.isdigit():
            print("Error: Doctor name cannot be just a number. Please enter a valid name.")
        else:
            break

    availability = "not set"

    doctors.append({'id': doctor_id, 'name': doctor_name, 'availability': availability})

    try:
        with open("doctors.txt", 'w') as file:
            for d in doctors:
                file.write(f"{d['id']},{d['name']},{d['availability']}\n")
        print(f"Doctor {doctor_name} (ID: {doctor_id}) registered successfully with availability '{availability}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving doctor data: {e}")

    print("Returning to Receptionist Menu.")


# Allows the user to select a doctor from a displayed list by name.
def select_doctor_by_name_from_list():
    doctors = get_doctors_data()
    if not doctors:
        print("No doctors registered in the system.")
        return None

    while True:
        print("\n--- Select a Doctor ---")
        for i, doctor in enumerate(doctors):
            print(f"{i + 1}. {doctor['name']}")
        print("0. Cancel")

        choice_str = input("Enter the number of the doctor (or 0 to cancel): ").strip()
        if choice_str == '0':
            print("Doctor selection cancelled.")
            return None
        try:
            choice = int(choice_str)
            if 1 <= choice <= len(doctors):
                return doctors[choice - 1]['name']
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Retrieves and returns a patient's details based on their ID.
def get_patient_details_by_id():
    while True:
        patient_id_input = input("Enter Patient ID (or type 'cancel' to exit): ").strip()
        if patient_id_input.lower() == 'cancel':
            return None

        try:
            patient_id = int(patient_id_input)
            if patient_id <= 0:
                print("Error: Patient ID must be a positive number (greater than 0).")
                continue
        except ValueError:
            print("Error: Invalid ID. Please enter a whole number.")
            continue

        try:
            with open("patients.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 6 and parts[0] == patient_id_input:
                        try:
                            return {
                                'patient_id': int(parts[0]),
                                'name': parts[1],
                                'age': float(parts[2]),
                                'gender': parts[3],
                                'address': parts[4],
                                'contact_number': parts[5]
                            }
                        except ValueError:
                            print(f"Skipping malformed patient record: {line.strip()}")
                            continue
            print(f"Patient with ID {patient_id_input} not found in records. Please ensure the ID is correct.")
            continue
        except FileNotFoundError:
            print("Patient records file 'patients.txt' not found. Cannot verify patient existence.")
            return None
        except Exception as e:
            print(f"An error occurred while reading patient data: {e}")
            return None


# Registers a new patient with their personal details.
def register_new_patient():
    while True:
        patients = []
        try:
            with open("patients.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 1:
                        patients.append({'id': parts[0]})
        except FileNotFoundError:
            print("Patient records file not found. A new one will be created upon saving the first patient.")
            pass
        except Exception as e:
            print(f"An error occurred while reading existing patient data: {e}")

        while True:
            patient_id_str = input("Enter Patient ID (or type 'cancel' to exit): ").strip()
            if patient_id_str.lower() == 'cancel':
                print("Patient registration cancelled.")
                return
            try:
                patient_id = int(patient_id_str)
                if patient_id <= 0:
                    print("Error: Patient ID must be a positive number (greater than 0).")
                    continue
                if any(p['id'] == patient_id_str for p in patients):
                    print("Error: Patient ID already exists. Please enter a unique ID.")
                    continue
                break
            except ValueError:
                print("Error: Invalid ID. Please enter a whole number.")

        while True:
            name = str(input("Enter patient name: ").strip())
            if name == "":
                print("Error: Patient name cannot be empty.")
            elif name.isdigit():
                print("Error: Patient name cannot be just a number. Please enter a valid name.")
            else:
                break

        while True:
            age_str = input("Enter patient age: ").strip()
            try:
                age = float(age_str)
                if age < 0.1 or age > 200:
                    print("Error: Age must be between 0.1 and 200.")
                else:
                    break
            except ValueError:
                print("Error: Invalid age. Please enter a number (e.g., 25 or 25.5).")

        while True:
            gender = str(input("Enter patient gender (M/F): ").strip())
            if gender == "":
                print("Error: Gender cannot be empty.")
            elif gender.lower() != "m" and gender.lower() != "f":
                print("Error: Please enter 'M' or 'F'.")
            else:
                gender = gender.upper()
                break

        address = input("Enter patient address: ").strip()
        while not address:
            print("Error: Address cannot be empty.")
            address = input("Enter patient address: ").strip()

        contact_number = input("Enter patient contact number: ").strip()
        while not contact_number.isdigit() or len(contact_number) < 7:
            print("Error: Contact number must be a sequence of digits and at least 7 characters long.")
            contact_number = input("Enter patient contact number: ").strip()

        filename = "patients.txt"

        try:
            record_line = f"{patient_id},{name},{age},{gender},{address},{contact_number}\n"
            with open(filename, 'a') as file:
                file.write(record_line)
            print("Patient data saved.")
        except NameError:
            print("Error: Patient data could not be saved due to missing or invalid input. Please check the entries.")
        except Exception as e:
            print(f"An unexpected error occurred while saving the file: {e}")

        continue_input = input("\nDo you want to enter another patient? (yes/no): ").strip().lower()
        if continue_input != "yes":
            print("Returning to Receptionist Menu.")
            break


# Updates the details of an existing patient.
def update_patient_details():
    patient_to_update = get_patient_details_by_id()
    if patient_to_update is None:
        print("Update cancelled or patient not found. Returning to menu.")
        return

    patients = []
    try:
        with open("patients.txt", 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    try:
                        patients.append({
                            'patient_id': int(parts[0]),
                            'name': parts[1],
                            'age': float(parts[2]),
                            'gender': parts[3],
                            'address': parts[4],
                            'contact_number': parts[5]
                        })
                    except ValueError:
                        pass
                else:
                    print(f"Skipping malformed patient record in update: {line.strip()} (Incorrect number of parts)")
    except FileNotFoundError:
        print("No patient records found. The 'patients.txt' file does not exist yet.")
        return
    except Exception as e:
        print(f"An error occurred while reading patient data: {e}")
        return

    print("\nEnter new patient details (leave blank to keep current value):")

    new_name = input(f"Current Name: {patient_to_update['name']}, New Name: ").strip()
    if new_name:
        if new_name.isdigit():
            print("Error: Patient name cannot be just a number. Keeping current name.")
        else:
            patient_to_update['name'] = new_name

    while True:
        new_age_str = input(f"Current Age: {patient_to_update['age']}, New Age: ").strip()
        if not new_age_str:
            break
        try:
            new_age = float(new_age_str)
            if new_age < 0.1 or new_age > 200:
                print("Error: Age must be between 0.1 and 200. Keeping current age.")
            else:
                patient_to_update['age'] = new_age
                break
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 25 or 25.5). Keeping current age.")

    while True:
        new_gender = input(f"Current Gender: {patient_to_update['gender']}, New Gender (M/F): ").strip()
        if not new_gender:
            break
        if new_gender.lower() != "m" and new_gender.lower() != "f":
            print("Error: Please enter 'M' or 'F'. Keeping current gender.")
        else:
            patient_to_update['gender'] = new_gender.upper()
            break

    new_address = input(f"Current Address: {patient_to_update['address']}, New Address: ").strip()
    if new_address:
        patient_to_update['address'] = new_address

    while True:
        new_contact_number = input(
            f"Current Contact Number: {patient_to_update['contact_number']}, New Contact Number: ").strip()
        if not new_contact_number:
            break
        if not new_contact_number.isdigit() or len(new_contact_number) < 7:
            print(
                "Error: Contact number must be a sequence of digits and at least 7 characters long. Keeping current contact number.")
        else:
            patient_to_update['contact_number'] = new_contact_number
            break

    try:
        with open("patients.txt", 'w') as file:
            for patient in patients:
                if patient['patient_id'] == patient_to_update['patient_id']:
                    file.write(
                        f"{patient_to_update['patient_id']},{patient_to_update['name']},{patient_to_update['age']},{patient_to_update['gender']},{patient_to_update['address']},{patient_to_update['contact_number']}\n")
                else:
                    file.write(
                        f"{patient['patient_id']},{patient['name']},{patient['age']},{patient['gender']},{patient['address']},{patient['contact_number']}\n")
        print("Patient details updated successfully!")
    except Exception as e:
        print(f"Error saving updated patient details: {e}")


# Schedules an appointment for a patient with a selected doctor.
def schedule_appointment():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Appointment scheduling cancelled or patient not found. Returning to Receptionist Menu.")
        return

    patient_id = patient_info['patient_id']

    while True:
        appt_date_str = input("Enter Appointment Date (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(appt_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD (e.g., 2025-01-15).")

    while True:
        appt_time_str = input("Enter Appointment Time (HH:MM): ").strip()
        try:
            datetime.datetime.strptime(appt_time_str, "%H:%M")
            break
        except ValueError:
            print("Error: Invalid time format. Please use HH:MM (e.g., 09:00 or 14:30).")

    doctor_name = select_doctor_by_name_from_list()
    if doctor_name is None:
        print("Appointment scheduling cancelled due to doctor selection.")
        print("Returning to Receptionist Menu.")
        return

    try:
        record_line = f"{patient_id},{appt_date_str},{appt_time_str},{doctor_name}\n"
        with open("appointments.txt", 'a') as file:
            file.write(record_line)
        print("Appointment scheduled successfully!")
    except Exception as e:
        print(f"An unexpected error occurred while scheduling the appointment: {e}")

    print("Returning to Receptionist Menu.")


# Processes a payment for a patient, including amount and method.
def process_payment():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Payment processing cancelled or patient not found. Returning to Receptionist Menu.")
        return

    patient_id = patient_info['patient_id']

    while True:
        amount_str = input("Enter Amount Due: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Error: Amount must be a positive number (greater than 0).")
            else:
                break
        except ValueError:
            print("Error: Invalid amount. Please enter a number (e.g., 150.00).")

    print("\nSelect Payment Method:")
    print("1. Cash")
    print("2. Card")
    print("3. Insurance")
    while True:
        method_choice = input("Enter your choice (1-3): ").strip()
        if method_choice == '1':
            payment_method = "Cash"
            break
        elif method_choice == '2':
            payment_method = "Card"
            break
        elif method_choice == '3':
            payment_method = "Insurance"
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    payment_date = datetime.date.today().strftime("%Y-%m-%d")

    filename = "payments.txt"

    try:
        record_line = f"{patient_id},{amount},{payment_method},{payment_date}\n"
        with open(filename, 'a') as file:
            file.write(record_line)
        print("Payment processed successfully!")
    except Exception as e:
        print(f"An unexpected error occurred while processing payment: {e}")

    print("Returning to Receptionist Menu.")


# Helper function to delete records matching an ID from a specified file.
def _delete_records_from_file(filename, id_to_delete):
    records = []
    found_file = True
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts and parts[0] == id_to_delete:
                    continue
                records.append(line.strip())
    except FileNotFoundError:
        found_file = False
        print(f"Warning: File '{filename}' not found for deletion. Skipping.")
        return True
    except Exception as e:
        print(f"Error reading '{filename}' during deletion: {e}")
        return False

    if not found_file and not records:
        return True

    try:
        with open(filename, 'w') as file:
            for record_line in records:
                file.write(f"{record_line}\n")
        print(f"Records successfully processed for '{filename}'.")
        return True
    except Exception as e:
        print(f"Error writing to '{filename}' after deletion: {e}")
        return False


# Deletes all associated data for a specific patient across multiple files.
def delete_patient_data():
    patient_info = get_patient_details_by_id()

    if patient_info is None:
        print("Deletion cancelled or patient not found. Returning to menu.")
        return

    patient_id_to_delete = str(patient_info['patient_id'])
    print(f"\n--- Patient Found: {patient_info['name']} (ID: {patient_id_to_delete}) ---")

    while True:
        confirm_delete = input(f"Do you want to delete ALL data about Patient ID {patient_id_to_delete} ({patient_info['name']})? (yes/no): ").strip().lower()
        if confirm_delete == 'yes':
            print(f"Proceeding with deletion for Patient ID {patient_id_to_delete}...")

            files_to_update = [
                "patients.txt",
                "appointments.txt",
                "medical_history.txt",
                "payments.txt",
                "observations.txt",
                "medicine_log.txt"
            ]

            all_deleted_successfully = True
            for filename in files_to_update:
                if not _delete_records_from_file(filename, patient_id_to_delete):
                    all_deleted_successfully = False

            if all_deleted_successfully:
                print(f"Patient ID {patient_id_to_delete} and all related records have been conceptually removed.")
            else:
                print(f"Deletion for Patient ID {patient_id_to_delete} completed with some issues. Check logs.")
            break
        elif confirm_delete == 'no':
            print("Deletion cancelled. Returning to menu.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# Displays the receptionist menu and handles their actions.
def receptionist_menu():
    print("\n--- Receptionist Menu ---")
    print("1. Register new patient")
    print("2. Update patient details")
    print("3. Schedule appointment")
    print("4. Process payment")
    print("5. Register new doctor")
    print("6. Delete patient records")
    print("0. Go back to Main Menu")

    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 0 <= choice <= 6:
                if choice == 1:
                    register_new_patient()
                elif choice == 2:
                    update_patient_details()
                elif choice == 3:
                    schedule_appointment()
                elif choice == 4:
                    process_payment()
                elif choice == 5:
                    register_new_doctor()
                elif choice == 6:
                    delete_patient_data()
                elif choice == 0:
                    break
            else:
                print("Invalid choice. Please enter a number from 0 to 6.")
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 6.")


# Allows a doctor to view a patient's medical history.
def view_medical_history():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting medical history viewer.")
        return

    patient_id_to_view = str(patient_info['patient_id'])

    print("\n--- Patient Details ---")
    print(f"ID: {patient_info['patient_id']}")
    print(f"Name: {patient_info['name']}")
    print(f"Age: {patient_info['age']}")
    print(f"Gender: {patient_info['gender']}")
    print(f"Address: {patient_info['address']}")
    print(f"Contact Number: {patient_info['contact_number']}")

    history_found = False
    print("\n--- Medical History & Treatment Logs ---")
    try:
        with open("medical_history.txt", "r") as history_file:
            for line in history_file:
                history_details = line.strip().split(',')
                if len(history_details) == 5 and history_details[0] == patient_id_to_view:
                    history_found = True
                    print(
                        f"  Date: {history_details[1]}, Diagnosis: {history_details[2]}, Treatment: {history_details[3]}, Doctor: {history_details[4]}"
                    )
            if not history_found:
                print(f"  No medical records found for Patient ID {patient_id_to_view}.")

    except FileNotFoundError:
        print("  Medical history file 'medical_history.txt' not found. No records to display.")
    except Exception:
        print("  An error occurred while reading medical history records.")

    while True:
        another_view = input("\nView another patient's medical history? (yes/no): ").strip().lower()
        if another_view != 'yes':
            print("Returning to Doctor Menu.")
            break
        else:
            return view_medical_history()


# Allows a doctor to update a patient's medical records with diagnosis and treatment.
def update_patient_records():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting medical record update.")
        return

    patient_id = patient_info['patient_id']
    doctor_id = None

    doctors = get_doctors_data()
    if not doctors:
        print("No doctors registered. Cannot update records.")
        return

    selected_doctor_name = None
    while True:
        input_doctor_id = input("Enter your Doctor ID to update records (or type 'cancel' to exit): ").strip()
        if input_doctor_id.lower() == 'cancel':
            print("Medical record update cancelled due to doctor ID selection.")
            return

        found_doctor = False
        for doctor in doctors:
            if doctor['id'] == input_doctor_id:
                doctor_id = input_doctor_id
                selected_doctor_name = doctor['name']
                found_doctor = True
                break

        if found_doctor:
            break
        else:
            print("Doctor ID not found. Please enter a valid ID.")

    print(f"\n--- Patient Found: {patient_info['name']} (ID: {patient_info['patient_id']}) ---")
    print(f"Doctor: {selected_doctor_name} (ID: {doctor_id}) is updating records.")

    while True:
        record_date_str = input("Enter Date of Record (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(record_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD (e.g., 2025-01-15).")

    while True:
        diagnosis = input("Enter Diagnosis: ").strip()
        if not diagnosis:
            print("Error: Diagnosis cannot be empty.")
        else:
            break

    while True:
        treatment = input("Enter Treatment: ").strip()
        if not treatment:
            print("Error: Treatment cannot be empty.")
        else:
            break

    filename = "medical_history.txt"
    try:
        record_line = f"{patient_id},{record_date_str},{diagnosis},{treatment},{selected_doctor_name}\n"
        with open(filename, 'a') as file:
            file.write(record_line)
        print("Medical record updated successfully!")
    except Exception:
        print("An unexpected error occurred while saving the medical record.")

    while True:
        add_another = input("\nAdd another medical record for a patient? (yes/no): ").strip().lower()
        if add_another != 'yes':
            print("Returning to Doctor Menu.")
            break
        else:
            return update_patient_records()


# Allows a doctor to view their scheduled appointments.
def view_own_appointment_list():
    doctors = get_doctors_data()
    if not doctors:
        print("No doctors registered in the system.")
        return

    selected_doctor_name = None
    while True:
        input_doctor_id = input("Enter your Doctor ID to view appointments (or type 'cancel' to exit): ").strip()
        if input_doctor_id.lower() == 'cancel':
            print("Exiting appointment viewer.")
            return

        found_doctor = False
        for doctor in doctors:
            if doctor['id'] == input_doctor_id:
                selected_doctor_name = doctor['name']
                found_doctor = True
                break

        if found_doctor:
            break
        else:
            print("Doctor ID not found. Please enter a valid ID.")

    print(f"\n--- Appointments for {'Dr. ' + selected_doctor_name.title()} ---")
    found_appointments_for_doctor = False

    try:
        with open("appointments.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')

                if len(parts) == 4:
                    if parts[3].lower() == selected_doctor_name.lower():
                        found_appointments_for_doctor = True
                        print(f"  Patient ID: {parts[0]}, Date: {parts[1]}, Time: {parts[2]}")

        if not found_appointments_for_doctor:
            print(f"  No appointments found for {'Dr. ' + selected_doctor_name.title()}.")

    except FileNotFoundError:
        print("No appointment records found. The 'appointments.txt' file does not exist yet.")
    except Exception:
        print("An error occurred while attempting to read appointment records.")

    while True:
        another_view = input("\nView another doctor's appointment list? (yes/no): ").strip().lower()
        if another_view != 'yes':
            print("Returning to Doctor Menu.")
            break
        else:
            return view_own_appointment_list()


# Allows a doctor to set their availability status (available/unavailable).
def block_unblock_availability():
    doctors = get_doctors_data()
    if not doctors:
        print("No doctors registered in the system to manage availability.")
        return

    selected_doctor_id = None
    display_doctor_name = ""
    current_status_from_file = ""
    while True:
        input_id = input("Enter your Doctor ID to manage availability (or type 'cancel' to exit): ").strip()
        if input_id.lower() == 'cancel':
            print("Availability management cancelled.")
            return

        found_doctor = False
        for doctor in doctors:
            if doctor['id'] == input_id:
                selected_doctor_id = input_id
                display_doctor_name = doctor['name']
                current_status_from_file = doctor['availability']
                found_doctor = True
                break

        if found_doctor:
            break
        else:
            print("Doctor ID not found. Please enter a valid ID.")

    print(f"\n--- Manage Availability for {display_doctor_name} (ID: {selected_doctor_id}) ---")
    print(f"Current status: {current_status_from_file.title()}")

    print("\nSelect an option:")
    print("1. Set to Available")
    print("2. Set to Unavailable")
    print("0. Keep current status and Exit")

    new_status = current_status_from_file

    while True:
        choice_str = input("Enter your choice (0-2): ").strip()
        if choice_str == '0':
            print(f"{display_doctor_name}'s status remains unchanged. Exiting.")
            return
        try:
            choice = int(choice_str)
            if choice == 1:
                new_status = "available"
                break
            elif choice == 2:
                new_status = "unavailable"
                break
            else:
                print("Invalid choice. Please enter 1 for Available, 2 for Unavailable, or 0 to exit.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    updated = False
    for i, record in enumerate(doctors):
        if record['id'] == selected_doctor_id:
            doctors[i]['availability'] = new_status
            updated = True
            break

    try:
        with open("doctors.txt", "w") as file:
            for record in doctors:
                file.write(f"{record['id']},{record['name']},{record['availability']}\n")
        print(f"{display_doctor_name}'s availability successfully updated to {new_status.title()}!")
    except Exception:
        print("An error occurred while saving doctor availability.")

    another_manage = input("\nManage another doctor's availability? (yes/no): ").strip().lower()
    if another_manage != 'yes':
        print("Returning to Doctor Menu.")
        return


# Displays the doctor menu and handles their actions.
def doctor_menu():
    print("\n--- Doctor Menu ---")
    print("1. View medical history and treatment logs")
    print("2. Update patient records")
    print("3. View own appointment list")
    print("4. Block/unblock availability")
    print("0. Go back to Main Menu")

    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 0 <= choice <= 4:
                if choice == 1:
                    view_medical_history()
                elif choice == 2:
                    update_patient_records()
                elif choice == 3:
                    view_own_appointment_list()
                elif choice == 4:
                    block_unblock_availability()
                elif choice == 0:
                    break
            else:
                print("Invalid choice. Please enter a number from 0 to 4.")
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 4.")


# Allows a nurse to view a doctor's appointment list.
def view_doctors_appointment_list():
    while True:
        doctor_name_input = select_doctor_by_name_from_list()
        if doctor_name_input is None:
            print("Exiting doctor's appointment viewer.")
            break

        print(f"\n--- Appointments for {'Dr. ' + doctor_name_input.title()} ---")
        found_appointments_for_doctor = False

        try:
            with open("appointments.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')

                    if len(parts) == 4:
                        if parts[3].lower() == doctor_name_input.lower():
                            found_appointments_for_doctor = True
                            print(f"  Patient ID: {parts[0]}, Date: {parts[1]}, Time: {parts[2]}")

            if not found_appointments_for_doctor:
                print(f"  No appointments found for {'Dr. ' + doctor_name_input.title()}.")

        except FileNotFoundError:
            print("No appointment records found. The 'appointments.txt' file does not exist yet.")
        except Exception:
            print("An error occurred while attempting to read appointment records.")

        another_view = input("\nView another doctor's appointment list? (yes/no): ").strip().lower()
        if another_view != 'yes':
            print("Returning to Nurse Menu.")
            break


# Records a patient's observations like blood pressure, pulse, and temperature.
def record_patients_observations():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting patient observations recorder.")
        return

    patient_id = patient_info['patient_id']
    print(f"\n--- Recording observations for {patient_info['name']} (ID: {patient_info['patient_id']}) ---")

    temperature = 0.0
    while True:
        blood_pressure = input("Enter Blood Pressure (e.g., 120/80): ").strip()
        if not blood_pressure:
            print("Error: Blood Pressure cannot be empty.")
        else:
            break

    while True:
        pulse_str = input("Enter Pulse Rate (beats/min): ").strip()
        try:
            pulse = int(pulse_str)
            if pulse <= 0 or pulse > 300:
                print("Error: Pulse rate must be a positive number, typically between 1 and 300.")
            else:
                break
        except ValueError:
            print("Error: Invalid pulse rate. Please enter a whole number.")

    while True:
        temperature_str = input("Enter Temperature (°C): ").strip()
        if not temperature_str:
            print("Error: Temperature cannot be empty.")
            continue
        try:
            temperature = float(temperature_str)
            if temperature < 20 or temperature > 45:
                print("Warning: Temperature seems outside typical human range (e.g., 36.5-37.5°C).")
            break
        except ValueError:
            print("Error: Invalid temperature. Please enter a number (e.g., 37.5).")

    observation_date = datetime.date.today().strftime("%Y-%m-%d")

    filename = "observations.txt"
    try:
        record_line = f"{patient_id},{observation_date},{blood_pressure},{pulse},{temperature}\n"
        with open(filename, 'a') as file:
            file.write(record_line)
        print("Patient observations recorded successfully!")
    except Exception:
        print("An unexpected error occurred while saving the observations.")

    while True:
        add_another = input("\nRecord observations for another patient? (yes/no): ").strip().lower()
        if add_another != 'yes':
            print("Returning to Nurse Menu.")
            break
        else:
            return record_patients_observations()


# Allows a nurse to view a patient's prescriptions (from medical history).
def view_doctors_prescriptions():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting doctor's prescriptions viewer.")
        return

    patient_id_to_view = str(patient_info['patient_id'])
    print(f"\n--- Prescriptions for {patient_info['name']} (ID: {patient_info['patient_id']}) ---")

    prescriptions_found = False
    try:
        with open("medical_history.txt", "r") as history_file:
            for line in history_file:
                history_details = line.strip().split(',')
                if len(history_details) == 5 and history_details[0] == patient_id_to_view:
                    prescriptions_found = True
                    print(
                        f"  Date: {history_details[1]}, Diagnosis: {history_details[2]}, Treatment: {history_details[3]}"
                    )
        if not prescriptions_found:
            print(f"  No prescriptions found for Patient ID {patient_id_to_view}.")
    except FileNotFoundError:
        print("  Medical history file 'medical_history.txt' not found. No prescriptions to display.")
    except Exception:
        print("  An error occurred while reading medical history records.")

    while True:
        add_another = input("\nView prescriptions for another patient? (yes/no): ").strip().lower()
        if add_another != 'yes':
            print("Returning to Nurse Menu.")
            break
        else:
            return view_doctors_prescriptions()


# Administers medicine to a patient and logs the details.
def administer_medicine():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting medicine administration.")
        return

    patient_id = patient_info['patient_id']
    print(f"\n--- Administering medicine for {patient_info['name']} (ID: {patient_info['patient_id']}) ---")

    while True:
        medicine_name = input("Enter Medicine Name: ").strip()
        if not medicine_name:
            print("Error: Medicine Name cannot be empty.")
        else:
            break

    while True:
        dosage = input("Enter Dosage (e.g., '500mg', '1 tablet'): ").strip()
        if not dosage:
            print("Error: Dosage cannot be empty.")
        else:
            break

    while True:
        nurse_name = input("Enter Administering Nurse's Name: ").strip()
        if not nurse_name:
            print("Error: Nurse's Name cannot be empty.")
        else:
            break

    administration_date = datetime.date.today().strftime("%Y-%m-%d")

    filename = "medicine_log.txt"
    try:
        record_line = f"{patient_id},{administration_date},{medicine_name},{dosage},{nurse_name}\n"
        with open(filename, 'a') as file:
            file.write(record_line)
        print("Medicine administered and recorded successfully!")
    except Exception:
        print("An unexpected error occurred while saving the medicine administration record.")

    while True:
        print_receipt_choice = input(
            "Do you want to print a receipt for this administration? (yes/no): ").strip().lower()
        if print_receipt_choice == 'yes':
            print("\n--- Medicine Administration Receipt ---")
            print(f"Patient ID: {patient_id}")
            print(f"Date: {administration_date}")
            print(f"Medicine: {medicine_name}")
            print(f"Dosage: {dosage}")
            print(f"Administered by Nurse: {nurse_name}")
            print("-------------------------------------")
            break
        elif print_receipt_choice == 'no':
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

    while True:
        add_another = input("\nAdminister medicine for another patient? (yes/no): ").strip().lower()
        if add_another != 'yes':
            print("Returning to Nurse Menu.")
            break
        else:
            return administer_medicine()


# Displays the nurse menu and handles their actions.
def nurse_menu():
    print("\n--- Nurse Menu ---")
    print("1. View doctor's appointment list")
    print("2. Record patients' observations")
    print("3. View doctor's prescriptions")
    print("4. Administer medicine")
    print("0. Go back to Main Menu")

    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 0 <= choice <= 4:
                if choice == 1:
                    view_doctors_appointment_list()
                elif choice == 2:
                    record_patients_observations()
                elif choice == 3:
                    view_doctors_prescriptions()
                elif choice == 4:
                    administer_medicine()
                elif choice == 0:
                    break
            else:
                print("Invalid choice. Please enter a number from 0 to 4.")
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 4.")


# Allows a patient to access their personal medical records.
def access_personal_medical_records():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting personal medical records access. Returning to Patient Menu.")
        return

    patient_id_to_view = str(patient_info['patient_id'])

    print(f"\n--- Medical Records for {patient_info['name']} (ID: {patient_info['patient_id']}) ---")
    print(f"Address: {patient_info['address']}")
    print(f"Contact Number: {patient_info['contact_number']}")

    records_found = False
    try:
        with open("medical_history.txt", "r") as history_file:
            for line in history_file:
                history_details = line.strip().split(',')
                if len(history_details) == 5 and history_details[0] == patient_id_to_view:
                    records_found = True
                    print(
                        f"  Date: {history_details[1]}, Diagnosis: {history_details[2]}, Treatment: {history_details[3]}, Doctor: {history_details[4]}"
                    )
            if not records_found:
                print(f"  No medical records found for Patient ID {patient_id_to_view}.")
    except FileNotFoundError:
        print("  Medical history file 'medical_history.txt' not found. No records to display.")
    except Exception:
        print("  An error occurred while reading medical history records.")

    while True:
        return_choice_str = input("\nEnter 0 to return to Patient Menu: ").strip()
        if return_choice_str == '0':
            print("Returning to Patient Menu.")
            break
        else:
            print("Invalid input. Please enter 0 to return.")


# Allows a patient to view their upcoming appointments.
def view_upcoming_appointments():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting upcoming appointments viewer. Returning to Patient Menu.")
        return

    patient_id_to_view = str(patient_info['patient_id'])

    print(f"\n--- Upcoming Appointments for {patient_info['name']} (ID: {patient_info['patient_id']}) ---")
    print(f"Address: {patient_info['address']}")
    print(f"Contact Number: {patient_info['contact_number']}")

    appointments_found = False
    current_date = datetime.date.today()
    try:
        with open("appointments.txt", "r") as appt_file:
            for line in appt_file:
                appt_details = line.strip().split(',')
                if len(appt_details) == 4 and appt_details[0] == patient_id_to_view:
                    appointment_date_str = appt_details[1]
                    appointment_date = datetime.datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
                    if appointment_date >= current_date:
                        appointments_found = True
                        print(
                            f"  Date: {appt_details[1]}, Time: {appt_details[2]}, Doctor: {appt_details[3]}"
                        )
        if not appointments_found:
            print(f"  No upcoming appointments found for Patient ID {patient_id_to_view}.")
    except FileNotFoundError:
        print("  Appointment records file 'appointments.txt' not found. No appointments to display.")
    except Exception:
        print("  An error occurred while reading appointment records.")

    while True:
        return_choice_str = input("\nEnter 0 to return to Patient Menu: ").strip()
        if return_choice_str == '0':
            print("Returning to Patient Menu.")
            break
        else:
            print("Invalid input. Please enter 0 to return.")


# Allows a patient to update their personal information.
def update_personal_information():
    patient_to_update = get_patient_details_by_id()
    if patient_to_update is None:
        print("Update cancelled or patient not found. Returning to Patient Menu.")
        return

    patients = []
    try:
        with open("patients.txt", 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    try:
                        patients.append({
                            'patient_id': int(parts[0]),
                            'name': parts[1],
                            'age': float(parts[2]),
                            'gender': parts[3],
                            'address': parts[4],
                            'contact_number': parts[5]
                        })
                    except ValueError:
                        pass
                else:
                    print(f"Skipping malformed patient record in update: {line.strip()} (Incorrect number of parts)")
    except FileNotFoundError:
        print("No patient records found. The 'patients.txt' file does not exist yet.")
        print("\nReturning to Patient Menu.")
        return
    except Exception as e:
        print(f"An error occurred while reading patient data: {e}")
        print("\nReturning to Patient Menu.")
        return

    print("\nEnter new personal details (leave blank to keep current value):")

    new_name = input(f"Current Name: {patient_to_update['name']}, New Name: ").strip()
    if new_name:
        if new_name.isdigit():
            print("Error: Patient name cannot be just a number. Keeping current name.")
        else:
            patient_to_update['name'] = new_name

    while True:
        new_age_str = input(f"Current Age: {patient_to_update['age']}, New Age: ").strip()
        if not new_age_str:
            break
        try:
            new_age = float(new_age_str)
            if new_age < 0.1 or new_age > 200:
                print("Error: Age must be between 0.1 and 200. Keeping current age.")
            else:
                patient_to_update['age'] = new_age
                break
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 25 or 25.5). Keeping current age.")

    while True:
        new_gender = input(f"Current Gender: {patient_to_update['gender']}, New Gender (M/F): ").strip()
        if not new_gender:
            break
        if new_gender.lower() != "m" and new_gender.lower() != "f":
            print("Error: Please enter 'M' or 'F'. Keeping current gender.")
        else:
            patient_to_update['gender'] = new_gender.upper()
            break

    new_address = input(f"Current Address: {patient_to_update['address']}, New Address: ").strip()
    if new_address:
        patient_to_update['address'] = new_address

    while True:
        new_contact_number = input(
            f"Current Contact Number: {patient_to_update['contact_number']}, New Contact Number: ").strip()
        if not new_contact_number:
            break
        if not new_contact_number.isdigit() or len(new_contact_number) < 7:
            print(
                "Error: Contact number must be a sequence of digits and at least 7 characters long. Keeping current contact number.")
        else:
            patient_to_update['contact_number'] = new_contact_number
            break

    try:
        with open("patients.txt", 'w') as file:
            for patient in patients:
                if patient['patient_id'] == patient_to_update['patient_id']:
                    file.write(
                        f"{patient_to_update['patient_id']},{patient_to_update['name']},{patient_to_update['age']},{patient_to_update['gender']},{patient_to_update['address']},{patient_to_update['contact_number']}\n")
                else:
                    file.write(
                        f"{patient['patient_id']},{patient['name']},{patient['age']},{patient['gender']},{patient['address']},{patient['contact_number']}\n")
        print("Your personal details updated successfully!")
    except Exception as e:
        print(f"Error saving updated personal details: {e}")

    while True:
        return_choice_str = input("\nEnter 0 to return to Patient Menu: ").strip()
        if return_choice_str == '0':
            print("Returning to Patient Menu.")
            break
        else:
            print("Invalid input. Please enter 0 to return.")


# Allows a patient to access their billing details.
def access_billing_details():
    patient_info = get_patient_details_by_id()
    if patient_info is None:
        print("Exiting billing details access. Returning to Patient Menu.")
        return

    patient_id_to_view = str(patient_info['patient_id'])

    print(f"\n--- Billing Details for {patient_info['name']} (ID: {patient_info['patient_id']}) ---")
    print(f"Address: {patient_info['address']}")
    print(f"Contact Number: {patient_info['contact_number']}")

    billing_records_found = False
    try:
        with open("payments.txt", "r") as payments_file:
            for line in payments_file:
                payment_details = line.strip().split(',')
                if len(payment_details) == 4 and payment_details[0] == patient_id_to_view:
                    billing_records_found = True
                    print(
                        f"  Amount Due: {payment_details[1]}, Method: {payment_details[2]}, Date: {payment_details[3]}"
                    )
        if not billing_records_found:
            print(f"  No billing records found for Patient ID {patient_id_to_view}.")
    except FileNotFoundError:
        print("  Payment records file 'payments.txt' not found. No records to display.")
    except Exception:
        print("  An error occurred while reading payment records.")

    while True:
        return_choice_str = input("\nEnter 0 to return to Patient Menu: ").strip()
        if return_choice_str == '0':
            print("Returning to Patient Menu.")
            break
        else:
            print("Invalid input. Please enter 0 to return.")


# Displays the patient menu and handles their actions.
def patient_menu():
    print("\n--- Patient Menu ---")
    print("1. Access personal medical records")
    print("2. View upcoming appointments")
    print("3. Update personal information")
    print("4. Access billing details")
    print("0. Go back to Main Menu")

    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 0 <= choice <= 4:
                if choice == 1:
                    access_personal_medical_records()
                elif choice == 2:
                    view_upcoming_appointments()
                elif choice == 3:
                    update_personal_information()
                elif choice == 4:
                    access_billing_details()
                elif choice == 0:
                    break
            else:
                print("Invalid choice. Please enter a number from 0 to 4.")
        except ValueError:
            print("Invalid input. Please enter a number from 0 to 4.")


while True:
    user_choice = display_main_menu()

    if user_choice == 1:
        receptionist_menu()
    elif user_choice == 2:
        doctor_menu()
    elif user_choice == 3:
        nurse_menu()
    elif user_choice == 4:
        patient_menu()
    elif user_choice == 0:
        print("Exiting Clinic Management System. Goodbye!")
        break