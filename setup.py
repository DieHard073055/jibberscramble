from setuptools import setup, find_packages

setup(
    name="jibberscramble",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'python-gnupg>=0.4.7',
        'requests>=2.31.0'
    ],
    entry_points={
        'console_scripts': [
            'jibberscramble=cli:main',
        ],
    },
    author="Eshan Shafeeq",
    author_email="eshanshafeeq073055@gmail.com",
    description="A secure file encryption tool",
    license="MIT",
    keywords="encryption gpg compression",
    url="https://github.com/diehard073055/jibberscramble",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
