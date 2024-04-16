from config import ALLOWED_FILE_TYPES

def is_file_type_allowed(file_type: str) -> bool:
    return file_type in ALLOWED_FILE_TYPES