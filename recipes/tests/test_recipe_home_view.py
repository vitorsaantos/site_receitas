from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeHomeViewTest(RecipeTestBase):    
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')


    def test_recipe_home_template_shows_no_recipes_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 😢</h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        responde_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe title', content)
        self.assertEqual(len(responde_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """TEST RECIPE IS_PUBLISHE False DONT SHOW"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Check if one recipe exists
        self.assertIn(
            '<h1>No recipes found here 😢</h1>',
            response.content.decode('utf-8'))
