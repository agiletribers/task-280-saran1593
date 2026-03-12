from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from passlib.hash import argon2
api= FastAPI()


users= [
    {"name":"saran","email":"saran@gmail.com","password":argon2.hash("saran123")},
    {"name":"vinu","email":"vinu@gmail.com","password":argon2.hash("vinu123")},
]
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
    {"id": 3, "name": "Tablet", "price": 299.99},
]

class Product(BaseModel):
    id: int
    name: str
    price: float

class User(BaseModel):
    email: str
    password: str
    
@api.post("/login")
def login(user:User):
    email=user.email
    password=user.password
    for u in users:
        if u["email"]==email and argon2.verify(password,u["password"]):
            return {"message":f"{u['name']} logged in successfully"}
    else:
        return {"message":"invalid credentials"}

@api.get("/products")
def get_products():
    return products
@api.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

class Request(BaseModel):
    num1 :int
    num2: int
    operator:Literal["add","subtract","multiply","divide"]

@api.post("/calculator")

def calculate(request:Request):
    a= request.num1
    b= request.num2
    operator=request.operator
    if operator=="add":
        return {"result": a + b}
    elif operator=="subtract":
        return {"result": a - b}
    elif operator=="multiply":
        return {"result": a * b}
    elif operator=="divide":
        if b == 0:
            return {"error": "Division by zero is not allowed."}
        return {"result": a / b}
    else:
        return {"error": "Invalid operator."}