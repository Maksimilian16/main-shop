from models import LoginPage, UsersTable, Products
from settings import session
from JWT_OP import create_access_token
from sqlalchemy import update


class UserActions():
    def __init__(self):
        self.LoginPage = LoginPage

    def login(self, name, password):
        x = UsersTable.email if "@" in name else UsersTable.login
        filt = session.query(UsersTable.password, UsersTable.email).filter(x == name).first()
        if filt and filt[0] == password:
            return create_access_token({"login": name, "email": filt.email})

        elif filt:
            return "password is wrong"

        else:
            return "account not found"

    def register(self, email, password, name, password_confirmation):
        if session.query(UsersTable).filter(UsersTable.login == name, UsersTable.email == email).first():
            return "this name or email already exists"

        elif password != password_confirmation:
            return "passwords don't match"

        else:
            session.add(UsersTable(login=name, password=password, email=email))
            session.commit()
            return create_access_token({"login": name, "email": email})


def account(account_id, token):
    result = session.query(UsersTable.basket, UsersTable.email, UsersTable.login).filter(
        UsersTable.id == account_id).first()
    if result:
        basket, email, login = result
        if email == token["login"]:
            return {"basket": basket, "email": email, "login": login}
        elif result:
            return {"login": login}

        else:
            return {"error": "Account not found"}

    else:
        return "there is no account like this"


def product_creating(name, price, token, description=None):
    session.add(Products(name=name, price=price, owner=token, description=description))
    session.commit()


def filters(pricemin=None, pricemax=None, name=None):
    if pricemin is not None:
        query = session.query(Products).filter(Products.price >= pricemin)

    if pricemax is not None:
        query = session.query(Products).filter(Products.price <= pricemax)

    if name is not None:
        query = session.query(Products).filter(Products.name.ilike(f'%{name}%'))

    return query.all()


def product_find(id):
    query = session.query(Products).filter(Products.id == id).first()
    return {"name": query.name,
            "price": query.price,
            "description": query.description,
            "owner": query.owner}


def basket_product(product_id, number, token):
    basket_list = session.query(UsersTable.basket).filter(UsersTable.login == token["login"]).first()
    if session.query(Products).filter(Products.id == product_id).first():
        pass
    else:
        return "there is no car like this"

    if basket_list is None:
        session.execute(update(UsersTable).where(UsersTable.login == token["login"]).values({UsersTable.basket: {product_id: number}}))
    else:
        basket_list[0].update({product_id: number})
        session.execute(update(UsersTable).where(UsersTable.login == token["login"]).values(
            {UsersTable.basket: basket_list[0]}))
    session.commit()
    return "Product added to your basket"


def basket(id):
    x = session.query(UsersTable.basket).filter(UsersTable.login == id).all()
    lst = []
    x_dict = x[0][0]
    for k, v in x_dict.items():
        y = session.query(Products).filter(Products.id == k).first()
        lst.append({
            "amount": v,
            "product_id": k,
            "price": y.price,
            "description": y.description,
            "name": y.name,
            "owner": y.owner
        })
    return lst
