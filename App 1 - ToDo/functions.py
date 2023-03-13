from os import path, system, name
import sys
import os.path
import configparser
import ast
#TODO Add Help File

last_file = ""
file_list = []
file_open = ""
file_to_edit = ''
undo_opt = {
    'last': '',
    'data' : ''
}
config = configparser.ConfigParser()

def clear():
 # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

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

def get_undo_opt():
    return undo_opt
def get_file_list():
    return file_list
    
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
        print("Opening last file called: "+ last_file)
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

def console_add_bracket(todo):
    return "[ ] " + todo

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

def print_msg_box(message, title = "LAST ACTION ", sub_text = "type UNDO to undo last action "):
    box_padding = 10
    if (len(title) % 2 ) != 0: # Make message even for better border alignment
        title = title + " "
    if (len(sub_text) % 2 ) != 0: # Make message even for better border alignment
        sub_text = sub_text + " "
    if (len(message) % 2 ) != 0: # Make message even for better border alignment
        message = message + " "
    
    box_width = len(message) + box_padding # Width of history box based on incoming message length plus padding

    print_spaces = lambda static_text_len : ' ' * int(get_spaces(static_text_len))
    get_spaces = lambda static_text_len : (box_width - (static_text_len + 2)) / 2
    msg_spaces = ' ' * 4
    empty_spaces = len(message) + 8
    print('*' * box_width)
    print(f'*{print_spaces(len(title))}{title}{print_spaces(len(title))}*')
    print(f'*{" " * empty_spaces}*')
    print(f'*{msg_spaces}{message}{msg_spaces}*')
    print(f'*{" " * empty_spaces}*')
    print(f'*{print_spaces(len(sub_text))}{sub_text}{print_spaces(len(sub_text))}*')
    print('*' * box_width)

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
            print_msg_box(f'Changed to TODO list titled {file_to_edit[:-4].title().replace("_"," ")}')
            save_config(file_to_edit, file_list)
            return file_to_edit
            
        elif user_action == '2':
            new_file = add_new_file()
            with open(new_file, 'w') as fp:
                pass
            print_msg_box(f'Created a new TODO list named {file_to_edit[:-4].title().replace("_"," ")}')
            while True:
                user_action = format_input(input("Do you want to edit this new TODO now? Y/N: "))
                if user_action == 'y':
                    title_bar(new_file)
                    file_to_edit = new_file
                    save_config(file_to_edit, file_list)
                    print_msg_box(f'Switched to new TODO list named {file_to_edit[:-4].title().replace("_"," ")}')
                    return file_to_edit
                elif user_action == 'n':
                    file_to_edit = file_to_edit
                    save_config(file_to_edit, file_list)
                    break
                else:
                    print("Invalid Selection")
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
    file_list.append(file_name)
    return file_name

def add_task(user_action, file_to_edit, undo = False, gui = False):
    global undo_opt
    if not gui:
        todo = user_action[4:].capitalize()
    else:
        if not undo:
            todo = user_action
        else:
            todo = user_action[4:]
    message = todo
    todo = console_add_bracket(todo)
    todos = get_todos(file_to_edit)
    todos.append(todo)
    try:
        write_to_file(todos,file_to_edit)
    except:
        print("Failed to save file to disk.")
    else:
        if not undo:
            print_msg_box(f'Added {message} to list.')
        else:
            print_msg_box(f'Added {message} to list via UNDO command.','UNDO','Type UNDO to REDO.')
        undo_opt.update({'last':'add'})

def edit_task(user_action, file_to_edit, gui=False, new_edit = ""):
    todos = get_todos(file_to_edit)
    if not gui:
        selection = user_action[5]
    else:
        selection = str(todos.index(user_action) + 1)
    
    try:
        selection = int(selection.strip()) - 1
    except ValueError:
        print_msg_box("You did not enter a number", "ERROR", "Enter a valid number")
    else:
        try:
            old_todo = todos[selection] 
        except IndexError:
            print_msg_box("No task with that number is in your list.", "ERROR", "")
        else:
            if not gui:
                if user_action[7:] == "":
                    print_msg_box(f'Enter the new task for todo task {old_todo[4:].capitalize()}', "DIRECTIONS", " Type COMMAND for more info.")
                    edit_todo = input()
                else:
                    if user_action[6] != " ":
                        edit_todo = user_action[6:].capitalize()
                    else:
                        edit_todo = user_action[7:].capitalize()
            else:
                edit_todo = new_edit
            edit_todo = "[ ] " + edit_todo
            todos = get_todos(file_to_edit)
            todos[selection] = edit_todo
            try:
                write_to_file(todos,file_to_edit)
            except:
                print("Failed to save list to file.")
            else:
                print_msg_box(f'Replaced TODO task successfully \'{old_todo[4:].capitalize()}\' with \'{edit_todo[4:].capitalize()}\' ')

