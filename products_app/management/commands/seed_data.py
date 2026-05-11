"""
Seed data script - Run with: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products_app.models import Product, Category
from users_app.models import UserProfile
from orders_app.models import Order
from payments_app.models import Payment
from reviews_app.models import Review
from budget_app.models import Budget


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create superuser / admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@shopbd.com', 'admin123')
            UserProfile.objects.get_or_create(user=admin, defaults={'phone': '01700000000', 'address': 'Dhaka, Bangladesh'})
            self.stdout.write('  ✓ Admin user: admin / admin123')

        # Regular user
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user('testuser', 'user@shopbd.com', 'test1234', first_name='Test', last_name='User')
            UserProfile.objects.get_or_create(user=user, defaults={'phone': '01800000000', 'address': 'Chittagong, Bangladesh'})
            self.stdout.write('  ✓ Test user: testuser / test1234')

        # Categories
        cats = ['Electronics', 'Clothing', 'Books', 'Home & Living', 'Sports']
        cat_objs = {}
        for cat in cats:
            obj, _ = Category.objects.get_or_create(name=cat)
            cat_objs[cat] = obj
        self.stdout.write(f'  ✓ {len(cats)} categories')

        # Products
        products_data = [
            ('Wireless Headphones', 'High-quality Bluetooth 5.0 headphones with 30hr battery life and noise cancellation.', 2499, 50, 'Electronics'),
            ('Cotton T-Shirt', 'Premium quality cotton t-shirt, available in multiple colors. Comfortable for all-day wear.', 499, 100, 'Clothing'),
            ('Python Programming Book', 'Complete guide to Python programming from beginner to advanced. Includes exercises.', 899, 30, 'Books'),
            ('Ceramic Coffee Mug', 'Handcrafted ceramic mug, 350ml capacity. Dishwasher safe.', 299, 75, 'Home & Living'),
            ('Running Shoes', 'Lightweight running shoes with cushioned sole. Great for jogging and gym.', 3499, 40, 'Sports'),
            ('Laptop Stand', 'Adjustable aluminium laptop stand for better ergonomics. Compatible with all laptops.', 1299, 60, 'Electronics'),
            ('Denim Jeans', 'Classic straight-fit denim jeans. Durable and stylish for everyday wear.', 1499, 80, 'Clothing'),
            ('Data Structures Book', 'Learn data structures and algorithms with real-world examples and problems.', 799, 25, 'Books'),
        ]

        for name, desc, price, stock, cat_name in products_data:
            Product.objects.get_or_create(
                product_name=name,
                defaults={'description': desc, 'price': price, 'stock': stock, 'category': cat_objs[cat_name]}
            )
        self.stdout.write(f'  ✓ {len(products_data)} products')

        # Budget records
        budgets = [
            (1, 2025, 150000, 95000),
            (2, 2025, 180000, 110000),
            (3, 2025, 220000, 130000),
            (4, 2025, 195000, 115000),
        ]
        for month, year, income, expense in budgets:
            Budget.objects.get_or_create(
                month=month, year=year,
                defaults={'total_income': income, 'total_expense': expense}
            )
        self.stdout.write(f'  ✓ {len(budgets)} budget records')

        self.stdout.write(self.style.SUCCESS('\n✅ Seed data created successfully!'))
        self.stdout.write('   Admin panel: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Login: admin / admin123')
