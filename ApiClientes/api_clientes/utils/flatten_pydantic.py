from pydantic import BaseModel


def flatten_pydantic(model: BaseModel, by_alias: bool = False) -> dict:
    """
    This function recurses into a pydantic model and flatten nested models

    Args:
        model (BaseModel): Some pydantic model derivade from BaseModel
    """
    dictionary = model.model_dump(by_alias=by_alias)

    def flatten(thing):
        for key, value in thing.items():
            if issubclass(type(value), BaseModel):
                thing[key] = value.model_dump(by_alias=by_alias)
                flatten(thing[key])

    flatten(dictionary)
    return dictionary
