# Step 1
- A.) implement proxy

  - Server side

   - A1.) Create an incoming socket
   - A2.) Accept client and process request
   - A3.) Redirect the traffic
   - A4.) Send the response back to the client

  - Client side

    A1.1.) Create a socket
    A2.1.) Connect to the server
    A5.) Send the request
    A6.) Receive/display the response


# Step 2
- B.) Parse user arguments

    - B1.) Parse the arguments
    - B2.) Check if the arguments are valid
    - B3.) If the arguments are valid, continue to step 3
    - B4.) If the arguments are invalid, display an error message and exit (Ex: Port > 65535)


# Step 3
- C.) Implement burpsuite feature (http request/response modification)

    - C1.) Parse the packet into a structure with http headers and body
    - C2.) Modify the packet based on the user's input


# Step 4
- D.) Ship it
    - D1.) Solve p=np
