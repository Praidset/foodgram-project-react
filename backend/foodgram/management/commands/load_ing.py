from django.core.management.base import BaseCommand
import csv
from foodgram.models import Ingredients


class Command(BaseCommand):
    help = 'load ingredients from csv'

    def handle(self, *args, **kwargs):
        with open('ingredients.csv', 'r', encoding='UTF-8') as ingredients:
            for row in csv.reader(ingredients):
                ingredient = row[0]
                measure = row[1]
                Ingredients.objects.create(
                    name=ingredient, measurement_unit=measure,
                )