from pydantic import BaseModel
from typing import Optional

class HealthCheckCreate(BaseModel):
    employee_name: str
    temperature: str
    symptoms: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
