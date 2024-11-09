def all_thing_is_obj(object: any) -> int:
    if isinstance(object, list):
        print(f"List : {type(object)}", end="\n")
    elif isinstance(object, tuple):
        print(f"Tuple : {type(object)}", end="\n")
    elif isinstance(object, set):
        print(f"Set : {type(object)}", end="\n")
    elif isinstance(object, dict):
        print(f"Dict : {type(object)}", end="\n")
    elif isinstance(object, str):
        print(f"{object} is in the kitchen", end="\n")
    else:
        print("type not found", end="\n")
    return 42