def mark_task(user_action, file_to_edit, mark = True, undo = False, gui=False):
    global undo_opt
    todos = get_todos(file_to_edit)

    if mark:
        if not undo:
            if gui:
                selection = str(todos.index(user_action) + 1)
            else:
                selection = user_action[4:]
        else:
            if gui:
                selection = str(todos.index(user_action) + 1)
            else:
                selection = str(user_action + 1)
        try:
            selection = int(selection.strip()) - 1
        except ValueError:
            title_bar(file_to_edit)
            print_msg_box("You did not enter a number", "ERROR", "Enter a valid number")
        else:
            try:
                text = todos[selection]  
            except IndexError:
                title_bar(file_to_edit)
                print_msg_box("No task with that number is in your list.", "ERROR", "")
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
                    title_bar(file_to_edit)
                    print_msg_box(f'Task: {todos[selection][4:].capitalize()} marked Complete.')
                    undo_opt.update({'last':'mark','data':selection})
    else:
        if not undo:
            selection = user_action[4:]
        else:
            selection = str(user_action + 1)
        try:
            selection = int(selection.strip()) - 1
        except ValueError:
            title_bar(file_to_edit)
            print_msg_box("You did not enter a number", "ERROR", "Enter a valid number")
        else:
            try:
                text = todos[selection]  
            except IndexError:
                title_bar(file_to_edit)
                print_msg_box("No task with that number is in your list.", "ERROR", "")
            else:
                result = ''
                result = "[ ] " + text[4:]
                todos = get_todos(file_to_edit)
                todos[selection] = result
                try:
                    write_to_file(todos,file_to_edit)
                except:
                    print("Failed to save file to disk.")
                else:
                    title_bar(file_to_edit)
                    print_msg_box(f'Task: {todos[selection][4:].capitalize()} UNmarked.')
                    undo_opt.update({'last':'unmark','data':selection}) 

def remove_marked_tasks(file_to_edit, gui = False, confirm = False):
    global undo_opt
    while True:
        if not gui:
            title_bar(file_to_edit)
        
        if not confirm:
            print_msg_box(f'CONFIRM remove all completed tasks? (Y/N)', "CONFIRMATION", "Type y or n to continue")
            user_action = format_input(input())
        else:
            user_action = 'y'

        if user_action == 'y':
            new_todos = []
            removed_todos = []
            todos = get_todos(file_to_edit)
            original_todos = todos
            for i in todos:
                if i[1] != 'X':
                    new_todos.append(i)
                elif i[1] == 'X':
                    removed_todos.append(i)
            todos = new_todos
            print_msg_box(f'')
            if len(removed_todos) == 0:
                title_bar(file_to_edit)
                print_msg_box("No tasked were removed as none were marked as Complete.", "NOTICE", "Type mark <task#> to mark tasks.")
                break
            else:
                try:
                    write_to_file(todos,file_to_edit)
                except:
                    print("Failed to save file to disk.")
                else:
                    title_bar(file_to_edit)
                    print_msg_box(f'Removed {len(removed_todos)} successfully')
                    undo_opt.update({'last':'remove','data':original_todos})
                    break
        elif user_action == 'n':
            title_bar(file_to_edit)
            break
        else:
            title_bar(file_to_edit)
            print_msg_box("You did not type 'y' or 'n'", "ERROR", "")
        
def delete_task(user_action, file_to_edit, undo = False, gui = False):
    global undo_opt
    todos = get_todos(file_to_edit)
    if not gui:
        selection = user_action[5]
        if not undo:
            selection = user_action[6:]
        else:
            selection = user_action - 1
    else:
        if not undo:
            selection = str(todos.index(user_action) + 1)
        else:
            selection = user_action - 1


    try:
        if not undo:
            selection = int(selection.strip()) - 1
        else:
            pass
    except:
        print_msg_box("You did type a number",'ERROR','Enter a valid list number.')
    else:
        try:
            todos = get_todos(file_to_edit)
            removed_item = todos.pop(selection)
        except IndexError:
            print_msg_box("No task with that number is in your list.",'ERROR','Enter a valid list number.')
        else:
            if undo:
                print_msg_box(f'Removed task \'{removed_item[4:]}\' via UNDO command', 'UNDO', 'type UNDO to REDO this command')
                undo_opt.update({'last':'delete','data':removed_item})
            else:
                print_msg_box(f'Removed task \'{removed_item[4:]}\' from list')
                undo_opt.update({'last':'delete','data':removed_item})
            try:
                write_to_file(todos,file_to_edit)
            except:
                print("Failed to save file to disk.")   

def undo(undo, file_to_edit, gui = False):
    global undo_opt
    match undo['last']:
        case "add":
            selection = len(get_todos(file_to_edit))
            delete_task(selection, file_to_edit, undo = True, gui = gui)
        case 'delete':
            add_task(undo['data'],file_to_edit, undo = True, gui = gui)
        case 'mark':
            mark_task(undo['data'],file_to_edit, mark = False, undo = True,gui = gui)
        case 'unmark':
            mark_task(undo['data'],file_to_edit, mark = True, undo = True,gui = gui)
        case 'remove':
            todos = []
            for todo in undo['data']:
                todos.append(todo)
            write_to_file(todos,file_to_edit)
            print_msg_box("Undo 'Remove All Marked'", "NOTICE", "No Undo Available")

                
def get_file_to_edit():
    return file_to_edit
            

    
def title_bar(file_to_edit):
    clear()
    print('----------------------------TERMINAL OPERATED DAILY ORGANIZER----------------------------')
    print(f'*********EDITING TODO LIST: {file_to_edit[:-4].replace("_"," ").title()}*********')
    print('-----------------------------------------------------------------------------------------')

 