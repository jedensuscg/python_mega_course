# usernames = ["john 1990", "alberta1970", "magnola2000"]

# Extend the code above so the code prints out a list containing the number of characters for each username.

# The output of your code should be as below:

# [9, 11, 11]

usernames = ["john 1990", "alberta1970", "magnola2000"]

usernames = [len(name) for name in usernames]

print(usernames)