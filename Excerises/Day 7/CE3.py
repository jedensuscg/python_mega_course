# user_entries = ['10', '19.1', '20']
# Extend the code above so the code prints out a list containing the same items as floats.

# The output of your code should be as below:

# [10.0, 19.1, 20.0]

user_entries = ['10', '19.1', '20']

user_entries = [float(user) for user in user_entries]

print(user_entries)