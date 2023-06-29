from foodgram.models import Ingredient, Recipeingredient


def CreateUpdate(ingredients, instance=None, recipe=None):
    if instance:
        recipe = instance
    else:
        recipe = recipe
    Recipeingredient.objects.bulk_create(
        [Recipeingredient(
                        recipe=recipe,
                        ingredients=Ingredient.objects.get(id=ing['id']),
                        amount=ing['amount']
        ) for ing in ingredients]
    )
