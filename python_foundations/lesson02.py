import sys

site_name = input("Enter the site name:")

while True:
    
    try:
        connected_users = int(input ("Enter connected users:"))
        if connected_users < 0:
            raise ValueError("Connected users cannot be negative.")
    except ValueError as error:
        print(f"ERROR: {error}")
        continue

    break


print(f"The no of connected users is {connected_users}")





