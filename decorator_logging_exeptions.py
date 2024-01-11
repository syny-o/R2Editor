from functools import wraps
from datetime import datetime

def logged_exc(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        result = None
        start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = function(*args, **kwargs)
        except Exception as ex:
            print(f"{start} -- {__name__}:{function.__name__} -- Argumenty: {args}, {kwargs}, Error: {ex}")
        
        return result
    
    return wrapper



# @logged_exc
def open_file(path):
    with open(path) as f:
        pass

@logged_exc
def divide(a, b):
    return a/b




# result = divide(5, 0)

open_file = logged_exc(open_file)
open_file("c:\\prdel.txt")
