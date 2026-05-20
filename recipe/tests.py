from django.test import TestCase
from django.urls import reverse
from .models import Category, Recipe


def make_category(name='Тестова категорія'):
    return Category.objects.create(name=name)


def make_recipe(category, title='Тестовий рецепт', **kwargs):
    return Recipe.objects.create(
        title=title,
        description='Опис',
        instructions='Інструкції',
        ingredients='Інгредієнти',
        category=category,
        **kwargs,
    )


class MainViewTest(TestCase):
    def setUp(self):
        category = make_category()
        for i in range(15):
            make_recipe(category, title=f'Рецепт {i}')

    def test_status_200(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'main.html')

    def test_returns_10_recipes(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(len(response.context['recipes']), 10)

    def test_returns_random_order(self):
        results = set()
        for _ in range(5):
            response = self.client.get(reverse('main'))
            titles = tuple(r.title for r in response.context['recipes'])
            results.add(titles)
        self.assertGreater(len(results), 1)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.category = make_category()
        for i in range(3):
            make_recipe(self.category, title=f'Рецепт {i}')
        self.other_category = make_category(name='Інша категорія')
        make_recipe(self.other_category, title='Чужий рецепт')

    def test_status_200(self):
        response = self.client.get(reverse('category_detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('category_detail', args=[self.category.pk]))
        self.assertTemplateUsed(response, 'category_detail.html')

    def test_shows_only_recipes_of_category(self):
        response = self.client.get(reverse('category_detail', args=[self.category.pk]))
        recipes = list(response.context['category'])
        self.assertEqual(len(recipes), 3)
        for recipe in recipes:
            self.assertEqual(recipe.category, self.category)

    def test_404_for_nonexistent_category(self):
        response = self.client.get(reverse('category_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class CategoryListViewTest(TestCase):
    def setUp(self):
        make_category(name='Супи')
        make_category(name='Салати')

    def test_status_200(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('category_list'))
        self.assertTemplateUsed(response, 'category_list.html')

    def test_shows_all_categories(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(len(response.context['categories']), 2)
