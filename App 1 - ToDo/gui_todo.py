from functions import (
    underline_text, title_bar, format_input, add_task, 
    delete_task, edit_task, show_list, load_config, startup, 
    get_todos, mark_task, remove_marked_tasks,
    show_options, undo, clear, get_undo_opt, show_file_menu, get_file_list, get_file_to_edit,
    format_filename)

import PySimpleGUI as sg
import os
console_flag = False
exit_flag = False
debug_flag = False
load_config()
file_to_edit = startup()
todos = get_todos(file_to_edit)
working_directory = os.getcwd()

#Setup GUI elements
sg.theme('Dark Blue')
label = sg.Text("Type in a ToDo", key='label')
input_box = sg.InputText(tooltip="Enter ToDo", key="todo")
add_button = sg.Button("Add", key='add')
list_box = sg.Listbox(values = get_todos(file_to_edit), key="todo_list", 
    enable_events=True, size=[40,20])
edit_button = sg.Button("Edit Task", key="edit")
delete_button =sg.Button("Delete Task", key="delete")
mark_button = sg.Button('Mark Complete', key='mark')
console_button = sg.Button("Console")
debug_toggle = sg.Checkbox('Print Debug Messages to console', key='debug')
remove_marked_button = sg.Button('Remove Marked', key='remove')
undo_button = sg.Button('Undo Last', key='undo')
msg_text = sg.Text('', key='msg')
file_text = sg.Text(format_filename(file_to_edit) ,key='file_open')
file_button = sg.FileBrowse('Browse',initial_folder='./lists/',file_types=[("txt Files","*.txt")])
file_input = sg.InputText(key='-FILE_PATH-')
file_open_button = sg.Button('Open',key='open_file')
create_list_button = sg.Button('Create New List',key='create_list')
exit_button =sg.Button('QUIT', key='-QUIT-',button_color="Red")
top_row = [[label,input_box,add_button],[file_text],[file_input,file_button, file_open_button],[create_list_button]]

list_col = [[list_box],[msg_text],[console_button, debug_toggle]]

button_col = [[edit_button],[delete_button],[mark_button],[remove_marked_button],[undo_button]]

console_layout = [[sg.Text("RUNNING IN CONSOLE MODE")],
    [sg.Text("Type exit in console to return to GUI mode.")]]

layout = [[ top_row ,sg.Column(list_col, key="-COL2-"),
            sg.Column(button_col, key="-COL3-"),sg.Column(console_layout, visible = False, key="-COL4-")]]
window = sg.Window('TODO APP',layout, 
    font = ('Helvetica', 14))

layout = 1

def console(file_to_edit):    
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
            global list_box
            clear()
            break
        else:
            print("!!! Command not recognized. Type commands to see list of available commands !!!\n")
    print("Returning to GUI Mode")

def gui():
    global console_flag
    global file_to_edit
    while True:
        event, values= window.read()
        try:
            if values['debug'] == True:
                print(f'Debug Start\nEvent Captured: {event}')
                print('Values of Event Captured')
                for key,value in values.items():
                    print(f'    {key} : {value}')
                print('End Debug')
        except:
            pass
        match event:
            case "add":
                window['msg'].update(value='')
                if values['todo'] == '':
                    print('DEBUG: Can not add blank ToDo')
                    window['msg'].update(value='Can not add blank ToDo')
                else:
                    add_task(values['todo'],file_to_edit, gui=True)
                    todos = get_todos(file_to_edit)
                    window['todo_list'].update(todos)
                    window['todo'].update(value="")
            case "edit":
                window['msg'].update(value='')
                if not values['todo_list']:
                    print('DEBUG: Nothing Selected to edit')
                    window['msg'].update(value='Nothing selected to edit!')
                elif values['todo'] == '':
                    print('DEBUG: Edit text is blank!')
                    window['msg'].update(value='Edit text is blank!')
                else:
                    edit_task(values['todo_list'][0], file_to_edit, gui=True, new_edit = values['todo'])
                    todos = get_todos(file_to_edit)
                    window['todo_list'].update(todos)
                    window['todo'].update(value="")
            case "delete":
                window['msg'].update(value='')
                if not values['todo_list']:
                    print('DEBUG: Nothing Selected to delete')
                    window['msg'].update(value='Nothing selected to delete!')
                else:
                    delete_task(values['todo_list'][0], file_to_edit, gui=True)
                    todos = get_todos(file_to_edit)
                    window['todo_list'].update(todos)
                    window['todo'].update(value="")
            case 'mark':
                window['msg'].update(value='')
                if not values['todo_list']:
                    print('DEBUG: Nothing Selected to mark')
                    window['msg'].update(value='Nothing selected to mark!')
                else:
                    mark_task(values['todo_list'][0], file_to_edit, gui=True)
                    todos = get_todos(file_to_edit)
                    window['todo_list'].update(todos)
                    window['todo'].update(value="")
            case 'remove':
                window['msg'].update(value='')
                clicked = sg.PopupYesNo('Confirm deletion of ALL Marked [X] tasks?')
                if clicked == 'Yes':
                    remove_marked_tasks(file_to_edit, gui=True, confirm=True)
                    todos = get_todos(file_to_edit)
                    window['todo_list'].update(todos)
                    window['todo'].update(value="")
                else:
                    pass
            case 'undo':
                undo(get_undo_opt(),file_to_edit, gui = True)
                todos = get_todos(file_to_edit)
                window['todo_list'].update(todos)
                window['todo'].update(value="")
                window['msg'].update(value='Completed UNDO command. Hit UNDO again to REDO')
            case 'todo_list':
                window['msg'].update(value='')
                try:
                    window['todo'].update(value=values['todo_list'][0][4:])
                except IndexError:
                    pass
            case 'open_file':
                if values['-FILE_PATH-'] == '':
                    window['-FILE_PATH-'].update('Please Select File')
                else:
                    try:
                        file_to_edit = values['-FILE_PATH-'].split("/lists/",1)[1]
                    except IndexError:
                        window['file_open'].update("Invalid List")
                    todos = get_todos(file_to_edit)
                    window['todo_list'].update(todos)
                    file_name = format_filename(file_to_edit)
                    window['file_open'].update(file_name)
                    show_file_menu(file_to_edit, gui=True)
            case 'create_list':
                list_name = sg.popup_get_text('Enter a name for the list',title='Create List')
                file_to_edit = list_name + ".txt"
                todos = get_todos(file_to_edit)
                window['todo_list'].update(todos)
                file_name = format_filename(file_to_edit)
                window['file_open'].update(file_name)
                show_file_menu(file_to_edit, gui=True)
            case 'Console':
                window[f'-COL2-'].update(visible=False)
                window[f'-COL3-'].update(visible=False)
                window['todo'].update(visible=False)
                window['add'].update(visible=False)
                window['label'].update(visible=False)
                window[f'-COL4-'].update(visible=True)
                console(file_to_edit)
                load_config()
                file_to_edit = startup()
                file_open = format_filename(file_to_edit)
                todos = get_todos(file_to_edit)
                window[f'-COL2-'].update(visible=True)
                window[f'-COL3-'].update(visible=True)
                window['todo'].update(visible=True)
                window['add'].update(visible=True)
                window['label'].update(visible=True)
                window[f'-COL4-'].update(visible=False)
                window['todo_list'].update(todos)
                window['file_open'].update(file_open)
            case sg.WIN_CLOSED:
                break
        
def format_filename(filename):
        name = f'List Open: {filename.replace("_", " ").title()[:-4]}'
        return name


gui()

window.close()



# if __name__ == "__main__":
#     main() 