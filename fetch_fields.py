import json
from apitable import Apitable

access_token = 'uskr7IEUFGLArGCDjxjBmPH'
datasheet_id = 'dstTbH8nkfwx8qsfV0'

apitable = Apitable(access_token)
datasheet = apitable.datasheet(datasheet_id)
fields = datasheet.fields.all()

def custom_serializer(obj):
    """A custom serializer function that converts objects to dictionaries."""
    if hasattr(obj, "__dict__"):
        # Convert the object's dictionary, filtering out any non-serializable items.
        return {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

with open('fields.json', 'w') as file:
    for field in fields:
        # Use the custom_serializer function to handle non-serializable objects.
        json.dump(field, file, default=custom_serializer)
        file.write('\n')