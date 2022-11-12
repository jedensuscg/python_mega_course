import sys

def format_input(input):
    return input.lower().strip()

todos = []
user_action = ''
while True:
    if len(todos) == 0:
        print("No ToDo list currently exists.")
        user_action = format_input(input("type add or exit\n"))
        match user_action:
            case 'add':
                user_prompt = "Enter a ToDo Task:\n"
                todo = input(user_prompt).capitalize()
                todos.append(todo)
            case 'exit':
                break
    else:
        user_action = format_input(input("type add, show, edit or exit\n"))
        match user_action:
            case 'add':
                user_prompt = "Enter a ToDo Task:\n"
                todo = input(user_prompt).capitalize()
                todos.append(todo)
            case 'show':
                print("** TODO LIST **")
                for item in todos:
                    print("-" + item)
                print("**End of TODO list.**")
            case 'edit':
                print("Select the number of the item to edit")
            case 'exit':
                break
print("Exiting")