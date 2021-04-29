// Server.cpp : �������̨Ӧ�ó������ڵ㡣
//
/***** winsock c/s�������̣���������*******
			1.��ʼ��WSA
			2.����socket
			3.��socket�Ͱ󶨶�Ӧ�˿�
			4.����
			5.��������
			6.���ͺͽ�������
			7.�Ͽ�����
******************************************/

#include "stdafx.h"
#include <iostream>
#include <stdio.h>
#include <WinSock2.h>
#include "Socket.h"
#pragma comment(lib, "ws2_32.lib")						// �ֹ���������ws2_32.lib�⣬ws2_32.lib��winsock2�Ŀ��ļ�
using namespace std;

int _tmain(int argc, _TCHAR* argv[])
{
	int port = 8080;					// set port
	ULONG IP = INADDR_ANY;				// set accept All ip
	// char* IP = 127.0.0.1;
	// 1.initial WSA
	bool flag1 = InitialWSA();
	if(!flag1)	return 0;

	// 2.Create socket
	SOCKET Server = CreateSocket();
	if(Server == INVALID_SOCKET){
		cout << "SOCKET ERROR!" << endl;
		return 0;
	}

	// 3.Bind IP and port
	bool flag2 = Bind(Server, IP, port);
	if(!flag2){
		cout << "BIND ERROR!" << endl;
		return 0;
	}
	
	// 4.listin
	bool flag3 = Listen(Server);
	if(!flag3){
		cout << "LISTEN ERROR!" << endl;
		return 0;
	}
	
	// 5.Accept Connect
	SOCKET Client = AcceptConnect(Server);
	
	// 6.recieve data
	Recieve(Client);
	
	// 7.Close
	Close(Server);
	return 0;
}

