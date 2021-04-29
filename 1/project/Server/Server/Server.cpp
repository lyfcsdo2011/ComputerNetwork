// Server.cpp : 定义控制台应用程序的入口点。
//
/***** winsock c/s建立过程（服务器）*******
			1.初始化WSA
			2.建立socket
			3.绑定socket和绑定对应端口
			4.监听
			5.接受连接
			6.发送和接受数据
			7.断开连接
******************************************/

#include "stdafx.h"
#include <iostream>
#include <stdio.h>
#include <WinSock2.h>
#include "Socket.h"
#pragma comment(lib, "ws2_32.lib")						// 手工导入链接ws2_32.lib库，ws2_32.lib是winsock2的库文件
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

