from os import path, system, name
import  psutil
import sys
import os.path
import configparser
import ast
#TODO Add Help File

last_file = ""
file_list = []
file_open = ""
file_to_edit = ''
config = configparser.ConfigParser()

def init_config():
        print("This appears to be the first time you have ran the TODO Software")
        print("No config file found, creating new one.")
        name = add_new_file()
        config['DEFAULT'] = {
        'LastFile' : 'todos.txt', 
        'FileList' : [name],
        'LoadLastAlways' : 'False'
        }
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        load_config()

def startup():
    config.read("config.ini")
    if config.getboolean('DEFAULT','loadlastalways') == True:
        return last_file
    else:
        return prompt_for_file()

def save_config(file_open, files):
    file_list_string = ""
    with open("config.ini", "w") as configfile:
        config.set('DEFAULT','LastFile',file_open)
        for filename in files:
            if not os.path.exists(filename):
                files.remove(filename)
        config.set('DEFAULT','FileList', f'{files}')
        config.write(configfile)

def load_config():
    global file_list
    global last_file

    if os.path.exists("config.ini"):
        config.read("config.ini")
        last_file = config['DEFAULT']['lastfile']
        print(last_file)
        file_list = ast.literal_eval(config['DEFAULT']['filelist'])
    else:
        init_config()

def format_input(input):
    """ Formats the input by lowercasing all 
    words and removing leading and trailing spaces.
    """
    return input.lower().strip()

def show_list(todos):
    print("\n** TODO LIST **\n")
    if len(todos) > 0:
        for index, item in enumerate(todos):
            item = item.replace("\n", "")
            print(f'{index + 1}: {item}')
    else:
        print("----------LIST IS EMPTY-----------")
    print("\n**End of TODO list.**\n")

def write_to_file(todo_list, todo_file):
        with open(todo_file, 'w', encoding="utf-8") as file:
            for i in todo_list:
                if i[0] != "[":
                    file.write("[ ] " + i + '\n')
                else:
                    file.write(i + '\n')

def print_welcome():
    print("*-------------------------------------------------------------*")
    print("WELCOME TO THE TERMINAL OPERATED DAILY ORGANIZER (TODO) SOFTWARE")
    print("*-------------------------------------------------------------*")

def underline_text(text):
    return "\x1B[4m" + text + "\x1B[0m"

def prompt_for_file():

        while True:
            print("Please select the number next to the TODO you want to use OR type NEW to create a new list")
            for index, file in enumerate(file_list):
                print(f'{index + 1}: {file[:-4].title().replace("_"," ")}')
            user_action = format_input(input("Enter selection: "))
            if user_action == 'new':
                add_new_file()
            else:
                try:
                    user_action = int(user_action)
                except ValueError:
                    print("You did not enter a number")
                else:
                    try:
                        file_to_open = file_list[user_action - 1]
                        file = file_to_open
                    except IndexError:
                        print("No file exist for number entered.")
                    else:
                        title_bar(file)
                        return file_to_open
            
def show_options(file_to_edit):
    while True:
        config.read("config.ini")
        load_last = config.getboolean('DEFAULT','LoadLastAlways')
        print("\nOptions Menu")
        print(f'1: Load last used list on startup: {"Yes" if load_last else "No"}')
        selection = format_input(input("Type the number of the option you wish to change, or exit to leave menu:  "))
        if selection == '1':
            while True:
                print('Setting to (Y)es will load last used TODO list without prompt. You can choose a different list from the FILE menu.')
                selection = format_input(input('Enter a new setting: Y/N  '))
                if selection == 'y':
                    with open("config.ini", "w") as configfile:
                        config.set('DEFAULT','loadlastalways','True')
                        config.write(configfile)
                        break
                elif selection == 'n':
                    with open("config.ini", "w") as configfile:
                        config.set('DEFAULT','loadlastalways','False')
                        config.write(configfile)
                        break
                else:
                    print("Invalid Selection")
        elif selection == 'exit':
            title_bar(file_to_edit)
            break
        else:
            print("Invalid Selection")

