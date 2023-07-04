import streamlit as st
import os
from functions import (
    underline_text, title_bar, format_input, add_task, 
    delete_task, edit_task, show_list, load_config, startup, add_new_file,
    get_todos, mark_task, remove_marked_tasks,
    show_options, undo, clear, get_undo_opt, show_file_menu, get_file_list, get_file_to_edit,
    format_filename, delete_file)

load_config()
main = st.container()
debug = st.expander("Debug")

todos = []
file_to_edit = startup()
todos = get_todos(file_to_edit)
number_of_tasks = 0

# for todo in raw_todos:
#     todos.append(todo[4:])
    
working_directory = os.getcwd()
lastfile = ''

def log_action(msg, log_items = []):
    print(log_items)
    if len(log_items)  == 0:
        with debug:
            st.write(msg)
    else:
        with debug:
            st.write(msg)
            for item in log_items:
                st.write(f'...{item.replace("[X]","")}')

def display_todos():
    checkbox_key = 0
    for todo in todos:
        checkbox_key += 1
        value = True if todo[:3] == "[X]" else False
        todo = todo[4:]
        st.checkbox(todo, key=checkbox_key, on_change=change_marking, value=value, args=(checkbox_key, ))

def load_list():
    list_to_get = st.session_state['file_list']
    file_to_edit = st.session_state['file_list']
    show_file_menu(file_to_edit,gui=True)
    todos = get_todos(file_to_edit)
    print(todos)


def display_filelist():
    filelist = []

    for root, dirs, files in os.walk('./lists/'):
      for file in files:

             filelist.append(file)
    st.selectbox("Lists",filelist,key="file_list",on_change=load_list)



def add_todo():
    todo = st.session_state["new_todo"]
    add_task(todo,file_to_edit)
    st.session_state["new_todo"] = ""
    log_action(f'Added item: {todo}')


def change_marking(list_key):
    
    item_to_mark = list_key - 1
    mark = st.session_state[list_key]
    mark_task(item_to_mark,file_to_edit, mark)
    log_action(f'Marked/Unmakred item # {item_to_mark}')

def delete_marked():
    todos = get_todos(file_to_edit)
    log_items = []
    for index, todo in enumerate(todos):
        if st.session_state[str(index + 1)] == True:
            log_items.append(f'{index}:{todo}')
            del st.session_state[str(index + 1)]
    log_action("deleted marked items.", log_items)
    remove_marked_tasks(file_to_edit)

def create_list():
    log_action("CREATING LISTS NO YET AVAILABLE IN WEB VERSION")
            



with st.sidebar:

    st.subheader("The only note app you don't really need!")
    st.write("By James Edens")
    st.write("Github: [https://github.com/jedensuscg](https://github.com/jedensuscg)")
    st.divider()
    st.write("Menu")
    st.button("Delete Marked", key="delete_marked_button", on_click=delete_marked)
    display_filelist()
    st.button("Create List", key="create_list_button", on_click=create_list)


with main:
    st.title("pyTODO")
    st.subheader(f'Current List: {file_to_edit.replace(".txt","")}')
    st.divider()
    display_todos()

    st.text_input(label="Upload List", label_visibility='hidden', placeholder="Enter a new ToDo.", on_change=add_todo, key="new_todo")

with debug:
    st.write("Session State")
    st.session_state
    st.write('Session Log')