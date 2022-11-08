class Dog:
    def __init__(self, name, color, habits):
        self.name = name
        self.color = color
        self.habits = habits
        self.farting = False
    
    def bark(self):
        print("My name is " + self.name + " and I am " + self.color + " and I bark!")
    
    def eat(self):
        print(f"My name is {self.name} I am eating!")

# list = [1, 2, 3]
# print(type(1))
# print(type('dog'))
# print(type(list))



class Golden_Retriever(Dog):
    def __init__(self, name, color, habits):
        super().__init__(name, color, habits)


#a child class of the class dog called 'pug' that inherets the class dog and adds the property smushiness
class Pug(Dog):
    def __init__(self, name, color, habits, *smushiness):
        super().__init__(name, color, habits)
        self.smushiness = smushiness

    def fart(self):
        if self.farting == False:
            self.farting = True
            print("I am farting")
        else:
            print("I am not farting")

    def eat(self):
        print(f'I only eat people')

    def bark(self):
        print("I am a pug")



# fido = Dog("Fido", "brown", ["bark", "eat"])
# john = Dog("John", "black", ["bark", "eat"])

# Bailey = Pug("Bailey", "brown", "bark", 'very smushy')
# Bailey.eat()
# fido.eat()