def show_file_menu(file_to_edit):
    while True:
        print("**FILE MENU**\n")
        user_action = format_input(input("Please make a selection:\n1: Select a different TODO file\n2: Add new TODO file \nType exit to cancel.\n"))
        if user_action == '1':
            file_to_edit = prompt_for_file()
            title_bar(file_to_edit)
            print(f'\nChanged to TODO list titled {file_to_edit[:-4].title().replace("_"," ")}')
            return file_to_edit
            
        elif user_action == '2':
            new_file = add_new_file()
            save_config(file_to_edit, file_list)
            while True:
                user_action = format_input(input("Do you want to edit this new TODO now? Y/N: "))
                if user_action == 'y':
                    title_bar(new_file)
                    file_to_edit = new_file
                    return file_to_edit
        elif user_action == 'exit':
            title_bar(file_to_edit)
            break
        else:
            print("Invalid Selection")

def get_todos(todo_file = "todos.txt"):
    """ Opens todo file and returns list of tasks"""
    if os.path.exists(todo_file):
        with open(todo_file, 'r', encoding="utf-8") as file:
            if file.readlines() == "":
                todos = []
            else:
                file.seek(0)
                todos_temp = file.readlines()
                todos = [i.strip("\n") for i in todos_temp]
                return todos
    else:
        file = open(todo_file, 'w', encoding="utf-8")
        todos = []
        return todos

def add_new_file():
    title_bar("Creating New TODO")
    name = format_input(input("Please enter a name for the initial TODO list:\n"))
    name = name.replace(" ","_")
    file_name = name + ".txt"
    print(f'New TODO file named {name}')
    file_list.append(file_name)
    return file_name

def add_task(user_action, file_to_edit):
    todo = user_action[4:].capitalize()
    todo = "[ ] " + todo
    todos = get_todos(file_to_edit)
    todos.append(todo)
    try:
        write_to_file(todos,file_to_edit)
    except:
        print("Failed to save file to disk.")
    else:
        print(f'List updated')

def edit_task(user_action, file_to_edit):
    todos = get_todos(file_to_edit)
    selection = user_action[5]
    try:
        selection = int(selection.strip()) - 1
    except ValueError:
        print("You did not enter a number")
    else:
        try:
            old_todo = todos[selection] 
        except IndexError:
            print("No task with that number is in your list.")
        else:
            if user_action[7:] == "":
                edit_todo = input("Enter new a TODO task:\n").capitalize()
            else:
                if user_action[6] != " ":
                    edit_todo = user_action[6:].capitalize()
                else:
                    edit_todo = user_action[7:].capitalize()
            edit_todo = "[ ] " + edit_todo
            todos = get_todos(file_to_edit)
            todos[selection] = edit_todo
            try:
                write_to_file(todos,file_to_edit)
            except:
                print("Failed to save list to file.")
            else:
                print(f'Replaced TODO task successfully \nOLD: {old_todo} \nNEW: {edit_todo} \n')

def mark_task(user_action, file_to_edit):
    todos = get_todos(file_to_edit)
    selection = user_action[4:]
    try:
        selection = int(selection.strip()) - 1
    except ValueError:
        print("You did not enter a number")
    else:
        try:
            text = todos[selection]  
        except IndexError:
            print("No task with that number is in your list.")
        else:
            result = ''
            result = "[X] " + text[4:]
            todos = get_todos(file_to_edit)
            todos[selection] = result
            try:
                write_to_file(todos,file_to_edit)
            except:
                print("Failed to save file to disk.")
            else:
                print(f'Task: {todos[selection][4:]} marked Complete.')

