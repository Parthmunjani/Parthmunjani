from pydantic import BaseModel, constr, EmailStr, validator


class Userschema(BaseModel):
    name: constr(max_length=255)
    email: EmailStr
    password: constr(max_length=255)
    phone_number: constr(max_length=20)
        
    @validator("name")
    def validate_name(cls, name):
        if not name.isalpha():
            raise ValueError("Name must only contain alphabetical characters")
        return name

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password
    
    @validator("phone_number")
    def validate_phone_number(cls, phone_number):
        if not phone_number.startswith("+"):
            raise ValueError("Phone number must start with a '+' sign")
        return phone_number
