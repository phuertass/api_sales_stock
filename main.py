from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from typing import List

app = FastAPI()


class ProductSales(BaseModel):
    productId: str
    sales: float


class ProductStock(BaseModel):
    productId: str
    stock: int


class SortProductsRequest(BaseModel):
    salesWeight: float
    stockWeight: float
    productSales: List[ProductSales]
    productStock: List[ProductStock]


@app.get("/hello")
def hello():
    """
    Endpoint para verificar que el servicio está activo.

    Returns:
        dict: Mensaje de saludo.
    """
    return {"message": "Hello, world!"}


@app.post("/sort-products")
def sort_products(request: SortProductsRequest):
    """
    Endpoint para ordenar productos basándose en las ventas y el stock.

    Args:
        request (SortProductsRequest): Datos de ventas, stock y ponderaciones para ordenar los productos.

    Returns:
        list: Lista de identificadores de productos ordenados por prioridad.
    """
    # Validar que las ponderaciones sumen 1
    if not (0 <= request.salesWeight <= 1 and 0 <= request.stockWeight <= 1):
        return {"error": "Las ponderaciones deben estar entre 0 y 1"}
    if request.salesWeight + request.stockWeight != 1:
        return {"error": "Las ponderaciones de ventas y stock deben sumar 1"}

    # Verificar que haya datos en productSales y productStock
    if not request.productSales:
        return {"error": "La lista productSales no puede estar vacía"}
    if not request.productStock:
        return {"error": "La lista productStock no puede estar vacía"}

    # Crear un diccionario para facilitar la búsqueda del stock por productId
    stock_dict = {product.productId: product.stock for product in request.productStock}

    # Calcular la prioridad de cada producto
    products_with_priority = []
    for product in request.productSales:
        stock = stock_dict.get(product.productId, 0)  # Obtener el stock del producto, si no existe se asume 0
        priority = (product.sales * request.salesWeight) + (stock * request.stockWeight)  # Calcular prioridad
        products_with_priority.append((product.productId, priority))

    # Ordenar los productos por prioridad de mayor a menor usando un bucle
    for i in range(len(products_with_priority)):
        for j in range(i + 1, len(products_with_priority)):
            if products_with_priority[i][1] < products_with_priority[j][1]:
                products_with_priority[i], products_with_priority[j] = products_with_priority[j], products_with_priority[i]

    # Devolver solo los identificadores de productos ordenados
    return [product[0] for product in products_with_priority]
