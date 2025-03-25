import argparse
import os
import sys
import logging

from url_resolver import URLResolver
from key_manager import KeyManager
from compression import CompressionHandler
from encryption import EncryptionEngine

def setup_logging():
    """Configure basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('jibberscramble')

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='JibberScramble File Encryption Tool')
    
    # Common arguments
    parser.add_argument('--gnupghome', help='Path to GPG home directory')
    
    # Create subparsers for encrypt and decrypt commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a folder')
    encrypt_parser.add_argument('--url', help='bit.ly URL to fetch public key')
    encrypt_parser.add_argument('--public-key', help='Path to local public key file')
    encrypt_parser.add_argument('--compression', choices=['zip', 'tar.gz'], default='zip',
                              help='Compression method (default: zip)')
    encrypt_parser.add_argument('folder', help='Path to folder to encrypt')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('--private-key', required=True, 
                              help='Path to private key file')
    decrypt_parser.add_argument('--output-dir', help='Directory for decrypted output')
    decrypt_parser.add_argument('file', help='Path to encrypted file')
    
    return parser.parse_args()

def encrypt_folder(args, logger):
    """Encrypt a folder using a public key from a bit.ly URL or local file."""
    logger.info(f"Starting encryption process for folder: {args.folder}")
    
    # Step 1: Get the key data
    key_data = None
    if args.url:
        logger.info(f"Resolving URL: {args.url}")
        try:
            url_resolver = URLResolver()
            target_url = url_resolver.resolve_bitly(args.url)
            key_data = url_resolver.fetch_content(target_url)
            logger.info(f"Successfully fetched key from {target_url}")
        except ValueError as e:
            logger.error(f"URL resolution failed: {e}")
            return 1
    elif args.public_key:
        logger.info(f"Reading public key from file: {args.public_key}")
        try:
            with open(args.public_key, 'r') as f:
                key_data = f.read()
        except (FileNotFoundError, IOError) as e:
            logger.error(f"Failed to read public key file: {e}")
            return 1
    else:
        logger.error("Either --url or --public-key must be specified")
        return 1
    
    # Step 2: Import and validate the key
    key_manager = KeyManager(args.gnupghome)
    try:
        fingerprint = key_manager.import_key(key_data)
        logger.info(f"Imported public key with fingerprint: {fingerprint}")
    except ValueError as e:
        logger.error(f"Key import failed: {e}")
        return 1
    
    # Step 3: Compress the folder
    compressor = CompressionHandler(args.compression)
    try:
        compressed_path = compressor.compress(args.folder)
        logger.info(f"Compressed folder to: {compressed_path}")
    except ValueError as e:
        logger.error(f"Compression failed: {e}")
        return 1
    
    # Step 4: Encrypt the compressed folder
    encryptor = EncryptionEngine(key_manager)
    try:
        encrypted_path = encryptor.encrypt_file(compressed_path, fingerprint)
        logger.info(f"Encrypted file saved to: {encrypted_path}")
    except (ValueError, RuntimeError) as e:
        logger.error(f"Encryption failed: {e}")
        return 1
    finally:
        # Clean up the compressed file
        if os.path.exists(compressed_path):
            os.unlink(compressed_path)
    
    return 0

def decrypt_file(args, logger):
    """Decrypt a file using a private key."""
    logger.info(f"Starting decryption process for file: {args.file}")
    
    # Step 1: Import private key
    key_manager = KeyManager(args.gnupghome)
    try:
        fingerprint = key_manager.import_key_from_file(args.private_key)
        logger.info(f"Imported private key with fingerprint: {fingerprint}")
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"Key import failed: {e}")
        return 1
    
    # Step 2: Decrypt the file
    encryptor = EncryptionEngine(key_manager)
    try:
        decrypted_path = encryptor.decrypt_file(args.file)
        logger.info(f"Decrypted to temporary file: {decrypted_path}")
    except (ValueError, RuntimeError) as e:
        logger.error(f"Decryption failed: {e}")
        return 1
    
    # Step 3: Decompress the file
    output_dir = args.output_dir or os.path.dirname(args.file)
    compressor = CompressionHandler()
    try:
        final_path = compressor.decompress(decrypted_path, output_dir)
        logger.info(f"Decompressed content to: {final_path}")
    except ValueError as e:
        logger.error(f"Decompression failed: {e}")
        return 1
    finally:
        # Clean up the decrypted file
        if os.path.exists(decrypted_path):
            os.unlink(decrypted_path)
    
    return 0

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    logger = setup_logging()
    
    if args.command == 'encrypt':
        return encrypt_folder(args, logger)
    elif args.command == 'decrypt':
        return decrypt_file(args, logger)
    else:
        logger.error("No command specified. Use 'encrypt' or 'decrypt'.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
