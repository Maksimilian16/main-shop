from settings import app
from JWT_OP import verify_token
from fastapi import Depends
from models import LoginPage, RegistrationPage, ProductCreate, Filters
from backend import UserActions, account, product_creating, filters, product_find, basket_product, basket


@app.post("/login")
async def root(log: LoginPage):
    return UserActions().login(name=log.login, password=log.password)


@app.post("/register")
async def root(reg: RegistrationPage):
    return UserActions().register(email=reg.email, password=reg.password, name=reg.login, password_confirmation=reg.password_confirmation)


@app.get("/{user_id}")
async def main(user_id: int, decoded_token: dict = Depends(verify_token)):
    return account(user_id, decoded_token)


@app.post("/products/create")
async def creating(pr: ProductCreate, decoded_token: dict = Depends(verify_token)):
    return product_creating(name=pr.name, price=pr.price, description=pr.description, token=decoded_token["login"])


@app.post("/products/filters")
async def filt(flt: Filters):
    filters(pricemin=flt.min, pricemax=flt.max, name=flt.name)


@app.get("/products/{product_id}")
async def product_id(product_id: int, decoded_token: dict = Depends(verify_token)):
    return product_find(product_id)


@app.post("/products/basket/add")
async def basket_add(number: int, id: int, decoded_token: dict = Depends(verify_token)):
    basket_product(token=decoded_token, product_id=id, number=number)


@app.get("/products/basket/")
async def users_basket(decoded_token: dict = Depends(verify_token)):
    return basket(decoded_token["login"])