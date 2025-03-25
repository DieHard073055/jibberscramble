import os
import zipfile
import tarfile
import tempfile

class CompressionHandler:
    def __init__(self, method='zip'):
        self.method = method
        
    def compress(self, folder_path):
        """Compress a folder into an archive."""
        if not os.path.isdir(folder_path):
            raise ValueError(f"Path {folder_path} is not a directory")
            
        # Create temporary file for the archive
        fd, temp_path = tempfile.mkstemp(suffix=f'.{self.method}')
        os.close(fd)
        
        base_name = os.path.basename(folder_path)
        if self.method == 'tar.gz':
            with tarfile.open(temp_path, 'w:gz') as tar:
                tar.add(folder_path, arcname=base_name)
        elif self.method == 'zip':
            with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                self._add_to_zip(zipf, folder_path, base_name)
        else:
            raise ValueError(f"Unsupported compression method: {self.method}")
            
        return temp_path
        
    def decompress(self, archive_path, output_dir):
        """Decompress an archive to the specified directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Detect archive type by content instead of extension
        with open(archive_path, 'rb') as f:
            magic_bytes = f.read(4)
        
        # ZIP files start with PK\x03\x04
        if magic_bytes.startswith(b'PK\x03\x04'):
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(output_dir)
        # TAR.GZ files start with \x1f\x8b\x08 (gzip magic number)
        elif magic_bytes.startswith(b'\x1f\x8b'):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(output_dir)
        else:
            raise ValueError(f"Unsupported archive format: {archive_path} (unknown file signature)")
        
        return output_dir
        
    def _add_to_zip(self, zipf, path, arc_path):
        """Add a file or directory to a zip file, preserving structure."""
        if os.path.isfile(path):
            zipf.write(path, arc_path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, os.path.dirname(path))
                    zipf.write(full_path, os.path.join(arc_path, rel_path))
