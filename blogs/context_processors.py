from .models import Category

def get_categories(request):
    from .models import Category
    categories = Category.objects.all()
    return dict(categories=categories)