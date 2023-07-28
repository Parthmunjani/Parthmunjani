from pydantic import BaseModel, constr, validator

class OrderSchema(BaseModel):
    user_id: int
    payment_status: constr(max_length=200)
    address_id: int
    category_id: int
    total_price: float
    status: constr(max_length=20)
    
    @validator('user_id','address_id','category_id')
    def validate_id(value):
        if value <= 0:
            raise ValueError("ID must be a positive integer")
        return value
    
    @validator('payment_status')
    def validate_payment_status(payment_status):
        if not payment_status.strip():
            raise ValueError("Payment status cannot be empty or consist only of whitespace")
        return payment_status
    
    @validator('total_price')
    def validate_total_price(total_price):
        if total_price < 0:
            raise ValueError("Total price cannot be negative")
        return total_price
    
    @validator('status')
    def validate_status(status):
        if not status.strip():
            raise ValueError("Status cannot be empty or consist only of whitespace")
        return status
