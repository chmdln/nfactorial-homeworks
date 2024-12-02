"""
Exercise 1:
Create a Pizza class that could have ingredients added to it. Raise an error if an attempt is made to add a duplicate ingredient.
"""
class Pizza:
    def __init__(self):
        self.ingredients = set()
    
    def add_ingredient(self, ingredient):
        if ingredient in self.ingredients: 
            raise ValueError(f"{ingredient} has already been added.")
        self.ingredients.add(ingredient)
        

"""
Exercise 2:
Create an Elevator class with methods to go up, go down, and get the current floor. The elevator should not be able to go below the ground floor (floor 0).
"""
class Elevator:
    def __init__(self):
        self.current_floor = 0 

    def go_up(self):
        self.current_floor += 1

    def go_down(self):
        if self.current_floor > 0: 
            self.current_floor -= 1

    def get_current_floor(self):
        return self.current_floor


"""
Exercise 3:
Create a class Stack with methods to push, pop, and check if the stack is empty. Raise an exception if a pop is attempted on an empty stack.
"""
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.stack:
            raise IndexError(f"Can't pop from empty stack.")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0 
        

"""
Exercise 4:
Design a BankAccount class with methods to deposit, withdraw, and check balance. Ensure that an account cannot go into a negative balance.
"""
class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance

    def deposit(self, amount):
        self.balance += amount 

    def withdraw(self, amount):
        if self.balance < amount: 
            raise ValueError("Insufficient funds in the account.")
        self.balance -= amount 

    def check_balance(self):
        return self.balance 


"""
Exercise 5:
Create a class Person with attributes for name and age. Implement a method birthday that increases the person's age by one. Raise an exception if an age less than 0 is entered.
"""
class Person:
    def __init__(self, name, age):
        if age < 0: 
            raise ValueError("Age can't be less than 0.")
        self.name = name 
        self.age = age 
        
    def birthday(self):
        self.age += 1


"""
Exercise 6:
Create an Animal base class and a Dog and Cat derived classes. Each animal should have a sound method which returns the sound they make.
"""
class Animal:
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Woof"

class Cat(Animal):
    def sound(self):
        return "Meow"


"""
Exercise 7:
Design a class Calculator with static methods for addition, subtraction, multiplication, and division. Division method should raise a ZeroDivisionError when trying to divide by zero.
"""
class Calculator:
    @staticmethod
    def add(x, y):
        return x+y 

    @staticmethod
    def subtract(x, y):
        return x-y 

    @staticmethod
    def multiply(x, y):
        return x*y 

    @staticmethod
    def divide(x, y):
        if y == 0: 
            raise ZeroDivisionError("Division by zero is not allowed.")
        return x/y 


"""
Exercise 8:
Create a class `Car` with attributes for speed and mileage. Raise a ValueError if a negative value for speed or mileage is entered.
"""
class Car:
    def __init__(self, speed, mileage):
        if speed < 0:
            raise ValueError("Speed cannot be negative.")
        if mileage < 0:
            raise ValueError("Mileage cannot be negative.")
        
        self.speed = speed
        self.mileage = mileage
        

"""
Exercise 9:
Create a Student class and a Course class. Each Course can enroll students and print a list of enrolled students.
"""
class Student:
    def __init__(self, name):
        self.name = name 

class Course:
    def __init__(self):
        self.students = set()

    def enroll(self, student):
        self.students.add(student)

    def print_students(self):
        return [student.name for student in self.students] 


"""
Exercise 10:
Create a Flight class with a destination, departure time, and a list of passengers. Implement methods to add passengers, change the destination, and delay the flight by a certain amount of time.
"""
class Flight:
    def __init__(self, destination, departure):
        self.destination = destination
        self.departure = departure 
        self.passengers = []

    @staticmethod
    def helper(time, delay_time):
        hours, minutes = map(int, time.split(":"))
        total_hours = hours + delay_time
        final_minutes = minutes % 60
        final_hours = total_hours % 24
        return f"{final_hours:02}:{final_minutes:02}"
    
    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def change_destination(self, new_destination):
        self.destination = new_destination

    def delay(self, delay_time):
        self.departure = self.helper(self.departure, delay_time)
        return self.departure
    

