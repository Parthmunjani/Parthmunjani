from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from logg import logger
def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                identity = get_jwt_identity()
                print(identity)
                user_role_name = identity.get("role_name")  # Get the role name from the identity
                if user_role_name in allowed_roles:  # Check if the user's role name is in the allowed roles list
                    return func(*args, **kwargs)
                else:
                    return {'message': 'Permission denied'}, 403
            except Exception as e:
                return {'message': 'Authentication required'}, 401
        return wrapper
    return decorator

import time,functools

def measure_time(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        response = await func(*args, **kwargs)
        end_time = time.monotonic()
        logger.info(f'{func.__name__} took {end_time - start_time:.6f} seconds')
        return response
    return wrapper