def expand_flattened_dict(flattened_dictionary: dict) -> dict:
    """
    This function expands the flattened dicts in the format "a__b__c":value
    It recurses into every key and expands the dictionary.

    Example output:
    "a":{
        "b":{
            "c": value
        }
    }

    Returns:
        dictionary: normalized dictionary
    """

    expanded_dict = {}
    for k, v in flattened_dictionary.items():
        key = k.lstrip("\ufeff").replace('"', "")
        subkeys = key.split("__")

        def insert(key_stack, dictionary, data):
            for i, subkey in enumerate(key_stack):
                if len(key_stack) == 1:
                    dictionary[subkey] = data
                else:
                    if subkey not in dictionary:
                        dictionary[subkey] = {}

                    key_stack.pop(0)
                    insert(key_stack, dictionary[subkey], data)

        insert(subkeys, expanded_dict, v)
    return expanded_dict
