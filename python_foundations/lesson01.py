import sys

site_name = input("Enter the site name:")
try:
    connected_users = int(input ("Enter connected users:"))
    if connected_users < 0:
        raise ValueError("Connected users cannot be negative.")
except ValueError as error:
    print(f"ERROR: {error}")
    sys.exit(1)

try:
    maximum_users = int(input("Enter the maximum users:"))
    if maximum_users <= 0:
        raise ValueError("ERROR: Please enter a valid non-negative and non-zero whole number.")
except ValueError as error:
    print(f"ERROR: {error}")
    sys.exit(1)

try:
    online_answer = input("Is the site online? (yes/no):").strip().lower()
    if online_answer != "yes" and online_answer != "no":
        raise ValueError("ERROR: online status is either yes or no.")
except ValueError as error:
    print(f"ERROR: {error}")
    sys.exit(1)

try:
    signal_power = float(input ("Enter received signal power (dBm):"))
except ValueError as error:
    print(f"Please enter a valid floating-point number for power in dB: {error} ")
    sys.exit(1)

is_online = online_answer == "yes"

utilization = (connected_users/maximum_users) * 100
aditional_users = maximum_users - connected_users
high_utilization = utilization >= 80
has_capacity = aditional_users >= 1
needs_attention = not is_online or high_utilization
site_healthy = is_online and not high_utilization
over_capacity = connected_users > maximum_users

if not is_online:
    print("\nCRITICAL: Base station offline")
elif high_utilization:
    print("\nWARNING: High site utilization")
else:
    print("\nNORMAL: Base station operating normally")

print("\nThe base station parameters are as follows:")
print (f"The cell tower name is {site_name}")
print(f"The no of connected users is {connected_users}")
print(f"The received signal power in dBm is : {signal_power} dBm")
print(f"Online status: {is_online}")
print(f"Site utilization: {utilization:.2f}%")
print(f"Aditonal users to accomodate: {aditional_users}")
print(f"Has capacity: {has_capacity}")
print(f"The site needs attention: {needs_attention}")
print(f"Site healthy: {site_healthy}")
print(f"Over capacity: {over_capacity}")



