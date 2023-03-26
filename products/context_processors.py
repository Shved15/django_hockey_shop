from products.models import Bag


def bags(request):
    user = request.user
    return {'bags': Bag.objects.filter(user=user) if user.is_authenticated else []}
