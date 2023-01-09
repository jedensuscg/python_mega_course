from functions import (
    underline_text, title_bar, format_input, add_task, 
    delete_task, edit_task, show_list, load_config, startup, 
    get_todos, print_welcome, mark_task, remove_marked_tasks,
    show_options, undo, save_config, clear, get_undo_opt, show_file_menu, get_file_list)

import PySimpleGUI as sg
console_flag = False

load_config()
file_to_edit = startup()
todos = get_todos(file_to_edit)
sg.theme('Dark Amber')
label = sg.Text("Type in a ToDo")
input_box = sg.InputText(tooltip="Enter ToDo", key="todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values = todos, key="todo_list", 
    enable_events=True, size=[45,20])
edit_button = sg.Button("Edit")
console_button = sg.Button("Console")
window = sg.Window('TODO APP',layout=
    [[label,input_box,add_button],
    [list_box, edit_button],
    [console_button]], 
    font = ('Helvetica', 14))

def console():
    
    load_config()
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
                print(f'Type {underline_text("unmark")} <<task #>> to unmark a task as completed.')
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

        elif user_action.startswith("unmark"):
            user_action = user_action.lstrip("un")
            title_bar(file_to_edit)
            mark_task(user_action, file_to_edit, mark = False)
                
        elif user_action.startswith("remove"):
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

        elif user_action.startswith("undo"):
            title_bar(file_to_edit)
            undo((get_undo_opt()), file_to_edit)

        elif user_action.startswith("exit"):
            save_config(file_to_edit, get_file_list())
            clear()
            break
        else:
            print("!!! Command not recognized. Type commands to see list of available commands !!!\n")
    print("Returning to GUI Mode")
def gui():
    global console_flag
    while True:
        event, values= window.read()
        print(event)
        print(values)
        match event:
            case "Add":
                add_task(values['todo'],file_to_edit, gui=True)
                todos = get_todos(file_to_edit)
                window['todo_list'].update(todos)
                window['todo'].update(value="")
            case "Edit":
                edit_task(values['todo_list'][0], file_to_edit, gui=True, new_edit = values['todo'])
                todos = get_todos(file_to_edit)
                window['todo_list'].update(todos)
                window['todo'].update(value="")
            case 'todo_list':
                window['todo'].update(value=values['todo_list'][0][4:])
            case 'Console':
                console()
            case sg.WIN_CLOSED:
                break
        if console_flag == True:
            console()
        else:
            gui()

gui()

window.close()



# if __name__ == "__main__":
#     main() 