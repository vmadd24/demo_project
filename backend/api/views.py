from decimal import Decimal
from datetime import datetime, timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction

from .models import User, Product, Order, OrderItem
from .auth_utils import (
    verify_password,
    create_access_token,
    admin_required,
)
from .serializers import (
    LoginSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderStatusSerializer,
)


def _product_to_dict(p: Product) -> dict:
    return {
        "id": str(p.id),
        "name": p.name,
        "category": p.category,
        "price": float(p.price),
        "description": p.description,
        "image_url": p.image_url,
        "available": p.available,
        "created_at": p.created_at.isoformat() if p.created_at else "",
    }


def _order_to_dict(o: Order) -> dict:
    return {
        "id": str(o.id),
        "customer_name": o.customer_name,
        "phone": o.phone,
        "address": o.address,
        "notes": o.notes,
        "total": float(o.total),
        "status": o.status,
        "created_at": o.created_at.isoformat() if o.created_at else "",
        "items": [
            {
                "product_id": str(i.product_id),
                "product_name": i.product_name,
                "quantity": i.quantity,
                "price": float(i.price),
            }
            for i in o.items.all()
        ],
    }


# ---------------- Root ----------------
@api_view(["GET"])
def root(request):
    return Response({"message": "Bakery API", "status": "ok"})


# ---------------- Auth ----------------
class LoginView(APIView):
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].lower().strip()
        password = ser.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or password"}, status=401)

        if not verify_password(password, user.password_hash):
            return Response({"detail": "Invalid email or password"}, status=401)

        token = create_access_token(user.id, user.email)
        resp = Response({
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "token": token,
        })
        resp.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 60 * 12,
            path="/",
        )
        return resp


class LogoutView(APIView):
    def post(self, request):
        resp = Response({"ok": True})
        resp.delete_cookie("access_token", path="/")
        return resp


class MeView(APIView):
    @admin_required
    def get(self, request):
        u = request.admin_user
        return Response({
            "id": str(u.id),
            "email": u.email,
            "name": u.name,
            "role": u.role,
        })


# ---------------- Products ----------------
class ProductListCreateView(APIView):
    def get(self, request):
        qs = Product.objects.all()
        category = request.query_params.get("category")
        if category and category.lower() != "all":
            qs = qs.filter(category=category)
        return Response([_product_to_dict(p) for p in qs])

    @admin_required
    def post(self, request):
        ser = ProductSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        p = Product.objects.create(
            name=d["name"],
            category=d["category"],
            price=Decimal(str(d["price"])),
            description=d.get("description", ""),
            image_url=d.get("image_url", ""),
            available=d.get("available", True),
        )
        return Response(_product_to_dict(p))


class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            p = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=404)
        return Response(_product_to_dict(p))

    @admin_required
    def put(self, request, product_id):
        try:
            p = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=404)
        ser = ProductSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        p.name = d["name"]
        p.category = d["category"]
        p.price = Decimal(str(d["price"]))
        p.description = d.get("description", "")
        p.image_url = d.get("image_url", "")
        p.available = d.get("available", True)
        p.save()
        return Response(_product_to_dict(p))

    @admin_required
    def delete(self, request, product_id):
        deleted, _ = Product.objects.filter(id=product_id).delete()
        if deleted == 0:
            return Response({"detail": "Product not found"}, status=404)
        return Response({"ok": True})


# ---------------- Orders ----------------
class OrderListCreateView(APIView):
    def post(self, request):
        ser = OrderSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        items = d["items"]
        if not items:
            return Response({"detail": "Order must contain at least one item"}, status=400)
        total = sum(Decimal(str(i["price"])) * i["quantity"] for i in items)
        with transaction.atomic():
            order = Order.objects.create(
                customer_name=d["customer_name"].strip(),
                phone=d["phone"].strip(),
                address=d["address"].strip(),
                notes=d.get("notes", ""),
                total=total,
                status="pending",
            )
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product_id=i["product_id"],
                    product_name=i["product_name"],
                    quantity=i["quantity"],
                    price=Decimal(str(i["price"])),
                )
                for i in items
            ])
        return Response(_order_to_dict(order))

    @admin_required
    def get(self, request):
        qs = Order.objects.all().prefetch_related("items")
        return Response([_order_to_dict(o) for o in qs])


class OrderStatusView(APIView):
    @admin_required
    def patch(self, request, order_id):
        ser = OrderStatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        new_status = ser.validated_data["status"]
        updated = Order.objects.filter(id=order_id).update(status=new_status)
        if updated == 0:
            return Response({"detail": "Order not found"}, status=404)
        return Response({"ok": True, "status": new_status})
