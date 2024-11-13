def generate_token(data: int) -> str:
    import os
    return os.urandom(len(str(data))).hex()    