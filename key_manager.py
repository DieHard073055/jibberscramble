import gnupg
import os
import tempfile
import shutil

class KeyManager:
    def __init__(self, gnupghome=None):
        if gnupghome is None:
            self.gnupghome = tempfile.mkdtemp()
            self.temp_dir = True
        else:
            self.gnupghome = gnupghome
            self.temp_dir = False
        
        self.gpg = gnupg.GPG(gnupghome=self.gnupghome)
    
    def __del__(self):
        if hasattr(self, 'temp_dir') and self.temp_dir:
            shutil.rmtree(self.gnupghome, ignore_errors=True)
    
    def import_key(self, key_data):
        """Import a GPG key from string data."""
        import_result = self.gpg.import_keys(key_data)
        if not import_result.fingerprints:
            raise ValueError("Invalid GPG key format")
        return import_result.fingerprints[0]
    
    def import_key_from_file(self, key_path):
        """Import a GPG key from a file."""
        with open(key_path, 'r') as f:
            key_data = f.read()
        return self.import_key(key_data)
    
    def validate_key(self, fingerprint, expected_type='pub'):
        """Validate that a key exists and is of the expected type."""
        keys = self.gpg.list_keys() if expected_type == 'pub' else self.gpg.list_keys(True)
        for key in keys:
            if key['fingerprint'] == fingerprint:
                return True
        return False
