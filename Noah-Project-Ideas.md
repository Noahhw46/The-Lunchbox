# Chat program/network protocol cracking
 -  Two components to this: making a messenging program/messaging protocol, and cracking it.
 -  Component 1:
        - Messaging app - chat room
        set up sockets to listen for communication on both ends
        set up threads every time a user connects to the server and the server will attempt to establish a socket and bind it to an ip address and port
            maybe port forwarding to establish public usage?
        all of this can be done with default python libraries, and shouldn't actually be that hard to get started (a geeksforgeeks article outlines the whole process)
        - security
        start with no security in the protocol - just send the message as raw data unencrypted
        step by step increase the security. First we could maybe do encryption and decryption on the client side and see the flaws witht hat (mitm)
        eventually move to a more advanced, no knowledge protocol
        include an audit of the protocol at every step
        there are a bunch of levers we could turn to make it more/less secure - where encryption happens, what data is included in the packets, what kind of encryption, etc

- Component 2:
        - listener
        set up a listener (we could make it from scratch or use netcat) to listen for communications on the given port.
        The advantage to making it from scratch would be to have native/automatic parsing of the specific protocol we want
        

        


# Network protocol audit
- Pick a given network protocol: a game, a social media app, etc, and audit it.
- This article is an example of a simple audit of public key infrastucture... http://auditor101.com/definition-question-public-key-infrastructure-pki/



# Messenger app components:
    - It would be a chat room situation, where multiple computers can connect to the server and all talk in semi-real time to each other.
    - There would be two necessary scripts - both we could write in python.

        - Script 1 (Client side)
            - The client has to listen for two possible input streams; user input and server input
                - Pythonically that would like like this: 
                    sockets_list = [sys.stdin, server]
                    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
            - After recieving a connection from one of those streams the client would either pass it to the server or to standard out depending on where it was coming from.


        - Script 2 (Server side)
            - The server only has to listen for one type of connection, but it also has to determine from which client that connection was coming.
            - It also has to listen for some set number of connections
            - It also has to start threads for each client connected 
                - pythonically that looks like this:
                    from from _thread import *
                    start_new_thread(clientthread,(conn,addr)) 
    

    -One other random idea I had was also to mess with authentication... How can our protocol detect/prevent people from impersonating others?