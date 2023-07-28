class People:
    def __init__(self,name,age,gender,weight) -> None:
        self.name=name
        self.age=age
        self.gender=gender
        self.weight=weight

    def __str__(self) -> str:
        return f"{self.name}({self.age}){self.gender}"

    def introduce_self(self):
        print("My name is {}.I am {} years old.I am a {}". format(self.name , self.age , self.gender) )

person1=People('Gina', 22,'girl',95)
person1.introduce_self()

person2=People('Jessy',19,'girl',85)
person2.introduce_self()

