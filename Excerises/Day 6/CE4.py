# Create a program that generates multiple text files by iterating over the filenames list. The text Hello should be written inside each generated text file.

filelist = ["list1.txt", "list2.txt", "list3.txt"]

for file in filelist:
    with open(file, "w+") as file:
        file.write("Hello")