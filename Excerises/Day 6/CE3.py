# Please download the members.txt file from the resources of this article.

# Then, create a program that, whenever executed, asks the user to enter a new member in the command line:


# Then, the member is added to members.txt. In this case, the text file content would be:

# John Smith

# Sen Lakmi

# Sono Octonot

# Solomon Right

name = input("Add a new member: ")

with open("members.txt", "a") as file:
    file.writelines("\n" + name)