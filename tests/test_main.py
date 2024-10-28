from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app



client = TestClient(app)

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


def test_sort_products_valid_request():
    response = client.post("/sort-products", json={
        "salesWeight": 0.5,
        "stockWeight": 0.5,
        "productSales": [
            {"productId": "1", "sales": 50000},
            {"productId": "2", "sales": 100000},
            {"productId": "3", "sales": 100000},
            {"productId": "4", "sales": 75000}
        ],
        "productStock": [
            {"productId": "1", "stock": 100000},
            {"productId": "2", "stock": 400000},
            {"productId": "3", "stock": 200000},
            {"productId": "4", "stock": 300000}
        ]
    })
    assert response.status_code == 200
    assert response.json() == ["2", "4", "3", "1"]

def test_sort_products_invalid_weights():
    response = client.post("/sort-products", json={
        "salesWeight": 1.2,
        "stockWeight": -0.2,
        "productSales": [
            {"productId": "1", "sales": 50000},
            {"productId": "2", "sales": 100000}
        ],
        "productStock": [
            {"productId": "1", "stock": 200},
            {"productId": "2", "stock": 300}
        ]
    })
    assert response.status_code == 200
    assert response.json() == {"error": "Las ponderaciones deben estar entre 0 y 1"}

def test_sort_products_weights_not_sum_to_one():
    response = client.post("/sort-products", json={
        "salesWeight": 0.7,
        "stockWeight": 0.4,
        "productSales": [
            {"productId": "1", "sales": 50000},
            {"productId": "2", "sales": 100000}
        ],
        "productStock": [
            {"productId": "1", "stock": 200},
            {"productId": "2", "stock": 300}
        ]
    })
    assert response.status_code == 200
    assert response.json() == {"error": "Las ponderaciones de ventas y stock deben sumar 1"}

def test_sort_products_empty_product_sales():
    response = client.post("/sort-products", json={
        "salesWeight": 0.5,
        "stockWeight": 0.5,
        "productSales": [],
        "productStock": [
            {"productId": "1", "stock": 200},
            {"productId": "2", "stock": 300}
        ]
    })
    assert response.status_code == 200
    assert response.json() == {"error": "La lista productSales no puede estar vacía"}

def test_sort_products_empty_product_stock():
    response = client.post("/sort-products", json={
        "salesWeight": 0.5,
        "stockWeight": 0.5,
        "productSales": [
            {"productId": "1", "sales": 50000},
            {"productId": "2", "sales": 100000}
        ],
        "productStock": []
    })
    assert response.status_code == 200
    assert response.json() == {"error": "La lista productStock no puede estar vacía"}

"""
if __name__ == "__main__":
    test_hello()
    test_sort_products_valid_request()
    test_sort_products_invalid_weights()
    test_sort_products_weights_not_sum_to_one()
    test_sort_products_empty_product_sales()
    test_sort_products_empty_product_stock()
"""