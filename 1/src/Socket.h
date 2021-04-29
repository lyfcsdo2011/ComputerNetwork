#ifndef __SOCKET__
#define __SOCKET__
#include "stdafx.h"
#include "Socket.h"
#include <iostream>
#include <WinSock2.h>
#include <string>
using namespace std;

bool InitialWSA();
SOCKET CreateSocket(); 
bool Bind(SOCKET, ULONG, int);
bool Listen(SOCKET);
SOCKET AcceptConnect(SOCKET);
bool Connect(SOCKET, char*, int);
void Recieve(SOCKET);
void Send(SOCKET);
void Close(SOCKET);
#endif