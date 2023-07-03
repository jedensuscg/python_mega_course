import streamlit as st
import os
from functions import (
    underline_text, title_bar, format_input, add_task, 
    delete_task, edit_task, show_list, load_config, startup, add_new_file,
    get_todos, mark_task, remove_marked_tasks,
    show_options, undo, clear, get_undo_opt, show_file_menu, get_file_list, get_file_to_edit,
    format_filename, delete_file)

load_config()
file_to_edit = startup()
todos = get_todos(file_to_edit)
working_directory = os.getcwd()
lastfile = ''

st.title("pyTODO")
st.subheader("The only note app you don't really need!")

for todo in todos:
    st.checkbox(todo)

st.text_input(label="",placeholder="Enter a new ToDo.")