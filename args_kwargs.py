# Example list and dictionary to use as inputs
lst = ["apple", "banana", "cherry"]
person_info = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

def demo_function(*args, **kwargs):
    """
    Demonstrates the use of *args and **kwargs in a function.

    Parameters:
    *args : tuple
        A variable-length tuple of positional arguments.
    **kwargs : dict
        A variable-length dictionary of keyword arguments.

    This function prints the positional arguments and keyword arguments
    it receives, showing how *args collects extra positional arguments
    into a tuple, and **kwargs collects extra keyword arguments into a dictionary.
    """
    print("Positional arguments (*args) received:")
    for i, arg in enumerate(args):
        print(f"  Argument {i}: {arg}")

    print("\nKeyword arguments (**kwargs) received:")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

# Calling the function with multiple positional arguments and keyword arguments
demo_function(10, 20, 30, fruit="apple", color="red")

print("\n---\n")

# Using the list and dictionary with unpacking operators * and **

# *lst unpacks the list into positional arguments
# **person_info unpacks the dictionary into keyword arguments
demo_function(*lst, **person_info)
