from functools import wraps
from datetime import datetime

def logged_exc(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        result = None
        start = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        try:
            result = function(*args, **kwargs)
        except Exception as ex:
            log_file_name = f"error_log_{start}.txt"
            error_text = (f"{start} -- {__name__}:{function.__name__} -- Arguments: {args}, {kwargs}, Error: {ex}")
            with open(log_file_name, "w") as f:
                f.write(error_text)
            raise
        return result
    
    return wrapper



# @logged_exc
# def open_file(path):
#     with open(path) as f:
#         pass

# @logged_exc
# def divide(a, b):
#     return a/b




# # result = divide(5, 0)

# open_file = logged_exc(open_file)
# open_file("c:\\prdel.txt")
