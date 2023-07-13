from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.responses import RedirectResponse
from ...Auth import handletoken
from ...database import User, Products
from typing import Annotated

cart = APIRouter(prefix="/api/v1", tags=["Carts"])


def getCorrect_Cart(email_data: str, name: str) -> bool:
    getCarts = User.objects(email=email_data).first().carts
    if len(getCarts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have any products in your carts.",
        )
    uname_list = []
    for clist in getCarts:
        uname_list.append(clist["uname"])
    if name not in uname_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You don't {name} product in your cart.",
        )
    return True


@cart.get(
    "/carts",
    summary="All the products you added in the Carts",
    description="Products in your Cart with Total price of all products.",
)
def getAllCarts(udata: tuple = Depends(handletoken)):
    getCarts = User.objects(email=udata[2]).first().carts
    pipeline = [
        {"$match": {"email": udata[2]}},
        {"$unwind": "$carts"},
        {"$group": {"_id": "$name", "Price": {"$sum": "$carts.price"}}},
    ]
    data = 0
    total_price = User.objects.aggregate(pipeline)
    for tt in total_price:
        data = tt["Price"]

    return {"Total Products": len(getCarts), "Total Price": data, "Carts": getCarts}


@cart.delete(
    "/cart/clear",
    summary="Clear all Products from Carts",
    description="Deletes all the products from your cart.",
    response_description="Cleared all Products.",
)
def deleteCarts(udata: tuple = Depends(handletoken)):
    getCarts = User.objects(email=udata[2])
    if len(getCarts.first().carts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have any products in your carts.",
        )
    getCarts.update_one(pull__carts={})
    return {"message": "Cleared all Products."}


@cart.get(
    "/cart/{name}",
    summary="Detail of Particular Product in Cart",
    description="Full Details of product that are present in the cart.",
)
def getCartDetails(
    name: Annotated[str, Path(description="Unique Name of the Product", example="bed")],
    udata: tuple = Depends(handletoken),
):
    if getCorrect_Cart(udata[2], name):
        return RedirectResponse(f"/api/v1/prod/{name}")


@cart.delete(
    "/cart/{name}",
    summary="Delete a product From your Cart",
    description="If you want to delete a product from your cart use this endpoint.",
    response_description="Deleted Successfully",
)
def deleteCartProduct(
    name: Annotated[str, Path(description="Unique Name of the Product", example="bed")],
    udata: tuple = Depends(handletoken),
):
    if getCorrect_Cart(udata[2], name):
        User.objects(email=udata[2]).update_one(pull__carts={"uname": name})
    return {"message": "Product Deleted From your Cart."}
