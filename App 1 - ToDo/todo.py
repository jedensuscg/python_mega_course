todos = []
user_action = ''
while True:
    if todos.length == 0:
        print("No ToDo list currently exists.")
        user_action = input("type add or exit")
        match user_action:
            case 'add':
                user_prompt = "Enter a ToDo Task:"
                todos = []
                todo = input(user_prompt)
                todos.append(todo)
            case 'exit':
                quit()
    else:
        user_action = "type add, show or exit"
        match user_action:
            case 'add':
                user_prompt = "Enter a ToDo Task:"
                todos = []
                todo = input(user_prompt)
                todos.append(todo)
            case 'show':
                print(todos)
            case 'exit':
                quit()