"""
Exercise 11:
Create a Library class with a list of Book objects. The Book class should have attributes for title and author. The Library class should have methods to add books and find a book by title.
"""
class Book:
    def __init__(self, title, author):
        self.title = title 
        self.author = author 

class Library:
    def __init__(self):
        self.books = set()

    def add_book(self, book):
        self.books.add(book)

    def find_by_title(self, title):
        return [book if book.title == title else None for book in self.books][0]
        


"""
Exercise 12:
Design a class Matrix that represents a 2D matrix with methods for addition, subtraction, and multiplication. Implement error handling for operations that are not allowed (e.g., adding matrices of different sizes).
"""
class Matrix:
    def __init__(self, matrix):
        # matrix is non-empty 
        if not matrix: 
            raise ValueError("Matrix must be non-empty.")
        # each row is of type List 
        if not all(isinstance(row, list) for row in matrix):
            raise ValueError("Matrix must be a 2D list.")
        # matrix has proper dimensions 
        if not all(len(row) == len(matrix[0]) for row in matrix):
            raise ValueError("All rows must have the same number of columns.")
        
        self.matrix = matrix 
        self.m = len(matrix)
        self.n = len(matrix[0]) 

    def _elementwise_operation(self, other, operator):
        mat = [[None for _ in range(other.n)] for _ in range(other.m)]
        for r in range(other.m): 
            for c in range(other.n):
                mat[r][c] = operator(self.matrix[r][c],  other.matrix[r][c])
        return Matrix(mat)


    def add(self, other):
        if (other.m != self.m) or (other.n != self.n): 
            raise ValueError("Matrices must have the same dimensions.")
        return self._elementwise_operation(other, (lambda x,y: x+y))


    def subtract(self, other):
        if (other.m != self.m) or (other.n != self.n): 
            raise ValueError("Matrices must have the same dimensions.")
        return self._elementwise_operation(other, (lambda x,y: x-y))
       
    # I assume we perform matrix cross-product operation (not dot product)
    def multiply(self, other):
        if (other.m != self.m) or (other.n != self.n): 
            raise ValueError("Matrices must have the same dimensions.")
        return self._elementwise_operation(other, (lambda x,y: x*y))


"""
Exercise 13:
Create a class Rectangle with attributes for height and width. Implement methods for calculating the area and perimeter of the rectangle. Also, implement a method is_square that returns true if the rectangle is a square and false otherwise.
"""
class Rectangle:
    def __init__(self, height, width):
        self.height = height 
        self.width = width 

    def area(self):
        return self.height*self.width 

    def perimeter(self):
        return 2*(self.height + self.width)

    def is_square(self):
        return self.height == self.width 


"""
Exercise 14:
Design a class Circle with attributes for radius. Implement methods for calculating the area and the circumference of the circle. Handle exceptions for negative radius values.
"""
class Circle:
    def __init__(self, radius):
        if radius < 0: 
            raise ValueError("Radius cannot be negative")
        self.radius = radius 
        self.pi = 3.141592653589793 

    def area(self):
        return self.pi*self.radius**2
        
    def circumference(self):
        return 2*self.pi*self.radius 


"""
Exercise 15:
Design a class Triangle with methods to calculate the area and perimeter. Implement error handling for cases where the given sides do not form a valid triangle.
"""
class Triangle:
    def __init__(self, side_a, side_b, side_c):
        # Check positive lengths
        if (side_a <= 0) or (side_b <= 0) or (side_c <= 0):
            raise ValueError("Triangle sides have to be positive.")
        # Triangle inequality theorem
        if (side_a+side_b <= side_c) or (side_a+side_c <= side_b) or (side_b+side_c <= side_a):
            raise ValueError("The sum of any two sides must be greater than the third side")
        
        self.a = side_a 
        self.b = side_b
        self.c = side_c 

    def area(self):
        semi = (self.a + self.b + self.c) / 2
        return (semi * (semi - self.a) * (semi - self.b) * (semi - self.c))**(1/2)

    def perimeter(self):
        return self.a + self.b + self.c


