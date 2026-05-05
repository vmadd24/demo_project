import uuid
from datetime import datetime, timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .db import users, products, orders
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

        user = users.find_one({"email": email})
        if not user or not verify_password(password, user["password_hash"]):
            return Response({"detail": "Invalid email or password"}, status=401)

        token = create_access_token(user["id"], user["email"])
        resp = Response({
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
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
            "id": u["id"],
            "email": u["email"],
            "name": u["name"],
            "role": u["role"],
        })


# ---------------- Products ----------------
class ProductListCreateView(APIView):
    def get(self, request):
        q = {}
        category = request.query_params.get("category")
        if category and category.lower() != "all":
            q["category"] = category
        items = list(products.find(q, {"_id": 0}).sort("created_at", -1))
        return Response(items)

    @admin_required
    def post(self, request):
        ser = ProductSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        product = {
            "id": str(uuid.uuid4()),
            **ser.validated_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        products.insert_one(product.copy())
        return Response(product)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        p = products.find_one({"id": product_id}, {"_id": 0})
        if not p:
            return Response({"detail": "Product not found"}, status=404)
        return Response(p)

    @admin_required
    def put(self, request, product_id):
        existing = products.find_one({"id": product_id}, {"_id": 0})
        if not existing:
            return Response({"detail": "Product not found"}, status=404)
        ser = ProductSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        update = dict(ser.validated_data)
        products.update_one({"id": product_id}, {"$set": update})
        return Response({**existing, **update})

    @admin_required
    def delete(self, request, product_id):
        res = products.delete_one({"id": product_id})
        if res.deleted_count == 0:
            return Response({"detail": "Product not found"}, status=404)
        return Response({"ok": True})


# ---------------- Orders ----------------
class OrderListCreateView(APIView):
    def post(self, request):
        ser = OrderSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        items = data["items"]
        if not items:
            return Response({"detail": "Order must contain at least one item"}, status=400)
        total = round(sum(i["price"] * i["quantity"] for i in items), 2)
        order = {
            "id": str(uuid.uuid4()),
            "customer_name": data["customer_name"].strip(),
            "phone": data["phone"].strip(),
            "address": data["address"].strip(),
            "notes": data.get("notes", ""),
            "items": [dict(i) for i in items],
            "total": total,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        orders.insert_one(order.copy())
        return Response(order)

    @admin_required
    def get(self, request):
        items = list(orders.find({}, {"_id": 0}).sort("created_at", -1))
        return Response(items)


class OrderStatusView(APIView):
    @admin_required
    def patch(self, request, order_id):
        ser = OrderStatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        new_status = ser.validated_data["status"]
        res = orders.update_one({"id": order_id}, {"$set": {"status": new_status}})
        if res.matched_count == 0:
            return Response({"detail": "Order not found"}, status=404)
        return Response({"ok": True, "status": new_status})
