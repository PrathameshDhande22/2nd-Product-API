import os
from fastapi import FastAPI
from .Routes import user, products, cart
from mongoengine import connect

description = """ 
## 2nd Product 

It means 2nd Hand products are available.

In this API user can register themselves, login to get access token use the access token in the header and explore the API, buy product, add to cart, delete product, add product.

"""

tags_metadata = [
    {
        "name": "Test The App",
        "description": "Test the App first to restart the server or to check if the server is running or not.",
    },
    {
        "name": "User",
        "description": "It consists of **Login** , **Register**, **Update** functionality. Allows you to access the API.",
    },
    {
        "name": "Products",
        "description": "Manage Your products, **Add Products**, **Get product by Query, tag or both**, **Delete Product**, **Buy Product**, **Access the Buy History** and **Add your Product to Cart**.",
    },
    {"name": "Carts", "description": "Manage your Product in Carts."},
]


def create_app() -> FastAPI:
    """Creates the app and includes the router"""
    api = FastAPI(
        title="2nd Product API",
        summary="This Api is example of E-commerce website just like OLX",
        version="v1.0.0",
        redoc_url=None,
        docs_url="/",
        contact={
            "name": "Prathamesh Dhande",
            "url": "https://www.github.com/prathameshdhande22",
            "email": "developerprathamesh.coder@gmail.com",
        },
        description=description,
        openapi_tags=tags_metadata,
    )

    connect(host=os.getenv("MONGODB_URI"))

    @api.get(
        "/test",
        tags=["Test The App"],
        summary="Use This endpoint first to Run the api successfully.",
        description="Starting with This endpoint enables the server to restart because it shutdowns after inactivity.",
        response_description="The app is restarted Succesfully.",
    )
    def test():
        return {"message": "hello World"}

    api.include_router(user)
    api.include_router(products)
    api.include_router(cart)

    return api
