from os import path
import sys
import os.path
#TODO Add Help File

def format_input(input):
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

def write_to_file(todo_list):
        with open('todos.txt', 'w', encoding="utf-8") as file:
            for i in todo_list:
                file.write(i + '\n')

def print_welcome():
    print("*-------------------------------------------------------------*")
    print("WELCOME TO THE TERMINAL OPERATED DAILY ORGANIZER (TODO) SOFTWARE")
    print("*-------------------------------------------------------------*")

def underline_text(text):
    return "\x1B[4m" + text + "\x1B[0m"
    
def main():
    if os.path.exists("todos.txt"):
        with open('todos.txt', 'r', encoding="utf-8") as file:
            if file.readlines() == "":
                todos = []
            else:
                file.seek(0)
                todos_temp = file.readlines()
                todos = [i.strip("\n") for i in todos_temp]
    else:
        file = open('todos.txt', 'w', encoding="utf-8")
        todos = []


    print_welcome()
    
    while True:
        while True:
            user_action = format_input(input("What would you like to do? Type COMMANDS for a list of commands\n"))
            if "commands" in user_action:
                print("\n***COMMANDS***")
                print(f'Type {underline_text("add")} <<your task>> to add a new task')
                print(f'Type {underline_text("show")} to see your list')
                print(f'Type {underline_text("edit")} <<task #>> to edit a task')
                print(f'Type {underline_text("mark")} <<task #>> to mark a task as completed but leave it in your list.')
                print(f'Type {underline_text("delete")} <<task #>> to delete a single task from the list.')
                print(f'Type {underline_text("remove")} to delete ALL MARKED tasks from list.')
                print(f'\n{underline_text("EXAMPLE COMMANDS")}')
                print("Adding a new task: add Clean House")
                print("Edit task #3: edit 3")
                print("******")
            else:
                break
        if user_action.startswith("add"):
            todo = user_action[4:].capitalize()
            todo = "[ ] " + todo
            todos.append(todo)
            try:
                write_to_file(todos)
            except:
                print("Failed to save file to disk.")
            else:
                print(f'List updated')
        elif user_action.startswith("show"):
            show_list(todos)
        elif user_action.startswith("edit"):
            selection = user_action[4:]
            try:
                selection = int(selection.strip()) - 1
            except:
                print("You did not enter a number")
            else:
                if 0 <= selection < len(todos):
                    old_todo = todos[selection]
                    edit_todo = input("Enter new a TODO task:\n").capitalize()
                    edit_todo = "[ ] " + edit_todo
                    todos[selection] = edit_todo
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save list to file.")
                    else:
                        print(f'Replaced TODO task successfully \nOLD: {old_todo} \nNEW: {edit_todo} \n')
                else:
                    print("No item with that number exists in your list.")
        elif user_action.startswith("mark"):
            selection = user_action[4:]
            try:
                selection = int(selection.strip()) - 1
            except:
                print("You did not enter a number")
            else:
                if 0 <= selection < len(todos):
                    result = ''
                    text = todos[selection]
                    # for c in text:
                    #     result = result + c + '\u0336'

                    result = "[X] " + text[4:]
                    todos[selection] = result
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")
                    else:
                        print(f'Task {todos[selection]} marked Complete.')
                else:
                    print("No task with that number exists in your TODO list.")
        elif user_action.startswith("remove"):
            user_action = format_input(input("CONFIRM remove all completed tasks? (Y/N)... "))
            if user_action == 'y':
                new_todos = []
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
                if 0 <= selection < len(todos):
                    removed_item = todos.pop(selection)
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")
                    else:
                        print(f'Removed \n{removed_item}\nsuccessfully\n')
                else:
                    print("No task with that number exists in your TODO list.")                
        elif user_action.startswith("exit"):
            break
        else:
            print("!!! Command not recognized. Type commands to see list of available commands !!!\n")
    print("Exiting")

if __name__ == "__main__":
    main() 