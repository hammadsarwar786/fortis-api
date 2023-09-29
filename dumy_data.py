import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *


# Define the database URL
DATABASE_URL = "sqlite:///./ecommerce_db.db"  # Adjust the path if needed

# Create an SQLite database connection
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to generate dummy data and insert it into the database
def create_dummy_data():
    # Create a database session
    db = SessionLocal()

    # Generate 100 dummy products
    for i in range(1, 101):
        product = Product(
            name=f"Product {i}",
            description=f"Description for Product {i}",
            price=random.uniform(10.0, 100.0),
            category=random.choice(["Electronics", "Clothing", "Home", "Sports", "Books"]),
        )
        db.add(product)

    # Commit the products to the database
    db.commit()

    # Generate sales and inventory data
    for product_id in range(1, 101):
        for _ in range(random.randint(1, 5)):
            sale_date = datetime.now() - timedelta(days=random.randint(1, 365))
            sale = Sale(
                product_id=product_id,
                sale_date=sale_date.date(),
                quantity=random.randint(1, 20),
                revenue=random.uniform(10.0, 100.0),
            )
            db.add(sale)

            inventory = Inventory(
                product_id=product_id,
                stock_quantity=random.randint(10, 100),
            )
            db.add(inventory)

    # Commit the sales and inventory data to the database
    db.commit()

    # Close the database session
    db.close()

if __name__ == "__main__":
    create_dummy_data()
    print("Dummy data has been inserted into the database.")
