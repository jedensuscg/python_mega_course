# We have the same list:

# ranking = ['John', 'Sen', 'Lisa']

# This time you need to create a program that:

# 1. Contains the above list.

# 2 Prompts the user to input the person's name.

# 3. Returns the rank that person has.

ranking = ['John', 'Sen', 'Lisa']

name = (input("Enter a name to get class rank: "))

print(ranking.index(name) + 1)