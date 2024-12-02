"""
💎 Exercise 1: User Management System

Design a User Management System for an application. 
The User class should have details such as name and email. 
he User Management System should allow users to register, 
delete their account, and update their information.
"""

class User:
    def __init__(self, name, email):
        self.name = name 
        self.email = email 

class UserManagementSystem:
    def __init__(self): 
        self.users = dict()

    def register(self, user):
        self.users[user] = user 

    def delete_account(self, user):
        del self.users[user]

    def update_info(self, user, new_info):
        self.users[user].name = new_info.get('name')
        self.users[user].email = new_info.get('email')
        

"""
💎 Exercise 2: Quiz Application

Create a Quiz class that has a list of Questions. 
Each Question has a question, a list of options and a correct answer. 
The Quiz should allow questions to be added, and it should calculate the 
score of a user based on the answers they provide.
"""

class Question:
    def __init__(self, question, options, correct_answer):
        self.question = question
        self.options = options 
        self.correct_answer = correct_answer

class Quiz:
    def __init__(self): 
        self.questions = set()
        self.question_to_ans = dict()

    def add_question(self, question):
        self.questions.add(question)
        self.question_to_ans[question.question] = question.correct_answer 

    def calculate_score(self, user_answers):    
        score = 0
        for question_text, answer in user_answers.items():
            correct_answer = self.question_to_ans.get(question_text)
            if correct_answer:
                score += (answer == correct_answer)
        return score 
        


"""
💎 Exercise 3: Recipe Management System

Design a Recipe Management System. The Recipe class should have a name, 
a list of ingredients and the preparation steps. 
The Recipe Management System should allow recipes to be added, removed, 
and searched by ingredient.
"""

class Recipe:
    def __init__(self, name, ingredients, steps):
        self.name = name 
        self.ingredients = ingredients
        self.steps = steps 

class RecipeManagementSystem:
    def __init__(self): 
        self.recipes = set()
    
    def add_recipe(self, recipe):
        self.recipes.add(recipe)

    def remove_recipe(self, recipe):
        self.recipes.remove(recipe)

    def search_by_ingredient(self, ingredient):
        return [recipe for recipe in self.recipes if ingredient in set(recipe.ingredients)]

"""
💎 Exercise 4: Online Shopping System

Create a ShoppingCart class for an online shopping system. 
The Product class represents a product with name and price. 
The ShoppingCart should allow products to be added, removed, 
and it should calculate the total price of the products in the cart.
"""

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price 

class ShoppingCart:
    def __init__(self):
        self.products = set() 

    def add_product(self, product):
        self.products.add(product)

    def remove_product(self, product):
        self.products.remove(product)

    def calculate_total(self):
        total = 0 
        for p in self.products: 
            total += p.price 
        return total 


