from decimal import Decimal
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

from .models import User, Product
from .auth_utils import hash_password, verify_password


SAMPLE_PRODUCTS = [
    {
        "name": "Rustic Sourdough Loaf",
        "category": "Bread",
        "price": "8.50",
        "description": "Slow-fermented sourdough with a crackling crust and airy crumb. Baked at dawn.",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Seeded Country Baguette",
        "category": "Bread",
        "price": "5.00",
        "description": "Crisp French baguette dusted with sesame and poppy seeds.",
        "image_url": "https://images.unsplash.com/photo-1568471173242-461f0a730452?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Honey Walnut Loaf",
        "category": "Bread",
        "price": "9.75",
        "description": "Wildflower honey and toasted walnuts folded into a rustic whole-wheat loaf.",
        "image_url": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Vanilla Bean Celebration Cake",
        "category": "Cake",
        "price": "42.00",
        "description": "Three-tier vanilla sponge layered with Madagascan cream and berry compote.",
        "image_url": "https://images.pexels.com/photos/29450335/pexels-photo-29450335.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    },
    {
        "name": "Dark Chocolate Ganache Cake",
        "category": "Cake",
        "price": "38.00",
        "description": "Rich 70% cocoa sponge finished with a glossy ganache shell and sea salt.",
        "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Lemon Olive Oil Cake",
        "category": "Cake",
        "price": "28.00",
        "description": "Bright, tender crumb with Amalfi lemon zest and a thin candied glaze.",
        "image_url": "https://images.unsplash.com/photo-1562440499-64c9a111f713?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Butter Croissant",
        "category": "Pastry",
        "price": "4.25",
        "description": "72 folds of laminated French butter dough — shatteringly flaky.",
        "image_url": "https://images.pexels.com/photos/15738015/pexels-photo-15738015.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    },
    {
        "name": "Almond Pain au Chocolat",
        "category": "Pastry",
        "price": "4.75",
        "description": "Dark chocolate batons enrobed in buttery laminated dough with toasted almonds.",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Cinnamon Morning Bun",
        "category": "Pastry",
        "price": "4.50",
        "description": "Laminated bun tossed in cardamom sugar with a warm cinnamon swirl.",
        "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?auto=format&fit=crop&w=900&q=80",
    },
]


def _seed_admin():
    email = settings.ADMIN_EMAIL
    password = settings.ADMIN_PASSWORD
    user = User.objects.filter(email=email).first()
    if not user:
        User.objects.create(
            email=email,
            password_hash=hash_password(password),
            name="Admin",
            role="admin",
        )
    elif not verify_password(password, user.password_hash):
        user.password_hash = hash_password(password)
        user.save(update_fields=["password_hash"])


def _seed_products():
    if Product.objects.exists():
        return
    Product.objects.bulk_create([
        Product(
            name=p["name"],
            category=p["category"],
            price=Decimal(p["price"]),
            description=p["description"],
            image_url=p["image_url"],
            available=True,
        )
        for p in SAMPLE_PRODUCTS
    ])


def seed_all():
    """Idempotent. Safe to run on every boot.

    Wrapped in try/except so it doesn't crash before migrations have been run
    (e.g. during `manage.py migrate` itself).
    """
    try:
        _seed_admin()
        _seed_products()
    except (OperationalError, ProgrammingError):
        # Tables don't exist yet — migration must run first.
        pass
