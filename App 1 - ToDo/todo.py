from os import path
import sys
import os.path

if os.path.exists("todos.txt"):
    file = open('todos.txt', 'r', encoding="utf-8")
    todos = file.readlines()
else:
    todos = []

user_action = ''

def format_input(input):
    return input.lower().strip()

def show_list():
    print("** TODO LIST **")
    for index, item in enumerate(todos):
        print(f'{index + 1}: {item}')
    print("**End of TODO list.**")

def write_to_file(todo_list):
        file = open('todos.txt', 'r', encoding="utf-8")
        todos = file.readlines()
        todos.append(todo_list)
        file = open('todos.txt', 'w', encoding="utf-8")
        file.writelines(todo_list)

while True:
    if len(todos) == 0:
        print("No ToDo list currently exists.")
        user_action = format_input(input("type (a)dd or exit\n"))
        match user_action:
            case 'add' | 'a':
                user_prompt = "Enter a ToDo Task:\n"
                todo = input(user_prompt).capitalize() + "\n"
                todos.append(todo)
                try:
                    write_to_file(todos)
                except:
                    print("Failed to save file to disk.")
                else:
                    print(f'List updated')
            case 'exit':
                break
    else:
        user_action = format_input(input("type (a)dd, (e)dit, (c)omplete, (r)emove, (s)how, or exit\n"))
        match user_action:
            case 'add' | 'a':
                user_prompt = "Enter a ToDo Task:\n"
                todo = input(user_prompt + "\n").capitalize() + "\n"
                todos.append(todo)
                try:
                    write_to_file(todos)
                except:
                    print("Failed to save file to disk.")
                else:
                    print(f'List updated')
            case 'show' | 's':
               show_list()
            case 'edit' | 'e':
                user_action = format_input(input("Select the number of the item to edit, or type show to show the list again: "))
                if user_action == "show":
                    show_list()
                else:
                    try:
                        edit_selection = int(user_action) - 1
                    except:
                        print("You did not enter a number")
                    else:
                        if 0 <= edit_selection < len(todos):
                            old_todo = todos[edit_selection]
                            edit_todo = input("Enter new ToDo:\n").capitalize()  + "\n"
                            todos[edit_selection] = edit_todo
                            try:
                                write_to_file(todos)
                            except:
                                print("Failed to save file to disk.")
                            else:
                                print(f'Replaced ToDO successfully \nOLD: {old_todo} \nNEW: {edit_todo} \n')
                        else:
                            print("No item with that number exists in your list.")
            case 'complete' | 'c':
                user_action = format_input(input("Select the number of the item mark complete, or type show to show the list again: "))
                if user_action == "show":
                    show_list()
                else:
                    try:
                        mark_selection = int(user_action) - 1
                    except:
                        print("You did not enter a number")
                    else:
                        if 0 <= mark_selection < len(todos):
                            result = ''
                            text = todos[mark_selection]
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
                            print("No item with that number exists in your list.")
            case 'remove' | 'r':
                user_action = format_input(input("Select the number of the item to remove, or type show to show the list again: "))
                if user_action == "show":
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
                            print("No item with that number exists in your list.")
            case 'exit':
                break
print("Exiting")