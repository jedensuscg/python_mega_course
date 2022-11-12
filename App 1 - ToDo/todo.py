import sys


todos = []
user_action = ''
while True:
    if len(todos) == 0:
        print("No ToDo list currently exists.")
        user_action = input("type add or exit").lower()
        match user_action:
            case 'add':
                user_prompt = "Enter a ToDo Task:"
                todo = input(user_prompt).capitalize()
                todos.append(todo)
            case 'exit':
                sys.exit()
    else:
        user_action = input("type add, show or exit").lower()
        match user_action:
            case 'add':
                user_prompt = "Enter a ToDo Task:"
                todo = input(user_prompt).capitalize()
                todos.append(todo)
            case 'show':
                print(todos)
            case 'exit':
                sys.exit()