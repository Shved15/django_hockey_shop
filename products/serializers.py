from rest_framework import fields, serializers

from products.models import Bag, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    # Use a SlugRelatedField to serialize the category name instead of the category object.
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')


class BagSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Bag
        fields = ('id', 'product', 'quantity', 'sum', 'total_sum', 'total_quantity', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Bag.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Bag.objects.filter(user_id=obj.user.id).total_quantity()
