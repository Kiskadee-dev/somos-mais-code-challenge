from pydantic import BaseModel
from pydantic_core import Url


def flatten_pydantic(model: BaseModel) -> dict:
    """
    This function recurses into a pydantic model and flatten nested models

    Args:
        model (BaseModel): Some pydantic model derivade from BaseModel
    """
    dictionary = dict(model)

    def flatten(thing):
        for key, value in thing.items():
            if issubclass(type(value), BaseModel):
                thing[key] = dict(value)
                flatten(thing[key])
            elif issubclass(type(value), Url):
                thing[key] = str(value)

    flatten(dictionary)
    return dictionary
