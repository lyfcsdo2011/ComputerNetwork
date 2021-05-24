# ComputerNetwork

## 1 Developing a simple C/S Text Transmission program based on SOCKET
BY C, VS 2010.

Why? Because we are asked to use it in one of our experiments...

Develop a program based on TCP/IP protocol SOCKET, Client can send text from the standard input,

and the server can receive and display it on the standard output.

## 2 Concurrent Server
BY PYTHON.

On the basis of experiments 1, using the concurrent server mode, realize the server applet or app.  

Clients can send text, message, picture audio or video files concurrently to server.

You need to cross compile the codes on Linux to generate apk.

Choose the correct SDK and NDK. (I generated, but they can't run on my Android 10!)

## 3 MultiChattingRoom
BY PYTHON.
I completed a multi-chattingroom which can comunicate online with many people.

It includes some function belowed.
	
### 3.1 Monitor Process and Kill Process
	I realized this function by coding a single file killer.py to monitor and kill the process.

### 3.2 Updating Automatically
	After starting it, the program will get the configurations of Server and Client and compare them to judge if you need update or not.

	If you need update, the program will remind you to update, if you choose "YES", it will start killer.py to monitor and kill the running process.

### 3.3 Concurrent comunication
	The server will receive any messages including files from all clients, and resend to any other client.


I put the setting information in file Setting.py. If you want to know more details, you can refer to my report.