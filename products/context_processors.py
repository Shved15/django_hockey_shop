from products.models import Bag, Favorites


def bags(request):
    user = request.user
    return {'bags': Bag.objects.filter(user=user) if user.is_authenticated else []}


def favorites(request):
    user = request.user
    return {'favorites': Favorites.objects.filter(user=user) if user.is_authenticated else []}
