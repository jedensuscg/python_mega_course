# Create a program that:

# 1. Prompts the user to input a (dollar) amount.

# 2. Calculates the corresponding amount in euros, given an exchange rate of 0.95.

# 3. Prints out the amount in euros, as shown in the screenshot below.

rate = 0.95
amount = input("Input a dollar amount: ")
euro = float(amount) * 0.95
print("The amount in Euros is: " + str(euro))