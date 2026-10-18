
def calculate_utilization ( connected_users,  max_users):
    """ Returns utilzation percentage"""
    utilization = (connected_users / max_users) * 100

    return utilization


site = {
    "site_name": "OULU_BTS_001",
    "connected_users": 215,
    "maximum_users": 250,
    "signal_power" : -68.5,
    "is_online": True
}

print(len(site))
print(site)

print(site["site_name"])
print(site["connected_users"])
site["connected_users"] = 200
site["location"] = "Oulu"

print(site)
print(len(site))

utilization = calculate_utilization(site["connected_users"], site["maximum_users"])
print(f"Calculated utilization: {utilization:.2f}")


