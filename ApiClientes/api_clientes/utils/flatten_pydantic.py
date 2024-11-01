from pydantic import BaseModel


def flatten_pydantic(model: BaseModel, by_alias: bool = False) -> dict:
    """
    Dumps the pydantic model

    Args:
        model (BaseModel): Some pydantic model derivade from BaseModel
    """
    return model.model_dump(by_alias=by_alias)
