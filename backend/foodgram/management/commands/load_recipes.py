import csv

from django.core.management.base import BaseCommand

from foodgram.models import Recipe


class Command(BaseCommand):
    help = 'load ingredients from csv'

    def handle(self, *args, **kwargs):
        with open('database_data/recipes.csv',
                  'r', encoding='UTF-8') as recipes:
            for row in csv.reader(recipes):
                name = row[0]
                cooking_time = row[1]
                text = row[2]
                image = row[3]
                author = 1
                Recipe.objects.create(
                    name=name,
                    cooking_time=cooking_time,
                    text=text,
                    image=image,
                    author_id=author
                )
