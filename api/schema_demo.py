from api.schemas import SiteResponse
from pydantic import ValidationError

# 1. Valid coercion from a raw dictionary
site_A = SiteResponse.model_validate({
    "site_name": "OULU_BTS_003",
    "utilization": "80.0",
    "status": "CRITICAL",
})

print(site_A.status)
print(site_A.utilization)
print(site_A.model_dump())
print(type(site_A))
print(site_A.model_dump()["utilization"])
print(type(site_A.utilization))

# 2. Invalid data validation
try:
    site_B = SiteResponse.model_validate({
        "site_name": "OULU_BTS_004",
        "utilization": "unknown",
        "status": "WARNING",
    })
    print(site_B.status)
except ValidationError as error:
    print(f"Validation error: {error}")
