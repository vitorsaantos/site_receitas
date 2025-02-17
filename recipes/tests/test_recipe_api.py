from django.urls import reverse
from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin
from unittest.mock import patch

class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_recipe_api_list(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipe_api-list')
        response = self.client.get(api_url)
        return response
    
    def test_recipe_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_corrects_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)
        response = self.client.get(reverse('recipes:recipe_api-list')) 
        qtd_of_loaded_recipes = len(response.data.get('results'))
        self.assertEqual(qtd_of_loaded_recipes, wanted_number_of_recipes)

    def test_recipe_api_list_do_not_show_not_publushed_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(len(response.data.get('results')), 1)
    
    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=9)
    def test_recipe_api_list_load_recipe_by_category_id(self):
        # Create categories
        category_wanted = self.make_category(name='Wanted_category')
        category_not_wanted = self.make_category(name='Not_wanted_category')
        # Create 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Channge all recipes to the wanted category
        # As a result, this recipe should NOT show in the page
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

            # Change one recipe to the NOT wanted category
        recipes[0].category = category_not_wanted
        recipes[0].save()
        
        # Action: get recipes by wanted category_id
        api_url = reverse('recipes:recipe_api-list') + f'?category=1{category_wanted.id}'
        response = self.get_recipe_api_list(api_url)
        
        # We should only see from the wanted category
        self.assertEqual(len(response.data.get('results')), 9)