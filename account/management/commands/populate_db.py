from random import choice, randint, sample

from django.core.management.base import BaseCommand

from account.models import User
from order.models import Cart, CartItem, Order, OrderProduct
from product.models import Brand, Category, Product, Review
from store.models import Store, StoreCategory


class Command(BaseCommand):
    help = "Populate the database with real data"

    def handle(self, *args, **kwargs):
        # Realistic User Data (20 users)
        users_data = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "username": "john_doe",
            },
            {
                "first_name": "Tommy",
                "last_name": "Smith",
                "email": "tommy.smith@example.com",
                "username": "tommy_smith",
            },
            {
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alice.johnson@example.com",
                "username": "alice_johnson",
            },
            {
                "first_name": "Bob",
                "last_name": "Williams",
                "email": "bob.williams@example.com",
                "username": "bob_williams",
            },
            {
                "first_name": "Emma",
                "last_name": "Brown",
                "email": "emma.brown@example.com",
                "username": "emma_brown",
            },
            {
                "first_name": "Sophia",
                "last_name": "Davis",
                "email": "sophia.davis@example.com",
                "username": "sophia_davis",
            },
            {
                "first_name": "James",
                "last_name": "Miller",
                "email": "james.miller@example.com",
                "username": "james_miller",
            },
            {
                "first_name": "Oliver",
                "last_name": "Garcia",
                "email": "oliver.garcia@example.com",
                "username": "oliver_garcia",
            },
            {
                "first_name": "Mia",
                "last_name": "Martinez",
                "email": "mia.martinez@example.com",
                "username": "mia_martinez",
            },
            {
                "first_name": "Liam",
                "last_name": "Rodriguez",
                "email": "liam.rodriguez@example.com",
                "username": "liam_rodriguez",
            },
            {
                "first_name": "Lucas",
                "last_name": "Perez",
                "email": "lucas.perez@example.com",
                "username": "lucas_perez",
            },
            {
                "first_name": "Isabella",
                "last_name": "Hernandez",
                "email": "isabella.hernandez@example.com",
                "username": "isabella_hernandez",
            },
            {
                "first_name": "Amelia",
                "last_name": "Lopez",
                "email": "amelia.lopez@example.com",
                "username": "amelia_lopez",
            },
            {
                "first_name": "Ethan",
                "last_name": "Gonzalez",
                "email": "ethan.gonzalez@example.com",
                "username": "ethan_gonzalez",
            },
            {
                "first_name": "Charlotte",
                "last_name": "Wilson",
                "email": "charlotte.wilson@example.com",
                "username": "charlotte_wilson",
            },
            {
                "first_name": "Aiden",
                "last_name": "Anderson",
                "email": "aiden.anderson@example.com",
                "username": "aiden_anderson",
            },
            {
                "first_name": "Scarlett",
                "last_name": "Thomas",
                "email": "scarlett.thomas@example.com",
                "username": "scarlett_thomas",
            },
            {
                "first_name": "Jackson",
                "last_name": "Taylor",
                "email": "jackson.taylor@example.com",
                "username": "jackson_taylor",
            },
            {
                "first_name": "Victoria",
                "last_name": "Moore",
                "email": "victoria.moore@example.com",
                "username": "victoria_moore",
            },
        ]
        users = []
        roles = ["customer", "store_manager", "store_owner", "admin"]
        for index, user_data in enumerate(users_data):
            user = User.objects.create_user(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                username=user_data["username"],
                email=user_data["email"],
                password="password123",
                phone_number=f"555-010{index+1}",
                address=f"{index+1} Main St, City, Country",
                role=roles[index % len(roles)],
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))

        # Store Categories (5 categories)
        store_categories = ["Electronics", "Fashion", "Groceries", "Books", "Furniture"]
        store_category_objs = [
            StoreCategory.objects.create(name=category) for category in store_categories
        ]
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(store_category_objs)} store categories")
        )

        # Stores (5 stores with realistic names)
        stores = [
            Store.objects.create(
                name=f"BestBuy {index+1}",
                address=f"{index+1} Shop Ave, City, Country",
                location=f"City {index+1}",
                owner=users[index % len(users)],
                manager=users[(index + 1) % len(users)],
            )
            for index in range(5)
        ]
        for store in stores:
            store.store_categories.add(*sample(store_category_objs, k=2))
        self.stdout.write(self.style.SUCCESS(f"Created {len(stores)} stores"))

        # Brands (20 entries)
        brands = [
            "Apple",
            "Samsung",
            "Sony",
            "LG",
            "Nike",
            "Adidas",
            "Microsoft",
            "Google",
            "Amazon",
            "Dell",
            "HP",
            "Lenovo",
            "Huawei",
            "Bose",
            "Canon",
            "Nikon",
            "Razer",
            "Seagate",
            "Intel",
            "Asus",
        ]
        brand_objs = [Brand.objects.create(name=brand) for brand in brands]
        self.stdout.write(self.style.SUCCESS(f"Created {len(brand_objs)} brands"))

        # Product Categories (20 entries)
        product_categories = [
            "Mobile",
            "Laptop",
            "Shoes",
            "Books",
            "TV",
            "Furniture",
            "Headphones",
            "Gaming",
            "Camera",
            "Smartwatch",
            "Monitor",
            "Speaker",
            "Tablet",
            "Storage",
            "Washing Machine",
            "Refrigerator",
            "Air Conditioner",
            "Smart Home",
            "Kitchen Appliances",
            "Lighting",
        ]
        category_objs = [
            Category.objects.create(name=category) for category in product_categories
        ]
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(category_objs)} product categories")
        )

        # Products (20 products with realistic names, descriptions, prices)
        products_data = [
            {
                "name": "iPhone 14",
                "description": "Apple's latest smartphone with cutting-edge features.",
                "price": 999.99,
                "brand": "Apple",
                "categories": ["Mobile", "Electronics"],
            },
            {
                "name": "Samsung Galaxy S23",
                "description": "Flagship smartphone with an amazing camera and display.",
                "price": 899.99,
                "brand": "Samsung",
                "categories": ["Mobile", "Electronics"],
            },
            {
                "name": "Sony WH-1000XM5",
                "description": "Industry-leading noise-canceling headphones.",
                "price": 349.99,
                "brand": "Sony",
                "categories": ["Electronics", "Audio"],
            },
            {
                "name": "Nike Air Max 270",
                "description": "Stylish and comfortable sneakers from Nike.",
                "price": 130.00,
                "brand": "Nike",
                "categories": ["Shoes", "Fashion"],
            },
            {
                "name": "LG 55-Inch 4K TV",
                "description": "Stunning 4K resolution for your home entertainment.",
                "price": 600.00,
                "brand": "LG",
                "categories": ["TV", "Electronics"],
            },
            {
                "name": "MacBook Pro 16-inch",
                "description": "Apple's powerful laptop for professional use.",
                "price": 2399.99,
                "brand": "Apple",
                "categories": ["Laptop", "Electronics"],
            },
            {
                "name": "Sony PlayStation 5",
                "description": "Next-gen gaming console with impressive performance.",
                "price": 499.99,
                "brand": "Sony",
                "categories": ["Electronics", "Gaming"],
            },
            {
                "name": "Kindle Paperwhite",
                "description": "Amazon's e-reader with a high-resolution screen.",
                "price": 129.99,
                "brand": "Amazon",
                "categories": ["Books", "Electronics"],
            },
            {
                "name": "Adidas Ultraboost 22",
                "description": "High-performance running shoes for comfort and speed.",
                "price": 180.00,
                "brand": "Adidas",
                "categories": ["Shoes", "Fashion"],
            },
            {
                "name": "Dell XPS 13",
                "description": "Compact laptop with a stunning display and powerful performance.",
                "price": 1099.99,
                "brand": "Dell",
                "categories": ["Laptop", "Electronics"],
            },
            {
                "name": "Samsun QLED 8K TV",
                "description": "Ultra-high-definition television with amazing clarity.",
                "price": 2999.99,
                "brand": "Samsung",
                "categories": ["TV", "Electronics"],
            },
            {
                "name": "Razer Blade 15",
                "description": "Gaming laptop with top-tier performance.",
                "price": 1799.99,
                "brand": "Razer",
                "categories": ["Laptop", "Gaming"],
            },
            {
                "name": "Bose QuietComfort 45",
                "description": "Noise-cancelling headphones with premium sound.",
                "price": 329.99,
                "brand": "Bose",
                "categories": ["Electronics", "Audio"],
            },
            {
                "name": "Canon EOS 90D",
                "description": "High-resolution DSLR camera for photography enthusiasts.",
                "price": 1199.99,
                "brand": "Canon",
                "categories": ["Camera", "Electronics"],
            },
            {
                "name": "Nikon D7500",
                "description": "Mid-range DSLR camera for high-quality photos.",
                "price": 849.99,
                "brand": "Nikon",
                "categories": ["Camera", "Electronics"],
            },
            {
                "name": "Seagate 1TB External HDD",
                "description": "Portable external hard drive for data storage.",
                "price": 59.99,
                "brand": "Seagate",
                "categories": ["Storage", "Electronics"],
            },
            {
                "name": "Samsung Galaxy Tab S8",
                "description": "High-performance tablet with a stunning display.",
                "price": 649.99,
                "brand": "Samsung",
                "categories": ["Tablet", "Electronics"],
            },
            {
                "name": "Samsung SmartThings Hub",
                "description": "Smart home control hub to manage devices.",
                "price": 99.99,
                "brand": "Samsung",
                "categories": ["Smart Home", "Electronics"],
            },
            {
                "name": "Whirlpool Washing Machine",
                "description": "Energy-efficient washing machine for your laundry needs.",
                "price": 499.99,
                "brand": "Whirlpool",
                "categories": ["Appliances", "Home"],
            },
        ]

        products = []
        for product_data in products_data:
            product = Product.objects.create(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                stock=randint(1, 100),
                rating=randint(1, 5),
                brand=choice(brand_objs),
                store=choice(stores),
                is_approved=True,
            )
            product.categories.add(
                *[
                    category
                    for category in category_objs
                    if category.name in product_data["categories"]
                ]
            )
            products.append(product)

        self.stdout.write(self.style.SUCCESS(f"Created {len(products)} products"))

        # Reviews (15 products with reviews, 5 without)
        reviews = []
        for product in products[:15]:  # Add reviews only for first 15 products
            for _ in range(randint(1, 5)):  # Random number of reviews per product
                review = Review.objects.create(
                    product=product,
                    user=choice(users),
                    rating=randint(1, 5),
                    comment=f"Great product! I really like the {product.name} for its features.",
                )
                reviews.append(review)
        self.stdout.write(self.style.SUCCESS(f"Created {len(reviews)} reviews"))

        # Orders (10 random orders)
        orders = []
        for _ in range(10):
            user = choice(users)
            order = Order.objects.create(user=user, status="Confirmed")
            products_sample = sample(products, k=3)
            for product in products_sample:
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    quantity=randint(1, 5),
                )
            orders.append(order)
        self.stdout.write(self.style.SUCCESS(f"Created {len(orders)} orders"))

        # Carts and CartItems (1 cart per user)
        for user in users:
            cart = Cart.objects.create(user=user)
            products_sample = sample(products, k=3)
            for product in products_sample:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=randint(1, 5),
                )
        self.stdout.write(
            self.style.SUCCESS(f"Created carts and cart items for all users")
        )

        self.stdout.write(
            self.style.SUCCESS("Database populated with real data successfully!")
        )
