import pickle


def serialize(obj: any) -> bytes:
    return pickle.dumps(obj)


def deserialize(byte_string: bytes) -> any:
    try:
        return pickle.loads(byte_string)
    except (pickle.UnpicklingError, ValueError):
        return object()


def save_obj_to_file(obj: any, file_name: str):
    with open(file_name, 'wb') as file:
        file.write(serialize(obj))


def load_obj_from_file(file_name: str) -> any:
    with open(file_name, 'rb') as file:
        return deserialize(file.read())
