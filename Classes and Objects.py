'''class Robot:
    def __init__(self,name,colour,weight):
        self.name=name
        self.colour=colour
        self.weight=weight
        
    def __str__(self) -> str:
        return f"{self.name}{self.colour}({self.weight})"

    def introduce_self(self):
        print("My name is " + self.name)
        print("My name is {} and my color is {} " .format(self.name , self.colour) )
    
robot1=Robot('Tom ','red',30)   
robot1.introduce_self() 
print(robot1.introduce_self())

robot2=Robot('Jerry','blue',40)
robot2.introduce_self()
print(robot2.introduce_self())'''
     

class Person:
    def __init__(thisperson,fname,lname) -> None:
        thisperson.firstname=fname
        thisperson.lastname=lname

    def printname(thisperson):
        print(thisperson.firstname,thisperson.lastname)

person1=Person('Gina','Jessy')
person1.printname()

class Student(Person):    #inheritance(put the parent class as the parameter)
    pass                  # the child class inherits the parent class functionality

student1=Student('Jeremy','Jayson')
student1.printname()

#Using the __init__function instead of pass:
class Student(Person):
    def __init__(thisperson,fname,lname) -> None:
        Person.__init__(thisperson,fname,lname)
        

#use of super()

class Student(Person):
     def __init__(thisperson, fname, lname, year) -> None:
         super().__init__(fname, lname)              #note the syntax difference between super()and __init__function.
         thisperson.graduationyear=year
         
     def about_self(thisperson):
         print(thisperson.firstname,thisperson.lastname,thisperson.graduationyear)

     def __str__(thisperson):
         return f"{thisperson.firstname}{thisperson.firstname}({thisperson.graduationyear})"
       
#ARBITRARY ARGS
     def introduce_student(thisperson):
         print('student1 is {} {}'.format(thisperson.firstname,thisperson.lastname) )

student2= Student('Gina','Marie',2025)
student2.introduce_student()

student2.firstname='Omondi'
student2.introduce_student()



