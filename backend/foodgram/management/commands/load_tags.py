import csv

from django.core.management.base import BaseCommand

from foodgram.models import Tag


class Command(BaseCommand):
    help = 'load ingredients from csv'

    def handle(self, *args, **kwargs):
        with open('database_data/tags.csv', 'r',
                  encoding='UTF-8') as recipes:
            for row in csv.reader(recipes):
                name = row[0]
                color = row[1]
                slug = row[2]
                Tag.objects.create(
                    name=name,
                    color=color,
                    slug=slug
                )
