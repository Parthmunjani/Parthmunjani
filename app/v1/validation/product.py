from pydantic import BaseModel, constr, validator

class Productschema(BaseModel):
    name: constr(max_length=50)
    price: int
    category_id: int
    
    @validator('name')
    def validate_name(cls, name):
        if not name.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return name
    
    @validator('price')
    def validate_price(cls, price):
        if price is not None and price < 0:
            raise ValueError("Price cannot be negative")
        return price

    @validator('category_id')
    def validate_category_id(cls, category_id):
        if not category_id:
            raise ValueError("Category ID cannot be empty")
        return category_id
