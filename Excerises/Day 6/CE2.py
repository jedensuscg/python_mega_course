# Write a program that reads the essay.txt file and returns the number of characters contained in the file.

with open("essay.txt", "r") as file:
    string = file.read()
    print(len(string))