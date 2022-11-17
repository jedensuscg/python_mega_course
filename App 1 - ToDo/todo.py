from os import path
import sys
import os.path

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
                todos = file.readlines()
    else:
        file = open('todos.txt', 'w', encoding="utf-8")
        todos = []


    print_welcome()
    
    while True:
        if len(todos) == 0:
            print("No TODO list currently exists.")
            user_action = format_input(input("Type (a)dd or exit:.. "))
            match user_action:
                case 'add' | 'a':
                    user_prompt = "Enter a TODO Task:\n"
                    todo = input(user_prompt).capitalize()
                    todos.append(todo)
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")
                    else:
                        print(f'Your TODO List was updated.')
                case 'exit':
                    break
        else:
            user_action = format_input(input("Type (a)dd, (e)dit, (c)omplete, (r)emove, (s)how, or exit:.. "))
            match user_action:
                case 'add' | 'a':
                    user_prompt = "Enter a ToDo Task:\n"
                    todo = input(user_prompt).capitalize()
                    todos.append(todo)
                    try:
                        write_to_file(todos)
                    except:
                        print("Failed to save file to disk.")
                    else:
                        print(f'List updated')
                case 'show' | 's':
                    show_list(todos)
                case 'edit' | 'e':
                    user_action = format_input(input("Select the number of the item to edit, or type show to show the list again:.. "))
                    if user_action == "show":
                        show_list(todos)
                    else:
                        try:
                            edit_selection = int(user_action) - 1
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
                case 'complete' | 'c':
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
                case 'remove' | 'r':
                    print("TASK Deletion Options:")
                    print("Type (d)elete to a delete a single task from your TODO list\nType (r)emove to remove all task MARKED as COMPLETE.\nType (s)how to cancel and view your list.")
                    user_action = format_input(input("What remove operation do you want to do:.. "))
                    match user_action:
                        case 'delete' | 'd':
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
                        case 'remove' | 'r':
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
                case 'exit':
                    break
    print("Exiting")

if __name__ == "__main__":
    main()