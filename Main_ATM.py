import random
import validation
import database
from getpass import getpass


def init():
    print("Welcome to Bank Python")

    have_account = int(input("Do you have an account with us: 1 (yes) 2 (no) \n"))

    if have_account == 1:

        login()

    elif have_account == 2:

        register()

    else:
        print("You have selected an invalid option.")
        init()


def login():
    print("*** Login ***")

    account_number_from_user = input("What is your account number? \n")

    is_valid_account_number = validation.account_number_validation(account_number_from_user)

    if is_valid_account_number:

        password = getpass("What is your password? \n")

        user = database.authenticated_user(account_number_from_user, password);

        if user:

            database.auth_session_start(account_number_from_user)
            bank_operation(user, account_number_from_user)

        print("Invalid account or password")
        login()

    else:
        print("Account number invalid. Account number must be 10 digits.")
        init()


def register():
    print("***** Register *****")

    first_name = input("What is your first name? \n")
    last_name = input("What is your last name? \n")
    email = input("What is your email address? \n")
    password = getpass("Create a password for yourself. \n")

    account_number = generate_account_number()

    is_user_created = database.create(account_number, first_name, last_name, email, password, str(0))

    if is_user_created:

        print("Your account has been created!")
        print(" ... ")
        print("Your account number is: %d" % account_number)
        print("Make sure you keep it safe!")
        print(" == ==== ===== ===== ===")

        login()

    else:
        print("Something went wrong, please try again.")
        register()


def bank_operation(user, account_number_from_user):
    print("Welcome %s %s !" % (user[0], user[1]))

    selected_option = int(input("What would you like to do? (1) Check Balance (2) Deposit (3) Withdrawal (4) Logout ("
                                "5) Exit \n"))

    if selected_option == 1:

        get_current_balance(user, account_number_from_user)
    elif selected_option == 2:

        deposit_operation(user, account_number_from_user)
    elif selected_option == 3:

        withdrawal_operation(user, account_number_from_user)
    elif selected_option == 4:

        login()
    elif selected_option == 5:

        database.auth_session_start(account_number_from_user)
        exit()
    else:

        print("Invalid option selected.")
        bank_operation()


def get_current_balance(user, account_number_from_user):
    print("Your current balance is: $%d." % int(user[4]))
    bank_operation(user, account_number_from_user)


def deposit_operation(user, account_number_from_user):
    deposit_amount = int(input("How much would you like to deposit? \n"))
    deposit_amount += int(user[4])
    set_current_balance(user, deposit_amount)

    database.update(user, account_number_from_user)
    database.auth_session_update(user, account_number_from_user)

    print("Your new balance is: $%d." % deposit_amount)
    print("Have a nice day!")
    logout()


def withdrawal_operation(user, account_number_from_user):
    withdrawal_amount = int(input("How much would you like to withdraw? \n"))

    if withdrawal_amount <= int(user[4]):
        withdrawal_amount -= user[4]
        set_current_balance(user, withdrawal_amount)

        database.update(user, account_number_from_user)
        database.auth_session_update(user, account_number_from_user)

        print("Please take your cash.")
        print("Your new balance is: $%d." % withdrawal_amount)
        logout()

    else:
        withdrawal_amount > int(user[4])
        print("Withdrawal amount exceeds account balance. Please try again.")
        bank_operation(user, account_number_from_user)


def generate_account_number():
    return random.randrange(1111111111, 9999999999)


def set_current_balance(user, balance):
    user[4] = balance


def logout():
    login()


init()
