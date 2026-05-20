from dataclasses import dataclass, field


@dataclass
class Product:
    id: str
    name: str
    category: str
    price_usd: float
    description: str
    in_stock: bool = True
    tags: list[str] = field(default_factory=list)


CATALOG: list[Product] = [
    # --- Plush Toys ---
    Product(
        id="plush-001",
        name="Hello Kitty Classic Plush - Small (6 inch)",
        category="Plush Toys",
        price_usd=12.99,
        description="Soft and cuddly Hello Kitty plush, perfect for gifts and collection. "
        "Made with premium polyester fabric. Officially licensed Sanrio product.",
        tags=["plush", "classic", "small", "gift"],
    ),
    Product(
        id="plush-002",
        name="Hello Kitty Classic Plush - Large (14 inch)",
        category="Plush Toys",
        price_usd=24.99,
        description="Extra-large Hello Kitty plush doll with iconic bow detail. "
        "Super soft filling, great for hugging. Officially licensed.",
        tags=["plush", "classic", "large", "gift"],
    ),
    Product(
        id="plush-003",
        name="Hello Kitty x Kuromi Duo Plush Set",
        category="Plush Toys",
        price_usd=29.99,
        description="Limited collaboration plush set featuring Hello Kitty and Kuromi "
        "in matching outfits. Collector's item, limited quantities.",
        in_stock=False,
        tags=["plush", "kuromi", "collab", "limited", "set"],
    ),
    Product(
        id="plush-004",
        name="Hello Kitty Holiday Edition Plush",
        category="Plush Toys",
        price_usd=19.99,
        description="Seasonal Hello Kitty plush dressed in festive holiday outfit. "
        "Perfect holiday gift. Limited seasonal stock.",
        tags=["plush", "holiday", "seasonal", "gift"],
    ),
    # --- Bags & Accessories ---
    Product(
        id="bag-001",
        name="Hello Kitty Mini Backpack",
        category="Bags",
        price_usd=34.99,
        description="Adorable mini backpack with Hello Kitty face embroidery. "
        "Dimensions: 10x8x4 inches. Adjustable straps, zip closure, inner pocket.",
        tags=["bag", "backpack", "mini", "everyday"],
    ),
    Product(
        id="bag-002",
        name="Hello Kitty Crossbody Bag",
        category="Bags",
        price_usd=27.99,
        description="Compact crossbody bag with Hello Kitty print. "
        "Dimensions: 8x6x2 inches. Adjustable strap. Perfect for outings.",
        tags=["bag", "crossbody", "compact", "everyday"],
    ),
    Product(
        id="acc-001",
        name="Hello Kitty Keychain Set (3-pack)",
        category="Accessories",
        price_usd=9.99,
        description="Set of 3 Hello Kitty metal keychains in different poses. "
        "Durable alloy material with enamel coating. Great stocking stuffer.",
        tags=["keychain", "accessory", "set", "gift"],
    ),
    Product(
        id="acc-002",
        name="Hello Kitty Phone Case - Universal Fit",
        category="Accessories",
        price_usd=14.99,
        description="Soft TPU phone case with Hello Kitty 3D raised print. "
        "Compatible with most iPhone and Samsung models (please specify at checkout).",
        tags=["phone case", "accessory", "protective"],
    ),
    # --- Stationery ---
    Product(
        id="stat-001",
        name="Hello Kitty Notebook Set (3-pack)",
        category="Stationery",
        price_usd=16.99,
        description="Set of 3 A5 lined notebooks with Hello Kitty covers. "
        "80 pages each, premium paper quality. Perfect for school or journaling.",
        tags=["notebook", "stationery", "school", "set"],
    ),
    Product(
        id="stat-002",
        name="Hello Kitty Gel Pen Set (10-pack)",
        category="Stationery",
        price_usd=11.99,
        description="10 colorful gel pens featuring Hello Kitty designs on barrel. "
        "Smooth 0.5mm ink tip. Colors: red, pink, purple, blue, green, and more.",
        tags=["pen", "stationery", "school", "set", "colorful"],
    ),
    Product(
        id="stat-003",
        name="Hello Kitty Pencil Case",
        category="Stationery",
        price_usd=8.99,
        description="Large-capacity pencil case with Hello Kitty zipper charm. "
        "Dimensions: 8x4 inches. Holds 40+ pens and pencils.",
        tags=["pencil case", "stationery", "school"],
    ),
    # --- Apparel ---
    Product(
        id="app-001",
        name="Hello Kitty Oversized T-Shirt",
        category="Apparel",
        price_usd=22.99,
        description="Trendy oversized tee with Hello Kitty graphic print. "
        "100% cotton, sizes S-3XL. Machine washable. Unisex fit.",
        tags=["tshirt", "apparel", "clothing", "casual"],
    ),
    Product(
        id="app-002",
        name="Hello Kitty Hoodie",
        category="Apparel",
        price_usd=39.99,
        description="Cozy pullover hoodie with embroidered Hello Kitty logo. "
        "80% cotton / 20% polyester. Kangaroo pocket. Sizes XS-2XL.",
        tags=["hoodie", "apparel", "clothing", "cozy"],
    ),
    Product(
        id="app-003",
        name="Hello Kitty Socks Set (5-pack)",
        category="Apparel",
        price_usd=13.99,
        description="Five pairs of cute Hello Kitty crew socks in assorted prints. "
        "One size fits most (US 5-9). Soft cotton blend.",
        tags=["socks", "apparel", "set", "gift"],
    ),
]


def get_all_products() -> list[Product]:
    return CATALOG


def get_in_stock_products() -> list[Product]:
    return [p for p in CATALOG if p.in_stock]


def get_products_by_category(category: str) -> list[Product]:
    return [p for p in CATALOG if p.category.lower() == category.lower()]


def search_products(query: str) -> list[Product]:
    query_lower = query.lower()
    return [
        p
        for p in CATALOG
        if query_lower in p.name.lower()
        or query_lower in p.description.lower()
        or any(query_lower in tag for tag in p.tags)
    ]


def format_catalog_for_prompt() -> str:
    """Serialize the catalog into a compact string for the system prompt."""
    lines = []
    categories: dict[str, list[Product]] = {}
    for product in CATALOG:
        categories.setdefault(product.category, []).append(product)

    for category, products in categories.items():
        lines.append(f"\n### {category}")
        for p in products:
            stock_note = "" if p.in_stock else " [OUT OF STOCK]"
            lines.append(
                f"- {p.name}{stock_note} | ${p.price_usd:.2f} | {p.description}"
            )
    return "\n".join(lines)