"""
Exercise 16:
Design a class Triangle with methods to calculate the area and perimeter. Implement error handling for cases where the given sides do not form a valid triangle.
"""
class AbstractShape:
    def area(self):
        pass
    def perimeter(self):
        pass

class Circle1(AbstractShape):
    def __init__(self, radius):
        self.radius = radius 

class Rectangle1(AbstractShape):
    def __init__(self, height, width):
        self.height = height 
        self.width = width 

class Triangle(AbstractShape):
    def __init__(self, side_a, side_b, side_c):
        # Check positive lengths
        if (side_a <= 0) or (side_b <= 0) or (side_c <= 0):
            raise ValueError("Triangle sides have to be positive.")
        # Triangle inequality theorem
        if (side_a+side_b <= side_c) or (side_a+side_c <= side_b) or (side_b+side_c <= side_a):
            raise ValueError("The sum of any two sides must be greater than the third side")
        
        self.a = side_a 
        self.b = side_b
        self.c = side_c 

    def area(self):
        semi = (self.a + self.b + self.c) / 2
        return (semi * (semi - self.a) * (semi - self.b) * (semi - self.c))**(1/2)

    def perimeter(self):
        return self.a + self.b + self.c
        

"""
Exercise 17:
Create a MusicPlayer class that contains a list of songs and methods to add songs, play a song, and skip to the next song. Also implement a method to shuffle the playlist.
"""
import random 
class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.index = 0 
        self.current_song = None   

    def add_song(self, song):
        self.playlist.append(song)

    def play_song(self):
        self.current_song = self.playlist[self.index]

    def next_song(self):
        self.index += 1
        self.current_song = self.playlist[self.index]

    def shuffle(self):
        n = len(self.playlist)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.playlist[i], self.playlist[j] = self.playlist[j], self.playlist[i]
        
        
"""
Exercise 18:
Design a Product class for an online store with attributes for name, price, and quantity. Implement methods to add stock, sell product, and check stock levels. Include error handling for attempting to sell more items than are in stock.
"""
class Product:
    def __init__(self, name, price, quantity):
        self.name = name 
        self.price = price 
        self.quantity = quantity

    def add_stock(self, quantity):
        self.quantity += quantity

    def sell(self, quantity):
        if quantity > self.quantity: 
            raise ValueError("Insufficient number of stock items.")
        self.quantity -= quantity 

    def check_stock(self):
        return self.quantity 


"""
Exercise 19:
Create a VideoGame class with attributes for title, genre, and rating. Implement methods to change the rating, change the genre, and display game details.
"""
class VideoGame:
    def __init__(self, title, genre, rating):
        self.title = title 
        self.genre = genre 
        self.rating = rating 

    def change_rating(self, rating):
        self.rating = rating 

    def change_genre(self, genre):
        self.genre = genre 

    def display_details(self):
        return self.__dict__


"""
Exercise 20:
Create a School class with a list of Teacher and Student objects. Teacher and Student classes should have attributes for name and age. The School class should have methods to add teachers, add students, and print a list of all people in the school.
"""
class Person1:
    def __init__(self, name, age):
        self.name = name 
        self.age = age 

class Teacher(Person1):
    def __init__(self, name, age): 
        super().__init__(name, age)

class Student1(Person1):
    def __init__(self, name, age): 
        super().__init__(name, age)

class School:
    def __init__(self):
        self.teachers = set()
        self.students = set()

    def add_teacher(self, teacher):
        self.teachers.add(teacher)

    def add_student(self, student):
        self.students.add(student)

    def get_all(self):
        return self.teachers | self.students 
        

"""
Exercise 21:
Design a Card class to represent a playing card with suit and rank. Then design a Deck class that uses the Card class. The Deck class should have methods to shuffle the deck, deal a card, and check the number of remaining cards.
"""
class Card:
    def __init__(self, suit, rank):
        self.suit = suit 
        self.rank = rank 

class Deck:
    def __init__(self):
        suits = ["hearts", "diamonds", "clubs", "spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
        
    def deal(self):
        if len(self.cards) == 0: 
            raise ValueError("All cards have been dealt.")
        return self.cards.pop()

    def count(self):
        return len(self.cards)


