"""
Comprehensions - filtering and transformation.
use conditions to filter, use functions to transform.
Transformation: Determines what value is placed into the output list.
Filtering: Determines whether a value is included.

"""

from python_foundations.calculations import calculate_utilization

def main():

    user_counts = [0, 50, 150, 200, 225, 250, 300]
    maximum_users = 250

    utilizations = [ calculate_utilization(user,maximum_users) for user in user_counts ]

    high_utilizations = [utilization for utilization in utilizations if utilization >= 80.0]

    overcapacity_utilizations = [utilization for utilization in utilizations if utilization > 100]

    high_usage_users = [user for user in user_counts if calculate_utilization(user, maximum_users)>=80.0]

    print("\nAll utilizations")
    print(utilizations)
    print("\nHigh utilizations")
    print(high_utilizations)
    print("\nOvercapacity utilizations")
    print(overcapacity_utilizations)
    print("\nHigh usage users")
    print(high_usage_users)


if __name__ == "__main__":
    main()