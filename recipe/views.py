from django.shortcuts import render
from .models import Recipe


def main(request):
    recipes = Recipe.objects.order_by('?')[:10]
    return render(request, 'main.html', {'recipes': recipes})
