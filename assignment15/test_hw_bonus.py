import unittest

# Assuming the User, UserManagementSystem, Question, Quiz, Recipe, RecipeManagementSystem, Product and ShoppingCart are defined in a module called "my_module"
from hw_bonus import User, UserManagementSystem, Question, Quiz, Recipe, RecipeManagementSystem, Product, ShoppingCart

class TestUserManagementSystem(unittest.TestCase):
    def setUp(self):
        self.user = User('test_user', 'test_email@gmail.com')
        self.system = UserManagementSystem()

    def test_register(self):
        self.system.register(self.user)
        # Assert that the user is registered in the system
        self.assertIn(self.user, self.system.users)

    def test_delete_account(self):
        self.system.register(self.user)
        self.system.delete_account(self.user)
        # Assert that the user is deleted from the system
        self.assertNotIn(self.user, self.system.users)

    def test_update_info(self):
        self.system.register(self.user)
        new_info = {'name': 'new_name', 'email': 'new_email@gmail.com'}
        self.system.update_info(self.user, new_info)
        # Assert that the user's info is updated
        self.assertEqual(self.user.name, 'new_name')
        self.assertEqual(self.user.email, 'new_email@gmail.com')


class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.quiz = Quiz()
        self.question = Question('Is this a test?', ['Yes', 'No'], 'Yes')

    def test_add_question(self):
        self.quiz.add_question(self.question)
        # Assert that the question is added to the quiz
        self.assertIn(self.question, self.quiz.questions)

    def test_calculate_score(self):
        self.quiz.add_question(self.question)
        user_answers = {'Is this a test?': 'Yes'}
        score = self.quiz.calculate_score(user_answers)
        # Assert that the user's score is calculated correctly
        self.assertEqual(score, 1)


class TestRecipeManagementSystem(unittest.TestCase):
    def setUp(self):
        self.system = RecipeManagementSystem()
        self.recipe = Recipe('Test Recipe', ['ingredient1', 'ingredient2'], ['step1', 'step2'])

    def test_add_recipe(self):
        self.system.add_recipe(self.recipe)
        # Assert that the recipe is added to the system
        self.assertIn(self.recipe, self.system.recipes)

    def test_remove_recipe(self):
        self.system.add_recipe(self.recipe)
        self.system.remove_recipe(self.recipe)
        # Assert that the recipe is removed from the system
        self.assertNotIn(self.recipe, self.system.recipes)

    def test_search_by_ingredient(self):
        self.system.add_recipe(self.recipe)
        found_recipes = self.system.search_by_ingredient('ingredient1')
        # Assert that the correct recipes are found by ingredient
        self.assertIn(self.recipe, found_recipes)


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.product = Product('Test Product', 10)

    def test_add_product(self):
        self.cart.add_product(self.product)
        # Assert that the product is added to the cart
        self.assertIn(self.product, self.cart.products)

    def test_remove_product(self):
        self.cart.add_product(self.product)
        self.cart.remove_product(self.product)
        # Assert that the product is removed from the cart
        self.assertNotIn(self.product, self.cart.products)

    def test_calculate_total(self):
        self.cart.add_product(self.product)
        self.cart.add_product(Product('Test Product 2', 20))
        total = self.cart.calculate_total()
        # Assert that the total price of the products in the cart is calculated correctly
        self.assertEqual(total, 30)

if __name__ == '__main__':
    unittest.main()