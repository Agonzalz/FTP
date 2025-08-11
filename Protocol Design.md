
## Protocol Design

**Control Channel:** This connection remains persistent throughout the FTP session  and is used for sending commands and receiving responses 

**Data Channel**: This connection is temporarily established for each file transfer or directory listing and is used only for data transmission. 

### Message Types and Formats
- All messages will be sent as bytes of varying sizes.
- Will be converted to string before being sent as bytes to simplify transmission process. 
#### Control Channel Messages 
- Only commands will be sent from client to server through this channel. 
- ephemeral port number will also be sent through this channel
- ##### Commands from Client to Server
	- **'ls'**: list the files in the current directory on the server 
	- **'get < filename >'**:  Requests to download specified file from the server
	- **'put < filename >'**: Request to upload specified file to the server.
	- **quit**: Close the connection and end the session 

#### Data Channel Messages
- File and data transmission will occur in this channel
- ##### Responses from Server to Client 
	- ls: encoded string of directory listing is transferred
	- get: specified data file is sent  
	- put: server receives specified file
- ##### Transmission from Client to Server
	- 'put': client sends file through data channel 

### Protocol Procedures 
#### Establishing Connections 
1. Control Channel Setup
	- Client initiates connection to server on a specified port
		- socket.connect(SERVER_SOCKET)
	- Server accepts the connection and sends a greeting message 
#### Command Execution 
2. Processing Commands on the Control Channel
	- client sends a command
		- Control_channel.send(COMMAND)
	- Server receives the command and prepares a response 
		- Server_Socket.receive(COMMAND_DATA)
	- If the command is 'ls', the server lists directory contents and sends it back
	- If the command is 'get', or 'put', the server responds with readiness for a data connection
3. Data Channel Setup for 'get' or 'put' Commands:
	- Client prepares for data transfer and informs server of Ephemeral port creation
		- Control_Socket.send(COMMAND, EPHEMERAL_PORT)
	- Server connects to the client's data channel and begins data transmission 
		- Data_Socket.connect(CLIENT DATA SOCKET)
	- After completing file transfer, the data channel is closed.
		-  Data_SOCK.close()
	![[Pasted image 20240508233905.png]]
#### Terminating connection
4. Ending the Session:
	- Client send the command 'quit'.
	- Server closes the control socket, ending the session.

### Message Exchanges for File Transfer Setup 
- To download a file ('get'):
	- Client: 'get filename'
		- socket.send(COMMAND, FILENAME, DATA_PORT)
	- Server: creates data channel connection and sends the file through that channel
		- data_socket.connect(DATA_PORT)
		- data_socket.send(file)
- To upload a file('put'):
	- Client: sends 'put filename'
		- socket.send(COMMAND, FILENAME, DATA_PORT)
	- Server: creates data channel connection and waits for client to send the data 
		- data_socket.connect(DATA_PORT)
		- data_socket.recv(file)
