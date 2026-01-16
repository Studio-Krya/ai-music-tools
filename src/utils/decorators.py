from functools import wraps
import time

def throttle(interval: float):
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_called[0] >= interval:
                last_called[0] = current_time
                return func(*args, **kwargs)
            return None
        
        return wrapper
    return decorator

def async_throttle(interval: float):
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - last_called[0] >= interval:
                last_called[0] = current_time
                return await func(*args, **kwargs)
            return None
        return wrapper
    return decorator