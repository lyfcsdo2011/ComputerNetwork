// Client.cpp : �������̨Ӧ�ó������ڵ㡣
//
/***** winsock c/s�������̣��ͻ��ˣ�*******
			1.��ʼ��WSA
			2.����socket
			3.���ӵ�������
			4.���ͺͽ�������
			5.�Ͽ�����
******************************************/

#include "stdafx.h"
#include "stdafx.h"
#include "Socket.h"
#include <iostream>
#include <stdio.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")
using namespace std;

int main(){
	int port = 8080;				// set port
	char* IP = "127.0.0.1";			// set IP
	// 1.initial WSA
	bool flag1 = InitialWSA();
	if(!flag1)	return 0;

	// 2.Create socket
	SOCKET Client = CreateSocket();
	if(Client == INVALID_SOCKET){
		cout << "SOCKET ERROR!" << endl;
		return 0;
	}

	// 3.Connect
	bool flag2 = Connect(Client, IP, port);
	if(!flag2){
		cout << "CONNECT ERROR!" << endl;
		Close(Client);
		return 0;
	}else cout << "Connect success!" << endl;

	// 4.send and recieve
	Send(Client);

	// 5.close
	closesocket(Client);
	WSACleanup();
	return 0;
}

