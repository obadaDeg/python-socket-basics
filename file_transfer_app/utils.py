from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def hash_file(file_paht):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    
    with open(file_paht, 'rb') as f:
        while chunk := f.read(4096):
            digest.update(chunk)
            
    hash_bytes = digest.finalize()
    return hash_bytes.hex()