def remove_marked_tasks(file_to_edit):
    user_action = format_input(input("CONFIRM remove all completed tasks? (Y/N)... "))
    if user_action == 'y':
        new_todos = []
        todos = get_todos(file_to_edit)
        for i in todos:
            if i[1] != 'X':
                new_todos.append(i)
        removed_todos = len(todos) - len(new_todos)
        todos = new_todos
        if removed_todos == 0:
            print("No tasked were removed as none were marked as Complete.")
        else:
            try:
                write_to_file(todos,file_to_edit)
            except:
                print("Failed to save file to disk.")
            else:
                print(f'Removed \n{removed_todos}\nsuccessfully\n')
    else:
        show_list(todos)

def delete_task(user_action, file_to_edit):
    selection = user_action[6:]
    try:
        selection = int(selection.strip()) - 1
    except:
        print("You did not enter a number")
    else:
        try:
            todos = get_todos(file_to_edit)
            text = todos[selection]  
        except IndexError:
            print("No task with that number is in your list.")
        else:
            removed_item = todos.pop(selection)
            print(f'Removed task \'{removed_item[4:]}\' from list')
            try:
                write_to_file(todos,file_to_edit)
            except:
                print("Failed to save file to disk.")   

def clear():
 # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    
def title_bar(file_to_edit):
    clear()
    print('----------------------------TERMINAL OPERATED DAILY ORGANIZER----------------------------')
    print(f'*********EDITING TODO LIST: {file_to_edit[:-4].replace("_"," ").title()}*********')
    print('-----------------------------------------------------------------------------------------')

   

def main():
    
    load_config()
    print_welcome()
    file_to_edit = startup()
    todos = get_todos(file_to_edit)
    
    while True:
        while True:

            print("\n***MAIN MENU***")
            user_action = format_input(input("What would you like to do? Type COMMANDS for a list of commands\n"))

            if "commands" in user_action:
                title_bar(file_to_edit)
                print("\n***COMMANDS***")
                print("*Task Commands*")
                print(f'Type {underline_text("add")} <<your task>> to add a new task')
                print(f'Type {underline_text("show")} to see your list')
                print(f'Type {underline_text("edit")} <<task #>>z <<new task>> to edit a task. You may also omit the new task to be prompted to enter it.')
                print(f'Type {underline_text("mark")} <<task #>> to mark a task as completed but leave it in your list.')
                print(f'Type {underline_text("delete")} <<task #>> to delete a single task from the list.')
                print(f'Type {underline_text("remove")} to delete ALL MARKED tasks from list.')
                print("*Program Commands*")
                print(f'Type {underline_text("file")} to bring up the TODO file menu.')
                print(f'\n{underline_text("EXAMPLE COMMANDS")}')
                print("ADD A NEW TASK: add Clean House")
                print("EDIT TASK #3: edit 3 Clean house")
                print("EDIT TASK #3 (secondary option): edit 3 NOTE: Omitting the new task will prompt you to enter one.")
                print("DELETE TASK #3: delete 3")
                print("******")
            else:
                break

        if user_action.startswith("add"):
            title_bar(file_to_edit)
            add_task(user_action, file_to_edit)

        elif user_action.startswith("show"):
            title_bar(file_to_edit)
            todos = get_todos(file_to_edit)
            show_list(todos)

        elif user_action.startswith("edit"):
            title_bar(file_to_edit)
            edit_task(user_action, file_to_edit)

        elif user_action.startswith("mark"):
            title_bar(file_to_edit)
            mark_task(user_action, file_to_edit)
                
        elif user_action.startswith("remove"):
            title_bar(file_to_edit)
            remove_marked_tasks(file_to_edit)
        
        elif user_action.startswith("delete"):
            title_bar(file_to_edit)
            delete_task(user_action, file_to_edit)

        elif user_action.startswith("file"):
            title_bar(file_to_edit)
            file_to_edit = show_file_menu(file_to_edit)

        elif user_action.startswith("option"):
            title_bar(file_to_edit)
            show_options(file_to_edit)

        elif user_action.startswith("exit"):
            save_config(file_to_edit, file_list)
            clear()
            break
        else:
            print("!!! Command not recognized. Type commands to see list of available commands !!!\n")
    print("Exiting")

if __name__ == "__main__":
    main() 