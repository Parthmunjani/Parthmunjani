from pydantic import BaseModel, constr, validator

class UserAddressSchema(BaseModel):
    user_id: int
    street: constr(max_length=200)
    state: constr(max_length=50)
    zip: constr(regex=r"^\d{4,7}$")
    
    @validator('user_id')
    def validate_user_id(cls, user_id):
        if not user_id:
            raise ValueError("User ID cannot be empty")
        return user_id
    
    @validator('street')
    def validate_street(cls, street):
        if not street.strip():
            raise ValueError("Street cannot be empty or consist only of whitespace")
        return street
    
    @validator('state')
    def validate_state(cls, state): 
        if not state.strip():
            raise ValueError("State cannot be empty or consist only of whitespace")
        return state