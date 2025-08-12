# FTP
Enables FTP between server and client through an IP and port number. Current IP is set to 0.0.0.0 for testing purposes

## Steps to run:
Steps are assuming you are running a linux environment
IP address is hardcoded in `pythonserv.py`. Choose your own port number  
Requires python3.x 

1. Go to `/code/server` and run `python3 pythonserv.py <PORTNUMBER>`. Note: `python` is fine if your path is already configured to a python3.x version
2. In a separate terminal go to `/code/client` and run 
`python3 cli.py <IP_ADDRESS> <PORTNUMBER>` with the IP address and Port number specified when starting the server.
3. Once connected, commands supported are `get, put, ls, and quit`  