#!python3
from setuptools import setup

setup(
    name="pyreq",
    version="1.0.1",
    
    description='A console based http client',
    long_description=open("README.rst").read(),

    url="https://github.com/BookOwl/pyreq",
    author="Matthew (BookOwl)",
    author_email="None",

    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Utilities",
        ],
    keywords='web http https curl',

    install_requires=["requests>=2.8,<3",],

    py_modules=["pyreq"],

    entry_points={
    'console_scripts': [
        'pyreq=pyreq:main',
        ],
    },
)
    
