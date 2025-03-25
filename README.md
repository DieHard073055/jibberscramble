# JibberScramble

A secure file encryption tool that combines GPG encryption with folder compression, supporting both URL-based and local public key encryption.

## Features

- Secure file encryption using GPG
- Folder compression (ZIP and TAR.GZ)
- Support for both URL-based and local public key encryption
- Command-line interface for easy use
- Secure temporary file handling
- Comprehensive error handling and validation

## Installation

You can install JibberScramble using pip:

```bash
pip install jibberscramble
```

Or install from source:

```bash
git clone https://github.com/DieHard073055/jibberscramble.git
cd jibberscramble
pip install .
```

## Usage

### Encrypting Files

You can encrypt files using either a public key from a URL or a local public key file.

Using a URL (e.g., bit.ly URL):

```bash
jibberscramble encrypt --url https://bit.ly/your-pgp-key ~/Documents/sensitive
```

Using a local public key file:

```bash
jibberscramble encrypt --public-key ~/keys/public_key.asc ~/Documents/sensitive
```

### Decrypting Files

Decrypt files using your private key:

```bash
jibberscramble decrypt --private-key ~/keys/private_key.asc ~/Documents/sensitive.zip.gpg
```

### Options

- `--compression`: Specify compression method (zip or tar.gz, default: zip)
- `--output-dir`: Specify output directory for decrypted files
- `--gnupghome`: Specify GPG home directory

## Security Features

- Uses GPG for strong encryption
- Secure temporary file handling
- Input validation and error checking
- Secure key management
- File format detection using magic bytes

## Requirements

- Python 3.8+
- python-gnupg
- requests

## Development

To run tests:

```bash
pip install pytest
python -m pytest tests/
```

## License

MIT License

Copyright (c) 2025 Eshan Shafeeq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
