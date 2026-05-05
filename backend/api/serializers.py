from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    category = serializers.ChoiceField(choices=["Bread", "Cake", "Pastry"])
    price = serializers.FloatField(min_value=0)
    description = serializers.CharField(allow_blank=True, required=False, default="")
    image_url = serializers.CharField(allow_blank=True, required=False, default="")
    available = serializers.BooleanField(required=False, default=True)
    created_at = serializers.CharField(read_only=True)


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.FloatField(min_value=0)


class OrderSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    customer_name = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    notes = serializers.CharField(allow_blank=True, required=False, default="")
    items = OrderItemSerializer(many=True)
    total = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["pending", "confirmed", "completed", "cancelled"])
