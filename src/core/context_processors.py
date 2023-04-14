from shops.models import Category


def all_categories_context_processors(request):
    return {"all_categories": Category.objects.all()}
