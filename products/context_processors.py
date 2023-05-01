from products.models import Bag, Favorites


def bags(request):
    """A context processor to add a user's bags to the context."""
    # Get the current user
    user = request.user
    # Return the user's bags if they are authenticated, otherwise an empty list.
    return {'bags': Bag.objects.filter(user=user) if user.is_authenticated else []}


def favorites(request):
    """A context processor to add a user's favorites to the context."""
    user = request.user
    return {'favorites': Favorites.objects.filter(user=user) if user.is_authenticated else []}
