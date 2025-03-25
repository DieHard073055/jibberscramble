import os
import gnupg
import tempfile

class EncryptionEngine:
    def __init__(self, key_manager):
        self.key_manager = key_manager
        self.gpg = key_manager.gpg
        
    def encrypt_file(self, file_path, recipient_fingerprint):
        """Encrypt a file using the specified public key."""
        if not os.path.isfile(file_path):
            raise ValueError(f"Path {file_path} is not a file")
            
        if not self.key_manager.validate_key(recipient_fingerprint, 'pub'):
            raise ValueError(f"Invalid public key fingerprint: {recipient_fingerprint}")
            
        output_path = f"{file_path}.gpg"
        
        with open(file_path, 'rb') as f:
            status = self.gpg.encrypt_file(
                f, recipients=[recipient_fingerprint],
                output=output_path,
                always_trust=True
            )
            
        if not status.ok:
            raise RuntimeError(f"Encryption failed: {status.status}")
            
        return output_path
        
    def decrypt_file(self, file_path):
        """Decrypt a file using the available private key."""
        if not os.path.isfile(file_path):
            raise ValueError(f"Path {file_path} is not a file")
            
        # Create a temporary file for decrypted content
        fd, temp_path = tempfile.mkstemp()
        os.close(fd)
        
        with open(file_path, 'rb') as f:
            status = self.gpg.decrypt_file(
                f, output=temp_path
            )
            
        if not status.ok:
            os.unlink(temp_path)
            raise RuntimeError(f"Decryption failed: {status.status}")
            
        return temp_path
