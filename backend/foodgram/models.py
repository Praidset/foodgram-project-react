from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator

from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200, verbose_name='Название рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], verbose_name='Время готовки')
    text = models.TextField()
    image = models.ImageField(
        upload_to='images/', verbose_name='Картинка рецепта'
    )
    ingredients = models.ManyToManyField('Ingredient',
                                         verbose_name='Ингредиенты',
                                         through='RecipeIngredient')
    tags = models.ManyToManyField('Tag',
                                  related_name='recipes',
                                  verbose_name='Теги для рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт {self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'Ингредиент {self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название')
    color = models.CharField(
        max_length=7, unique=True, validators=[RegexValidator(
            regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
            message='Введенное значение не является цветом в формате HEX!'
        ),
        ], verbose_name='Цвет тега')
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name='SlUG название')

    class Meta:
        verbose_name = 'Пометка'
        verbose_name_plural = 'Пометки'

    def __str__(self):
        return f'Тег {self.name}'


class Favourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='favourites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favby',
                               verbose_name='Рецепт под избранное')

    def __str__(self):
        return f'Избранное {self.user}{self.recipe}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_user_favourite_recipe')]


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='buyings',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='targeted',
                               verbose_name='Рецепт')

    def __str__(self):
        return f'В корзине {self.user} {self.recipe}'

    class Meta:
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'
        constraints = [UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_user_shopping_recipe')]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.PROTECT,
                                   verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                         verbose_name='Количество')

    def __str__(self) -> str:
        return f'{self.ingredient.name} - {self.amount}'

    class Meta:
        verbose_name = 'Ингредиенты у рецепта'
        verbose_name_plural = 'Ингредиенты у рецепта'
        constraints = [UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='recipe_unique_ingredient')]
