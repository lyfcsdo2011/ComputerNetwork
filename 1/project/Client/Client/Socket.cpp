#include "stdafx.h"
#include "Socket.h"
#include <iostream>
#include <string>
#include <WinSock2.h>
using namespace std;

bool InitialWSA(){
	WORD sockVersion = MAKEWORD(2, 2);					// version of winsock, that is winsock2
	WSADATA wsaData;									// store information about winsock returned by system
	return WSAStartup(sockVersion, &wsaData) == 0;		
}

SOCKET CreateSocket(){
	return 	socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);	// address family, connect, TCP
}

// Server
bool Bind(SOCKET Server, ULONG IP, int port){
	sockaddr_in in;
	in.sin_family = AF_INET;
	in.sin_port = htons(port);							// Converts a 16 bit byte order from host to network
	in.sin_addr.S_un.S_addr = IP;						
	return bind(Server, (LPSOCKADDR)&in, sizeof(in)) != SOCKET_ERROR;
}

// Server
bool Listen(SOCKET Server){
	return listen(Server, 10) != SOCKET_ERROR;			// max = 10;
}

// Server
SOCKET AcceptConnect(SOCKET Server){
	SOCKET Client;
	sockaddr_in ClientAddr;
	int LenOfAddr = sizeof(ClientAddr);
	cout << "Please Wait for connection..." << endl;
	Client = accept(Server, (SOCKADDR*)&ClientAddr, &LenOfAddr);
	if(Client == INVALID_SOCKET){
		cout << "ACCEPT ERROR!" << endl;
		return 0;
	}
	cout << "Accept a connection:" << inet_ntoa(ClientAddr.sin_addr) << endl;
	return Client;
}

// Client
bool Connect(SOCKET Client, char* IP, int port){
	sockaddr_in serverAddr;
	int SIZE = sizeof(serverAddr);
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(port);
	serverAddr.sin_addr.S_un.S_addr = inet_addr(IP);		// function of inet_addr is to exchange char* to ULONG
	return connect(Client, (sockaddr*)&serverAddr, SIZE) != SOCKET_ERROR;
}

// Server
void Recieve(SOCKET Client){
	char revData[255];
	while(true){
		int ret = recv(Client, revData, 255, 0);					// recieve
		if(ret > 0){	
			revData[ret] = 0x00;
			cout << "Message comes from Client:" << revData <<endl;
		}
		// acknowledge
		char* sendData = "Send success! \n\n";
		send(Client, sendData, strlen(sendData), 0);
	}
}

// Client
void Send(SOCKET Client){
	while(true){
		char *sendData = new char[255];
		cout << "Please input the message you want to send:";
		cin.getline(sendData,255);
		send(Client, sendData, strlen(sendData), 0);
		char recData[255];
		int ret = recv(Client, recData, 500, 0);
		if(ret > 0){
			recData[ret] = 0x00;
			cout << recData << endl;
		}
	}
}

void Close(SOCKET Server){
	closesocket(Server);
	WSACleanup();
}