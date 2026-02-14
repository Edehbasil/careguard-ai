from app.schemas.checkin import HealthCheckCreate

check = HealthCheckCreate(employee_name="John", temperature="36.7")
print(check)
