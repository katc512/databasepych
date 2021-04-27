import os
import validation

user_db_path = "data/user_record/"
auth_session_path = "data/auth_session"


def auth_session_start(account_number_from_user):

    f = open(auth_session_path + str(account_number_from_user) + ".txt", "x")
    f.close()


def create(user_account_number, first_name, last_name, email, password):

    # create a file
    # name of the file would be account_number.txt
    # add the user details to the file
    # return True
    # if saving to file fails, the delete the created file

    user_data = first_name + "," + last_name + "," + email + "," + password + "," + str(0)

    if does_account_number_exist(user_account_number):

        return False

    if does_email_exist(email):
        print("User already exists.")
        return False

    completion_state = False

    try:

        f = open(user_db_path + str(user_account_number) + ".txt", "x")

    except FileExistsError:

        does_file_contain_data = read(user_db_path + str(user_account_number) + ".txt")

        if not does_file_contain_data:
            delete(user_account_number)

        # delete the already created file, and print out error, then return false
        # check contents of the file before deleting

    else:

        f.write(str(user_data));
        completion_state = True

    finally:

        f.close();
        return completion_state


def read(user_account_number):

    # find user with account number
    # fetch content of the file

    is_valid_account_number = validation.account_number_validation(user_account_number)

    try:
        if is_valid_account_number:
            f = open(user_db_path + str(user_account_number) + ".txt", "r")
        else:
            f = open(user_db_path + user_account_number, "r")

    except FileNotFoundError:

        print("User not found.")

    except FileExistsError:

        print("User does not exist.")

    except TypeError:

        print("Invalid account number format.")

    else:

        return f.readline()

    return False


def update(user_account_number, user):

    # find user with account number
    # fetch the content of the file
    # update the content of the file
    # save the file
    # return true

    account_balance = user[4]

    user_account_update = user[0] + "," + user[1] + "," + user[2] + "," + user[3] + "," + str(user[4])

    f = open(user_db_path + str(user_account_number) + ".txt", "w")
    f.write(user_account_update)
    f.close()


def auth_session_update(user, user_account_number):

    account_balance = user[4]

    user_account_update = user[0] + "," + user[1] + "," + user[2] + "," + user[3] + "," + str(user[4])

    f = open(auth_session_path + str(user_account_number) + ".txt", "w")
    f.write(str(user_account_update))


def delete(user_account_number):

    # find user with account number
    # delete the user record (file)
    # return true

    is_delete_successful = False

    if os.path.exists(user_db_path + str(user_account_number) + ".txt"):

        try:

            os.remove(user_db_path + str(user_account_number) + ".txt")
            is_delete_successful = True

        except FileNotFoundError:
            print("User not found.")

        finally:

            return is_delete_successful


def does_email_exist(email):

    all_users = os.listdir(user_db_path)

    for user in all_users:
        user_list = str.split(read(user), ",")
        if email in user_list:
            return True
    return False


def does_account_number_exist(account_number):

    all_users = os.listdir(user_db_path)

    for user in all_users:

        if user == str(account_number) + ".txt":

            return True

    return False


def authenticated_user(account_number, password):

    if does_account_number_exist(account_number):

        user = str.split(read(account_number), ",")

        if password == user[3]:

            return user

    return False


def auth_session_end(user_account_number):

    close_user_visit = open(auth_session_path + str(user_account_number) + ".txt", "r")
    f = close_user_visit
    f.remove(str(close_user_visit))




















