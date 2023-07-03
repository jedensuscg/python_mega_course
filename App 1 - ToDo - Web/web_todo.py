import streamlit as st
import os
from functions import (
    underline_text, title_bar, format_input, add_task, 
    delete_task, edit_task, show_list, load_config, startup, add_new_file,
    get_todos, mark_task, remove_marked_tasks,
    show_options, undo, clear, get_undo_opt, show_file_menu, get_file_list, get_file_to_edit,
    format_filename, delete_file)

load_config()
todos = []
file_to_edit = startup()
todos = get_todos(file_to_edit)

# for todo in raw_todos:
#     todos.append(todo[4:])
    
working_directory = os.getcwd()
lastfile = ''

def display_todos():
    checkbox_key = 0
    for todo in todos:
        checkbox_key += 1
        value = True if todo[:3] == "[X]" else False
        todo = todo[4:]
        st.checkbox(todo, key=checkbox_key, on_change=change_marking, value=value, args=(checkbox_key, ))

def add_todo():
    todo = st.session_state["new_todo"]
    add_task(todo,file_to_edit)

def change_marking(list_key):
    item_to_mark = list_key - 1
    mark = st.session_state[list_key]
    mark_task(item_to_mark,file_to_edit, mark)

st.title("pyTODO")
st.subheader("The only note app you don't really need!")

display_todos()


st.text_input(label="",placeholder="Enter a new ToDo.", on_change=add_todo, key="new_todo")
st.session_state