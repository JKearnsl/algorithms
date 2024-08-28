
def chunk_string(input_string: str, chunk_size: int) -> str:
    for i in range(0, len(input_string), chunk_size):
        yield input_string[i:i + chunk_size]