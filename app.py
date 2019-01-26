import csv
import os
import re
import sys

from collections import OrderedDict
from datetime import datetime, timedelta


def show_main_menu():
    """Show main menu and get user's input"""
    while True:
        user_input = None
        while not isinstance(user_input, int):
            reset_screen("work log", "what would you like to do?")
            for num, option in MAIN_MENU.items():
                print(f"{num}) {option.__doc__.title()}")
            user_input = get_input(int)
        if user_input in MAIN_MENU:
            MAIN_MENU[user_input]()
        else:
            user_input = not_in_menu()


def add_entry():
    """Add new entry"""
    entry = {}
    date_keys = ["Date"]
    int_keys = ["Time Spent"]
    optional_keys = ["Notes"]
    for key, question in ENTRY_QUESTIONS.items():
        if key in date_keys:
            input_type = datetime
        elif key in int_keys:
            input_type = int
        else:
            input_type = str
        while True:
            reset_screen(MAIN_MENU[1].__doc__, question)
            user_input = get_input(input_type, newline=False)
            if user_input or key in optional_keys:
                entry[key] = user_input
                break
    write_to_csv(entry)
    reset_screen("entry has been added successfully.", confirm=True)


def write_to_csv(entry):
    """Write entry data to csv file"""
    header = []
    for key in entry:
        header.append(key)
    with open("entries.csv", "a", newline="") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=header)
        if csvfile.tell() == 0:
            csvwriter.writeheader()
        csvwriter.writerow(entry)


def show_search_options():
    """View existing entries"""
    user_input = None
    quit = (len(SEARCH_MENU) + 1)
    while user_input != quit:
        while not isinstance(user_input, int):
            reset_screen(MAIN_MENU[2].__doc__, "Please select an option:")
            for num, option in SEARCH_MENU.items():
                print(f"{num}) {option.__doc__}")
            print_return_to_main(quit)
            user_input = get_input(int)
        if user_input in SEARCH_MENU:
            return SEARCH_MENU[user_input]()
        elif user_input != quit:
            user_input = not_in_menu()


def search_exact_date():
    """By exact date"""
    user_input = None
    results = []
    entries = get_entries()
    dates_set = set()
    for entry in entries:
        dates_set.add(entry["Date"])
    dates = list(sorted(dates_set, key=lambda x: datetime.strptime(x, D_FORM)))
    dates.sort(reverse=True)
    quit = (len(dates) + 1)
    while user_input != quit:
        while not isinstance(user_input, int):
            reset_screen(SEARCH_MENU[1].__doc__, "Please select a date:")
            for index, date in enumerate(dates, 1):
                print(f"{index}) {date}")
            print_return_to_main(quit)
            user_input = get_input(int)
        if user_input in range(1, (len(dates) + 1)):
            for entry in entries:
                if dates[user_input - 1] == entry["Date"]:
                    results.append(entry)
            return view_results(results)
        elif user_input != quit:
            user_input = not_in_menu()


def search_date_range():
    """By date range"""
    entries = get_entries()
    beg_date = None
    end_date = None
    dates = []
    results = []
    while not beg_date:
        reset_screen(SEARCH_MENU[2].__doc__, "Begin date (mm/dd/yyyy):")
        beg_date = get_input(datetime, newline=False)
    while not end_date:
        reset_screen(SEARCH_MENU[2].__doc__, "End date (mm/dd/yyyy):")
        end_date = get_input(datetime, newline=False)
    beg_date = datetime.strptime(beg_date, D_FORM)
    end_date = datetime.strptime(end_date, D_FORM)
    date_range = end_date - beg_date
    for day in range(date_range.days + 1):
        dates.append(datetime.strftime(beg_date + timedelta(day), D_FORM))
    for entry in entries:
        for date in dates:
            if date == entry["Date"]:
                results.append(entry)
    return view_results(results)


def search_time_spent():
    """By time spent"""
    user_input = None
    results = []
    entries = get_entries()
    times_set = set()
    for entry in entries:
        times_set.add(int(entry["Time Spent"]))
    times = list(sorted(times_set))
    times.sort(reverse=True)
    quit = (len(times) + 1)
    while user_input != quit:
        while not isinstance(user_input, int):
            reset_screen(SEARCH_MENU[3].__doc__, "Please select a time:")
            for index, time in enumerate(times, 1):
                print(f"{index} {time}")
            print_return_to_main(quit)
            user_input = get_input(int)
        if user_input in range(1, len(times) + 1):
            for entry in entries:
                if times[user_input - 1] == int(entry["Time Spent"]):
                    results.append(entry)
            return view_results(results)
        elif user_input != quit:
            user_input = not_in_menu()


def search_exact_query():
    """By exact query"""
    entries = get_entries()
    search_keys = ["Title", "Notes"]
    results = []
    reset_screen(SEARCH_MENU[4].__doc__, "Please write a query:")
    user_input = get_input(str, newline=False)
    for entry in entries:
        for key in search_keys:
            if user_input.lower() in entry[key].lower():
                results.append(entry)
    return view_results(results)


