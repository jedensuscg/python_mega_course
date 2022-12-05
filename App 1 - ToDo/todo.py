from os import path
import sys
import os.path
import configparser
import ast
#TODO Add Help File

last_file = ""
file_list = []
file_open = ""
config = configparser.ConfigParser()
def save_settings(file_open, files):
    file_list_string = ""
    with open("config.ini", "w") as configfile:
        config.set('DEFAULT','lastfile',"todos.txt")
        config.set('DEFAULT','filelist', f'{files}')
        config.write(configfile)

def load_settings():
    if os.path.exists("config.ini"):
        config.read("config.ini")
        last_file = config['DEFAULT']['lastfile']
        file_list =  ast.literal_eval(config['DEFAULT']['filelist'])
        if len(file_list) < 2:
            file_open = file_list[0]
            print(file_open)
    else:
        print("No config found, creating new one.")
        config['DEFAULT'] = {'lastfile' : "todos.txt", 'FileList' : ["todos.txt"]}
        with open("config.ini", "w") as configfile:
            config.write(configfile)


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

def write_to_file(todo_list, todo_file = "todos.txt"):
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

def main():
    
    load_settings()
    todos = get_todos()
    print_welcome()
    
    while True:
        while True:
            user_action = format_input(input("What would you like to do? Type COMMANDS for a list of commands\n"))
            if "commands" in user_action:
                print("\n***COMMANDS***")
                print(f'Type {underline_text("add")} <<your task>> to add a new task')
                print(f'Type {underline_text("show")} to see your list')
                print(f'Type {underline_text("edit")} <<task #>> <<new task>> to edit a task. You may also omit the new task to be prompted to enter it.')
                print(f'Type {underline_text("mark")} <<task #>> to mark a task as completed but leave it in your list.')
                print(f'Type {underline_text("delete")} <<task #>> to delete a single task from the list.')
                print(f'Type {underline_text("remove")} to delete ALL MARKED tasks from list.')
                print(f'\n{underline_text("EXAMPLE COMMANDS")}')
                print("ADD A NEW TASK: add Clean House")
                print("EDIT TASK #3: edit 3 Clean house")
                print("EDIT TASK #3 (secondary option): edit 3 NOTE: Omitting the new task will prompt you to enter one.")
                print("DELETE TASK #3: delete 3")
                print("******")
            else:
                break

        if user_action.startswith("add"):
            todo = user_action[4:].capitalize()
            todo = "[ ] " + todo
            todos = get_todos()
            todos.append(todo)
            try:
                write_to_file(todos)
            except:
                print("Failed to save file to disk.")
            else:
                print(f'List updated')

        elif user_action.startswith("show"):
            todos = get_todos()
            show_list(todos)

        elif user_action.startswith("edit"):
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
                    todos = get_todos()
                    todos[selection] = edit_todo
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save list to file.")
                    else:
                        print(f'Replaced TODO task successfully \nOLD: {old_todo} \nNEW: {edit_todo} \n')

        elif user_action.startswith("mark"):
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
                    todos = get_todos()
                    todos[selection] = result
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")
                    else:
                        print(f'Task: {todos[selection][4:]} marked Complete.')
                
        elif user_action.startswith("remove"):
            user_action = format_input(input("CONFIRM remove all completed tasks? (Y/N)... "))
            if user_action == 'y':
                new_todos = []
                todos = get_todos()
                for i in todos:
                    if i[1] != 'X':
                        new_todos.append(i)
                removed_todos = len(todos) - len(new_todos)
                todos = new_todos
                if removed_todos == 0:
                    print("No tasked were removed as none were marked as Complete.")
                else:
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")
                    else:
                        print(f'Removed \n{removed_todos}\nsuccessfully\n')
            else:
                show_list(todos)
        
        elif user_action.startswith("delete"):
            selection = user_action[6:]
            try:
                selection = int(selection.strip()) - 1
            except:
                print("You did not enter a number")
            else:
                try:
                    todos = get_todos()
                    text = todos[selection]  
                except IndexError:
                    print("No task with that number is in your list.")
                else:
                    removed_item = todos.pop(selection)
                    print(f'Removed task \'{removed_item[4:]}\' from list')
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")            
        
        elif user_action.startswith("exit"):
            save_settings(file_open, file_list)
            break
        else:
            print("!!! Command not recognized. Type commands to see list of available commands !!!\n")
    print("Exiting")

if __name__ == "__main__":
    main() 