import os
import magic

ALLOWED_EXTENSIONS = {'.txt', '.pdf'}
MAX_FILE_SIZE_MB = 200

def is_valid_file(file_path):
    if not os.path.isfile(file_path):
        return False, "Not a valid file"

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file extension: {ext}"
    
    file_type = magic.from_file(file_path, mime=True)
    if file_type not in {'text/plain', 'application/pdf'}:
        return False, f"Unsupported file content type: {file_type}"


    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File size {size_mb:.2f}MB exceeds {MAX_FILE_SIZE_MB}MB limit"

    return True, "OK"
