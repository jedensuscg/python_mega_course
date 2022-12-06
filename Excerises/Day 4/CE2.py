# The list below represents the ranking of three athletes. John won 1st place, Sen got 2nd, and Lisa the 3rd.

# ranking = ['John', 'Sen', 'Lisa']

# Create a program that:

# 1. Contains the above list.

# 2. Prompts the user to input a rank number.

# 3. Returns the person who has the given rank.

ranking = ['John', 'Sen', 'Lisa']

rank = int(input("Enter a class rank number: ")) - 1

print (ranking[rank])