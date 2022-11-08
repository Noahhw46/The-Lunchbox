# Step 1
- A.) implement proxy

  - Server side
    A1.) Create an incoming socket
    A2.) Accept client and process request
    A3.) Redirect the traffic
    A4.) Send the response back to the client

  - Client side
    A5.) Create a socket
    A6.) Connect to the server
    A7.) Send the request
    A8.) Receive/display the response

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



# Step 3
- D.) feedback on port number used


class Proxy:
    def __init__(self, port):
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.listen(5)
        print("Proxy is listening on port " + str(self.port))

class Dog:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def bark(self):
        print("Woof! My name is " + self.name)

    def eat(self):
        print("Yum! I love eating!")

def main():
    fido = Dog("Fido")
    fido.bark()
>> print(type(fido))
>> print(type(1))
>> print(type("1"))