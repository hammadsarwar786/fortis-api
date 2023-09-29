from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi import APIRouter
from typing import List
import sqlite3

app = FastAPI()
router = APIRouter()

def connect_to_sqlite_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

def close_sqlite_db(conn):
    conn.close()

@router.get("/products/{product_id}/")
def read_product(product_id: int):
    db_path = 'ecommerce_db.db'
    conn, cursor = connect_to_sqlite_db(db_path)

    try:
        # Execute a SQL query to retrieve a product by ID
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Product not found")

        return result  # You may want to format the result as needed
    finally:
        close_sqlite_db(conn)

@router.get("/sales/")
def get_sales(
    start_date: str = Query(...),
    end_date: str = Query(...),
    category: str = Query(None),
    product_id: int = Query(None)
):
    db_path = 'ecommerce_db.db'
    conn, cursor = connect_to_sqlite_db(db_path)

    try:
        # Build the SQL query dynamically based on user-defined parameters
        query = "SELECT * FROM sales WHERE sale_date >= ? AND sale_date <= ?"
        params = [start_date, end_date]

        if category:
            query += " AND product_id IN (SELECT id FROM products WHERE category = ?)"
            params.append(category)

        if product_id:
            query += " AND product_id = ?"
            params.append(product_id)

        cursor.execute(query, params)
        results = cursor.fetchall()

        if not results:
            return []

        return results  # You may want to format the results as needed
    finally:
        close_sqlite_db(conn)

@router.get("/revenue/")
def analyze_revenue(
    start_date: str = Query(...),
    end_date: str = Query(...),
    category: str = Query(None),
    product_id: int = Query(None)
):
    db_path = 'ecommerce_db.db'
    conn, cursor = connect_to_sqlite_db(db_path)

    try:
        # Build the SQL query dynamically based on user-defined parameters
        query = "SELECT SUM(revenue) AS total_revenue FROM sales WHERE sale_date >= ? AND sale_date <= ?"
        params = [start_date, end_date]

        if category:
            query += " AND product_id IN (SELECT id FROM products WHERE category = ?)"
            params.append(category)

        if product_id:
            query += " AND product_id = ?"
            params.append(product_id)

        cursor.execute(query, params)
        result = cursor.fetchone()

        total_revenue = result[0] if result else 0
        return {"total_revenue": total_revenue}
    finally:
        close_sqlite_db(conn)

@router.get("/inventory/{product_id}/")
def get_inventory(product_id: int):
    db_path = 'ecommerce_db.db'
    conn, cursor = connect_to_sqlite_db(db_path)

    try:
        # Execute a SQL query to retrieve inventory status by product ID
        cursor.execute("SELECT * FROM inventory WHERE product_id = ?", (product_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Inventory not found")

        return result  # You may want to format the result as needed
    finally:
        close_sqlite_db(conn)

@router.put("/inventory/{product_id}/")
def update_inventory(product_id: int, stock_quantity: int):
    db_path = 'ecommerce_db.db'
    conn, cursor = connect_to_sqlite_db(db_path)

    try:
        # Execute a SQL query to update inventory levels for a specific product
        cursor.execute("UPDATE inventory SET stock_quantity = stock_quantity + ? WHERE product_id = ?", (stock_quantity, product_id))
        conn.commit()

        return {"message": "Inventory updated successfully"}
    finally:
        close_sqlite_db(conn)

# Define other routes similarly

app.include_router(router)
