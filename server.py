import os
import sys
import socket
from socket import AF_INET, SOCK_STREAM

host = ""
port = 8075

s = socket.socket(AF_INET, SOCK_STREAM)

s.bind((host, port))

