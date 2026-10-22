
def validate_site(site):

    """
    Validate a base-station record and return True if valid.

    Check record is a dictionary -> check required key exists -> Validate individual field types -> validate eng constraints -> Return True .
    """

    if not isinstance(site, dict):
        raise ValueError ("ERROR: site must be a dictionary ")

    required_keys = ["site_name", "connected_users", "maximum_users", "is_online"]

    missing_keys = [key for key in required_keys if key not in site]

    if missing_keys:
        raise ValueError (f"Missing required fields: {missing_keys}")

    if not isinstance(site['site_name'], str):
        raise ValueError ("ERROR: site name must be a string")

    if not site['site_name'].strip():
        raise ValueError ("ERROR: Site name must not be empty")

    if type(site['connected_users']) is not int:
        raise ValueError ("ERROR: connected users must be an integer number")

    if site['connected_users'] < 0:
        raise ValueError ("ERROR: Connected users cannot be less than zero")

    if type(site['maximum_users']) is not int:
        raise ValueError ("ERROR: maximum users must be an integer number")

    if site['maximum_users'] <= 0:
        raise ValueError ("ERROR: maximum users cannot be zero or negative.")

    if type(site['is_online']) is not bool:
        raise ValueError ("ERROR: Online status must be True or False")

    return True
