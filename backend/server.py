from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Request, Response, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient

# ---------------- Config ----------------
MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
JWT_SECRET = os.environ["JWT_SECRET"]
ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
JWT_ALGORITHM = "HS256"

# ---------------- DB ----------------
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# ---------------- App ----------------
app = FastAPI(title="Bakery API")
api = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Helpers ----------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        "type": "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_admin(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await db.users.find_one({"id": payload["sub"]}, {"_id": 0, "password_hash": 0})
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Admin not found")
    return user

# ---------------- Models ----------------
class LoginIn(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    name: str
    role: str

class ProductIn(BaseModel):
    name: str
    category: str  # Bread | Cake | Pastry
    price: float
    description: str = ""
    image_url: str = ""
    available: bool = True

class ProductOut(ProductIn):
    id: str
    created_at: str

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(ge=1)
    price: float

class OrderIn(BaseModel):
    customer_name: str
    phone: str
    address: str
    notes: str = ""
    items: List[OrderItem]

class OrderOut(BaseModel):
    id: str
    customer_name: str
    phone: str
    address: str
    notes: str
    items: List[OrderItem]
    total: float
    status: str
    created_at: str

# ---------------- Auth Routes ----------------
@api.post("/auth/login")
async def login(payload: LoginIn, response: Response):
    email = payload.email.lower().strip()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user["id"], user["email"])
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 12,
        path="/",
    )
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
        "token": token,
    }

@api.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"ok": True}

@api.get("/auth/me", response_model=UserOut)
async def me(user: dict = Depends(get_current_admin)):
    return UserOut(**user)

# ---------------- Product Routes ----------------
@api.get("/products", response_model=List[ProductOut])
async def list_products(category: Optional[str] = None):
    q = {}
    if category and category.lower() != "all":
        q["category"] = category
    products = await db.products.find(q, {"_id": 0}).sort("created_at", -1).to_list(500)
    return products

@api.get("/products/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    p = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@api.post("/products", response_model=ProductOut)
async def create_product(payload: ProductIn, user: dict = Depends(get_current_admin)):
    product = {
        "id": str(uuid.uuid4()),
        **payload.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.products.insert_one(product.copy())
    return product

@api.put("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, payload: ProductIn, user: dict = Depends(get_current_admin)):
    existing = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = {**existing, **payload.model_dump()}
    await db.products.update_one({"id": product_id}, {"$set": payload.model_dump()})
    return updated

@api.delete("/products/{product_id}")
async def delete_product(product_id: str, user: dict = Depends(get_current_admin)):
    res = await db.products.delete_one({"id": product_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}

# ---------------- Order Routes ----------------
@api.post("/orders", response_model=OrderOut)
async def create_order(payload: OrderIn):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")
    total = round(sum(i.price * i.quantity for i in payload.items), 2)
    order = {
        "id": str(uuid.uuid4()),
        "customer_name": payload.customer_name.strip(),
        "phone": payload.phone.strip(),
        "address": payload.address.strip(),
        "notes": payload.notes,
        "items": [i.model_dump() for i in payload.items],
        "total": total,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.orders.insert_one(order.copy())
    return order

@api.get("/orders", response_model=List[OrderOut])
async def list_orders(user: dict = Depends(get_current_admin)):
    orders = await db.orders.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return orders

@api.patch("/orders/{order_id}/status")
async def update_order_status(order_id: str, status_body: dict, user: dict = Depends(get_current_admin)):
    new_status = status_body.get("status")
    if new_status not in ["pending", "confirmed", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    res = await db.orders.update_one({"id": order_id}, {"$set": {"status": new_status}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True, "status": new_status}

@api.get("/")
async def root():
    return {"message": "Bakery API", "status": "ok"}

app.include_router(api)

# ---------------- Seed ----------------
SAMPLE_PRODUCTS = [
    {
        "name": "Rustic Sourdough Loaf",
        "category": "Bread",
        "price": 8.50,
        "description": "Slow-fermented sourdough with a crackling crust and airy crumb. Baked at dawn.",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Seeded Country Baguette",
        "category": "Bread",
        "price": 5.00,
        "description": "Crisp French baguette dusted with sesame and poppy seeds.",
        "image_url": "https://images.unsplash.com/photo-1568471173242-461f0a730452?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Honey Walnut Loaf",
        "category": "Bread",
        "price": 9.75,
        "description": "Wildflower honey and toasted walnuts folded into a rustic whole-wheat loaf.",
        "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Vanilla Bean Celebration Cake",
        "category": "Cake",
        "price": 42.00,
        "description": "Three-tier vanilla sponge layered with Madagascan cream and berry compote.",
        "image_url": "https://images.pexels.com/photos/29450335/pexels-photo-29450335.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    },
    {
        "name": "Dark Chocolate Ganache Cake",
        "category": "Cake",
        "price": 38.00,
        "description": "Rich 70% cocoa sponge finished with a glossy ganache shell and sea salt.",
        "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Lemon Olive Oil Cake",
        "category": "Cake",
        "price": 28.00,
        "description": "Bright, tender crumb with Amalfi lemon zest and a thin candied glaze.",
        "image_url": "https://images.unsplash.com/photo-1562440499-64c9a111f713?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Butter Croissant",
        "category": "Pastry",
        "price": 4.25,
        "description": "72 folds of laminated French butter dough — shatteringly flaky.",
        "image_url": "https://images.pexels.com/photos/15738015/pexels-photo-15738015.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    },
    {
        "name": "Almond Pain au Chocolat",
        "category": "Pastry",
        "price": 4.75,
        "description": "Dark chocolate batons enrobed in buttery laminated dough with toasted almonds.",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Cinnamon Morning Bun",
        "category": "Pastry",
        "price": 4.50,
        "description": "Laminated bun tossed in cardamom sugar with a warm cinnamon swirl.",
        "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?auto=format&fit=crop&w=900&q=80",
    },
]

async def seed_admin():
    existing = await db.users.find_one({"email": ADMIN_EMAIL})
    if not existing:
        await db.users.insert_one({
            "id": str(uuid.uuid4()),
            "email": ADMIN_EMAIL,
            "password_hash": hash_password(ADMIN_PASSWORD),
            "name": "Admin",
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
    elif not verify_password(ADMIN_PASSWORD, existing["password_hash"]):
        await db.users.update_one(
            {"email": ADMIN_EMAIL},
            {"$set": {"password_hash": hash_password(ADMIN_PASSWORD)}},
        )

async def seed_products():
    count = await db.products.count_documents({})
    if count > 0:
        return
    now = datetime.now(timezone.utc).isoformat()
    docs = [
        {
            "id": str(uuid.uuid4()),
            **p,
            "available": True,
            "created_at": now,
        }
        for p in SAMPLE_PRODUCTS
    ]
    await db.products.insert_many([d.copy() for d in docs])

@app.on_event("startup")
async def on_start():
    await db.users.create_index("email", unique=True)
    await db.products.create_index("id", unique=True)
    await db.orders.create_index("id", unique=True)
    await seed_admin()
    await seed_products()
