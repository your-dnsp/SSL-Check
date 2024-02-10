# SSL-check
I needed a script to regularly check my friend's website to troubleshoot issues with DNS and SSL certs.
There are many ways this could be accomplished, but I decided to write a python script instead. 

## Install some packages into your python environment
pip install dnspython

## Usage
Currently this script is designed to answer websites one by one. There could be a way to do multiple, but that wasn't needed for this use case. 
Execute the python script, provide a URL, and receive the results in the terminal. 

_python3 sslc.py_
