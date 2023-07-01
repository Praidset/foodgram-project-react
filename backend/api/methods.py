from foodgram.models import RecipeIngredient


def create_or_update(ingredients, instance=None, recipe=None):
    if instance:
        recipe = instance
    else:
        recipe = recipe
    RecipeIngredient.objects.bulk_create([RecipeIngredient(
        recipe=recipe,
        ingredient_id=ing['id'],
        amount=ing['amount']
    ) for ing in ingredients])
