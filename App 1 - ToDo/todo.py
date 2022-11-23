from os import path
import sys
import os.path
#TODO Add Help File

def format_input(input):
    return input.lower().strip()

def show_list(todos):
    print("\n** TODO LIST **\n")
    for index, item in enumerate(todos):
        item = item.replace("\n", "")
        print(f'{index + 1}: {item}')
    print("\n**End of TODO list.**\n")

def write_to_file(todo_list):
        with open('todos.txt', 'w', encoding="utf-8") as file:
            for i in todo_list:
                file.write(i + '\n')

def print_welcome():
    print("*-------------------------------------------------------------*")
    print("WELCOME TO THE TERMINAL OPERATED DAILY ORGANIZER (TODO) SOFTWARE")
    print("*-------------------------------------------------------------*")

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
                print("Type add <your task> to add a new Task")
                print("Type show to see your list")
                print("Type edit <task #> to edit a task: EXAMPLE - edit 2")
                print("Type mark to mark a task as completed but leave it in your list.")
                print("Type delete to delete a single task from the list.")
                print("Type remove to delete all MARKED tasks from list.")
                print("******")
            else:
                break
        if 'add' in user_action:
            todo = user_action[4:]
            todos.append(todo)
            try:
                write_to_file(todos)
            except:
                print("Failed to save file to disk.")
            else:
                print(f'List updated')
        if 'show' in user_action:
            show_list(todos)
        if 'edit' in user_action:
            edit_selection = user_action[4:]
            try:
                edit_selection = int(edit_selection.strip()) - 1
            except:
                print("You did not enter a number")
            else:
                if 0 <= edit_selection < len(todos):
                    old_todo = todos[edit_selection]
                    edit_todo = input("Enter new a TODO task:\n").capitalize()
                    todos[edit_selection] = edit_todo
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save list to file.")
                    else:
                        print(f'Replaced TODO task successfully \nOLD: {old_todo} \nNEW: {edit_todo} \n')
                else:
                    print("No item with that number exists in your list.")
        if 'mark' in user_action:
            user_action = format_input(input("Select the number of the task you want to mark COMPLETE, or type (s)how to show the list again:.. "))
            if user_action == "show" or user_action == 's':
                show_list()
            else:
                try:
                    mark_selection = int(user_action) - 1
                except:
                    print("You did not enter a number")
                else:
                    if 0 <= mark_selection < len(todos):
                        result = ''
                        text = "X" + todos[mark_selection]
                        for c in text:
                            result = result + c + '\u0336'

                        todos[mark_selection] = result
                        try:
                            write_to_file(todos)
                        except:
                            print("Failed to save file to disk.")
                        else:
                            print(f'Task {todos[mark_selection]} marked Complete.')
                    else:
                        print("No task with that number exists in your TODO list.")
        if 'remove' in user_action:
            user_action = format_input(input("CONFIRM remove all completed tasks? (Y/N)... "))
            if user_action == 'y':
                new_todos = []
                for i in todos:
                    if i[0] != 'X':
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
                show_list()
        if 'delete' in user_action:
            user_action = format_input(input("Select the number of the task to remove, or type (s)how to show the list again:.. "))
            if user_action == "show" or user_action == "s":
                show_list()
            else:
                try:
                    remove_selection = int(user_action) - 1
                except:
                    print("You did not enter a number")
                else:
                    if 0 <= remove_selection < len(todos):
                        removed_item = todos.pop(remove_selection)
                        try:
                            write_to_file(todos)
                        except:
                            print("Failed to save file to disk.")
                        else:
                            print(f'Removed \n{removed_item}\nsuccessfully\n')
                    else:
                        print("No task with that number exists in your TODO list.")                
        if 'exit' in user_action:
            break
    print("Exiting")

if __name__ == "__main__":
    main() 