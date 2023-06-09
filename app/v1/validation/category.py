from pydantic import BaseModel, constr, root_validator
from typing import List

class CategorySchema(BaseModel):
    id: int
    name: constr(max_length=50, strip_whitespace=True)
    parent_id: int
    children: List['CategorySchema']
    sub_category: List['CategorySchema']
    
    @root_validator(pre=True)
    def validate_fields(cls,values):
        for field_name, value in values.items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{field_name} cannot be empty")
        return values
