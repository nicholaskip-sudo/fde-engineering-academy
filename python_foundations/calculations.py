def calculate_utilization ( connected_users,  max_users):
    """ Returns utilization percentage"""

    if max_users <= 0:
        raise ValueError("Maximum users cannot be zero or less.")
    
    utilization = (connected_users / max_users) * 100

    return utilization


