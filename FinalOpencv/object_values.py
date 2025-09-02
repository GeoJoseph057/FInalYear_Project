# object_values.py
# This file contains value assignments for different objects
# Format: object_name: value (1-4)

object_values = {
    "bottle": 1,
    "cup": 1,
    "cell phone": 2,
    "book": 2,
    "keyboard": 3,
    "mouse": 3,
    "laptop": 4,
    "remote": 4,
    "bowl": 1,
    "apple": 1,
    "banana": 1,
    "orange": 1,
    "tv": 4,
    "scissors": 3,
    "toothbrush": 2,
    "clock": 2,
    "microwave": 3,
    "vase": 2,
    "fork": 1,
    "spoon": 1,
    "knife": 1
    # Add more objects as needed
}

# Default value for objects not in the dictionary
default_value = 1

def get_object_value(object_name):
    """Return the value for an object, or the default value if not found"""
    return object_values.get(object_name.lower(), default_value)