from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(
        max_length=200
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    text = models.TextField()
    image = models.ImageField(
        upload_to='images/'
    )
    ingredients = models.ManyToManyField('Ingredients',
                                         through='Recipe_ingredients')
    tags = models.ManyToManyField('Tags', related_name='recipes',
                                  verbose_name='tags_recipes')

    def __str__(self):
        return f'Рецепт {self.name}'


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(
        max_length=7, unique=True, validators=[RegexValidator(
            regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
            message='Введенное значение не является цветом в формате HEX!'
        )
        ])
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return f'Тег {self.name}'


class Favourites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='favourites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favby')


class ShoppingCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='buyings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='targeted')


class Recipe_ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name="mtmrecipe")
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                    related_name="mtmingredients")
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f'{self.ingredients.name} - {self.amount}'