def search_pattern():
    """By pattern"""
    user_input = None
    entries = get_entries()
    search_keys = ["Title", "Notes"]
    results = []
    while not user_input:
        reset_screen(SEARCH_MENU[5].__doc__, "Please write a regex:")
        user_input = r"" + get_input(str, newline=False)
    for entry in entries:
        for key in search_keys:
            if (re.search(user_input, entry[key])) and entry not in results:
                results.append(entry)
    return view_results(results)


def view_results(results):
    """Print results on screen"""
    if results:
        user_input = None
        cur_i = 0
        last_i = len(results)
        while user_input != "r":
            reset_screen("Results", f"Result: {cur_i + 1} of {last_i}")
            for key, value in results[cur_i].items():
                print(f"{key}: {value}")
            print("\n[B]ack, [N]ext, [E]dit, [D]elete, [R]eturn to Main Menu")
            user_input = get_input(str).lower()
            if user_input in ["b", "n", "e", "d"]:
                if user_input == "b" and cur_i > 0:
                    cur_i -= 1
                elif user_input == "n" and cur_i < last_i - 1:
                    cur_i += 1
                elif user_input == "e":
                    results[cur_i] = edit_entry(results[cur_i])
                elif user_input == "d":
                    return delete_entry(results, results[cur_i])
    else:
        reset_screen("Results", "No Results.", confirm=True)


def get_entries():
    """Return all entries from csv file"""
    with open("entries.csv", newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")
        entries = list(csvreader)
    return entries


def edit_entry(edit_result):
    """Edit entry"""
    new_entry = edit_result.copy()
    edit_key = None
    edit_value = None
    date_keys = ["Date"]
    int_keys = ["Time Spent"]
    while edit_key not in edit_result:
        reset_screen("key", "Please type the key you want to edit.")
        for key, value in edit_result.items():
            print(f"{key}: {value}")
        edit_key = get_input(str)
        if edit_key not in edit_result:
            reset_screen(error=True, sub_title="Input is not a valid key.")
    if edit_key in date_keys:
        input_type = datetime
    elif edit_key in int_keys:
        input_type = int
    else:
        input_type = str
    while not edit_value:
        reset_screen("new value", ENTRY_QUESTIONS[edit_key])
        edit_value = get_input(input_type, newline=False)
    new_entry[edit_key] = edit_value
    entries = get_entries()
    entries[entries.index(edit_result)] = new_entry
    csvfile = open("entries.csv", "w")
    csvfile.close()
    for entry in entries:
        write_to_csv(entry)
    return new_entry


def delete_entry(results, del_result):
    """Delete entry"""
    entries = get_entries()
    entries.remove(del_result)
    csvfile = open("entries.csv", "w")
    csvfile.close()
    for entry in entries:
        write_to_csv(entry)
    results.remove(del_result)
    return view_results(results)


def get_input(type, newline=True):
    """Get user's input"""
    cursor = "\n> " if newline else "> "
    if type == datetime:
        try:
            user_input = input(cursor).strip()
            datetime.strptime(user_input, D_FORM)
            return user_input
        except ValueError:
            reset_screen(error=True, sub_title="Input is not a valid date.")
    elif type == int:
        try:
            user_input = int(input(cursor))
            return user_input
        except ValueError:
            reset_screen(error=True, sub_title="Input is not an integer.")
    elif type == str:
        return input(cursor).strip().capitalize()


def reset_screen(title=None, sub_title=None, confirm=False, error=False):
    """Reset screen"""
    os.system("cls" if os.name == "nt" else "clear")
    if error:
        title, confirm = "Error", True
    if title:
        print("{0}\n{1}\n{0}\n".format("-" * 40, title.title()))
    if sub_title:
        print("{}\n".format(sub_title).capitalize())
    if confirm:
        input("Press enter to continue... ")


def print_return_to_main(value):
    """Print return to menu message"""
    print(f"\n{value}) Return to Main Menu")


def not_in_menu():
    """Print error message"""
    reset_screen(error=True, sub_title="Input is not in menu.")
    return None


def quit_program():
    """Quit Program"""
    reset_screen("Logged out")
    sys.exit()


MAIN_MENU = OrderedDict([
    (1, add_entry),
    (2, show_search_options),
    (3, quit_program),
])

SEARCH_MENU = OrderedDict([
    (1, search_exact_date),
    (2, search_date_range),
    (3, search_time_spent),
    (4, search_exact_query),
    (5, search_pattern)
])

ENTRY_QUESTIONS = {
    "Date": "What is the date? (mm/dd/yyyy)",
    "Title": "What is the title?",
    "Time Spent": "What is the amount of minutes spent? (integer)",
    "Notes": "Do you want to add any notes? (optional)",
}

D_FORM = "%m/%d/%Y"

if __name__ == "__main__":
    show_main_menu()
