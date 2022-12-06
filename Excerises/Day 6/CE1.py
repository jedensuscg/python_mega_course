# Please download the essay.txt file from the resources of this article. Then, create a program that reads that file and prints out its text. 
# The first letter of each word in the output should be uppercase.

with open("essay.txt", "r") as file:
    text = file.read()
    print(text.title())