
def calculate_utilization ( connected_users,  max_users):
    """ Returns utilzation percentage"""
    utilization = (connected_users / max_users) * 100

    return utilization

def calculate_remaining_capacity (connected_users, maximum_users):
    """ Returns remaining user capacity, never below zero"""
    remaining_capacity = max(0, maximum_users - connected_users)

    return remaining_capacity

def is_high_utilization (utilization, threshold):
    """ Boolean indicating whether utilization is at least the threshold"""
    is_high = utilization>=threshold

    return is_high

user_counts = [150, 225, 200, 300]
maximum_users = 250
threshold = 80

for user in user_counts:
    utilization = calculate_utilization(user,maximum_users)
    rem_capacity = calculate_remaining_capacity(user,maximum_users) 
    high_utilization = is_high_utilization(utilization, threshold)
    print(f"\nConnected users: {user}")
    print(f"Utilization: {utilization:.2f}%")
    print(f"Remaining capacity: {rem_capacity}")
    print(f"High utilization: {high_utilization}")




