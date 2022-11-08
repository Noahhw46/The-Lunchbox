# Chat program/network protocol cracking
 -  Two components to this: making a messenging program/messaging protocol, and cracking it.
 -  Component 1:

        - Messaging app - chat room
        --set up sockets to listen for communication on both ends
        --set up threads every time a user connects to the server and the server will attempt to establish a socket and bind it to an ip address and port
            --maybe port forwarding to establish public usage?
        --all of this can be done with default python libraries, and shouldn't actually be that hard to get started (a geeksforgeeks article outlines the whole process)
        
        - security
         start with no security in the protocol - just send the message as raw data unencrypted
         step by step increase the security. First we could maybe do encryption and decryption on the client side and see the flaws with that (mitm)
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
