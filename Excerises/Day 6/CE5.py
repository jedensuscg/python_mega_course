# Please download the three text files a.txt, b.txt, and c.txt from the resources. Then, create a program that reads each text file and prints out the content of each in the command line. The expected output would be like the following:

filelist = ["a.txt","b.txt","c.txt",]

for file in filelist:
    with open(file, "r") as file:
        string = file.read()
        print(string)