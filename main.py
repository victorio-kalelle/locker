import os
import json
import secrets
import string

EXIT_OPTION = 6
FILE_NAME = "users.txt"

def display_menu():
    print("================[Locker]================")
    print("[1] Add account (email & password)")
    print("[2] Search for account")
    print("[3] Delete account from list")
    print("[4] Generate a new secure password")
    print("[5] View all saved accounts")
    print("[6] Exit")

def process_choice(choice):
    match choice:
        case 1:
            print("-----[Add account/email & password]-----")
            add_account()
        case 2:
            print("-----[Search for account]-----")
            search_account()
        case 3:
            print("-----[Delete account from list]-----")
            delete_account()
        case 4:
            print("-----[Generate a new secure password]-----")
            generate_password()
        case 5:
            print("-----[View all saved accounts]-----")
            view_accounts()
        case 6:
            print("Exiting...")
            return
        case _:
            print("Invalid choice, please try again...")
    input("\nPress enter to continue...")

def get_user_choice():
    try:
        return int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input, please enter a number.")
        return None
    
def menu():
    while True:
        display_menu()
        choice = get_user_choice()

        if choice is None:
            input("Press enter to continue...")
            continue

        if choice == EXIT_OPTION:
            break

        process_choice(choice)

def load_accounts():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_accounts(accounts):
    with open(FILE_NAME, "w") as f:
        json.dump(accounts, f, indent=4)

def add_account():
    user = input("Enter email/username: ")
    password = input("Enter password (or leave blank to generate one): ")
    
    if not password:
        password = generate_password(return_only=True)
        print(f"Generated password: {password}")

    extra = {}
    while True:
        answer = input("Do you want to add more information? (Y/N): ").upper()
        if answer == "Y":
            extra.update(additional_information())
        elif answer == "N":
            break
        else:
            print("Please enter Y or N")

    account = {"email": user, "password": password, **extra}
    accounts = load_accounts()
    accounts.append(account)
    save_accounts(accounts)
    print("Your information is saved...")

def additional_information():
    print("-----[Additional Information]-----")
    print("[1] Username")
    print("[2] Extra password")
    print("[3] Others...")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid choice")
        return {}

    if choice == 1:
        username = input("Enter username: ")
        return {"username": username}
    elif choice == 2:
        new_pass = input("Enter extra password: ")
        return {"extra_password": new_pass}
    elif choice == 3:
        note = input("Enter other info: ")
        return {"others": note}
    else:
        print("Invalid option.")
        return {}

def view_accounts():
    accounts = load_accounts()
    if not accounts:
        print("No accounts saved yet.")
    else:
        for i, acc in enumerate(accounts, start=1):
            print(f"{i}. {acc}")

def search_account():
    accounts = load_accounts()
    if not accounts:
        print("No accounts saved yet.")
        return
    keyword = input("Enter email/username to search: ").lower()
    results = [acc for acc in accounts if keyword in acc.get("email", "")
               .lower()]
    if results:
        for i, acc in enumerate(results, start=1):
            print(f"{i}. {acc}")
    else:
        print("No matching account found.")

def delete_account():
    accounts = load_accounts()
    if not accounts:
        print("No accounts saved yet.")
        return
    view_accounts()
    try:
        index = int(input("Enter account number to delete: "))
        if 1 <= index <= len(accounts):
            deleted = accounts.pop(index - 1)
            save_accounts(accounts)
            print(f"Deleted: {deleted}")
        else:
            print("Invalid account number.")
    except ValueError:
        print("Please enter a valid number.")

def generate_password(length=12, return_only=False):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    if return_only:
        return password
    print(f"Generated password: {password}")

menu()