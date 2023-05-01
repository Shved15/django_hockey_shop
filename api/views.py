from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Bag, Product
from products.serializers import BagSerializer, ProductSerializer


class ProductModelViewSet(ModelViewSet):
    """
    The Django view for the Product model.
    Provides CRUD (create, read, update, delete) actions and sets permissions for each action.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """Defines the permissions for each action."""
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


class BagModelViewSet(ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = BagSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        """Defines, which Bag objects are returned for this view."""
        queryset = super(BagModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Defines the action of creating a Bag object.
        Retrieves the product_id from the request, checks for the existence of a product with this id,
        then creates or updates the Bag object for the given user and product.
        """
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'},
                                status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Bag.create_or_update(products.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'Thi field is required.'}, status=status.HTTP_400_BAD_REQUEST)
