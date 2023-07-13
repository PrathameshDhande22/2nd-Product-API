import json
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from ...database import Products, User
from ...models import ProductModel, RealProduct, Tags
from ...Auth import handletoken


products = APIRouter(prefix="/api/v1", tags=["Products"])


@products.post(
    "/addprod",
    summary="Add Your Products",
    response_description="Product added Successfully",
    status_code=status.HTTP_201_CREATED,
)
def addproduct(prodata: ProductModel, udata: tuple = Depends(handletoken)):
    """
    Sell your product by adding the product using these endpoint.

    It will automatically add your seller name and date you added the product.
    """
    product_already = Products.objects(uname=prodata.uname).scalar("id", "uname")
    if len(product_already) != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"{prodata.uname} already exists",
                "help": "Use Some Unique Name for adding the Product",
            },
        )
    new_product = RealProduct(**prodata.model_dump(), seller=udata[0], email=udata[2])
    Products(**new_product.model_dump()).save()
    return {"message": f"Product {prodata.name} Added Successfully."}


@products.get(
    "/prod/{name}",
    response_model=RealProduct,
    summary="Get the Particular Product Details",
    description="Get the Given unique name product Details.",
)
def getProduct(name: Annotated[str, Path(description="Unique Name of the Product", example="bed")]):
    getproducts = Products.objects(uname=name).fields(id=0).first()
    if getproducts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unique name = {name} product doesn't Exists.",
        )
    data = json.loads(getproducts.to_json())
    data["addedDate"] = str(getproducts.addedDate)
    return data


@products.get("/tags", summary="Get all tags", response_description="All Tags with their value")
def getalltags():
    """
    Get all tags with their value.
    """
    tag_dict = {}
    for g in Tags:
        tag_dict[str(g).removeprefix("Tags.")] = g.value
    return tag_dict


@products.get(
    "/prod",
    summary="Get Products by Tag, Query or All Products",
    response_description="List of Products",
)
def getProductAccording(
    tag: Annotated[
        Tags | None, Query(description="Tags of the Product", example="Electronics")
    ] = None,
    q: Annotated[str | None, Query(description="Query to search", example="phone")] = None,
):
    """
    Get the products according to given tag or query.

    If tag and query not given then fetches all the products.
    """
    import re

    regex = re.compile(f"(^|.){q}*", re.IGNORECASE)
    if q is None and tag is None:
        getproducts = list(Products.objects.fields(id=0).as_pymongo())
        return {"Total Products": len(getproducts), "products": getproducts}
    elif q is None:
        get_by_tags = list(Products.objects(tags=tag).fields(id=0).as_pymongo())
        return {f"{tag}": get_by_tags}
    elif tag is None:
        get_by_query = list(Products.objects(name=regex).fields(id=0).as_pymongo())
        return {f"{q}": get_by_query}
    else:
        get_by_both = list(Products.objects(name=regex, tags=tag).fields(id=0).as_pymongo())
        return {"Products": get_by_both}


@products.delete(
    "/prod/{name}",
    summary="Delete Your Own Products",
    response_description="Product Deleted Successfully",
    description="Deleting the Product which belongs to You by providing the product unique name.",
)
def deleteProduct(
    name: Annotated[str, Path(description="Unique Name of the Product", example="bed")],
    udata: tuple = Depends(handletoken),
):
    getProducts = Products.objects(uname=name).first()
    if getProducts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unique name = {name} product does not Exists.",
        )
    if udata[2] == getProducts.email:
        getProducts.delete()
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The product you are Trying to delete doesn't Belong to yours",
        )
    return {"message": "Product Deleted Successfully"}


@products.get(
    "/myprod",
    summary="View all your products",
    description="View all your products you added.",
    response_description="List of products.",
)
def getMyProducts(udata: tuple = Depends(handletoken)):
    getProducts = list(Products.objects(email=udata[2]).fields(id=0).as_pymongo())
    if len(getProducts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You Don't have any Products Added",
        )
    return {"Total Products": len(getProducts), "products": getProducts}


@products.get(
    "/prod/{name}/buy",
    summary="Buy Products",
    description="After Buying the product, it gets automatically deleted from the database.",
    response_description="Product Buyied Successfully",
)
def buyProduct(
    name: Annotated[str, Path(description="Unique Name of the Product", example="bed")],
    udata: tuple = Depends(handletoken),
):
    getProducts = Products.objects(uname=name).first()
    if getProducts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unique name = {name} product does not Exists.",
        )
    if getProducts.email == udata[2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You Cannot buy your Own Product",
        )

    User.objects(email=udata[2]).update_one(
        push__history={
            "name": getProducts.name,
            "uname": getProducts.uname,
            "seller": getProducts.seller,
            "tags": getProducts.tags,
            "addedDate": str(getProducts.addedDate),
            "price": getProducts.price,
            "email": getProducts.email,
        }
    )
    getProducts.delete()
    return {"message": "Product Buyied Successfully"}


@products.get(
    "/history",
    summary="Get History of Buyied Products",
    description="Product you buy are stored here and deleted from product.",
    response_description="List of Products",
)
def getHistory(udata: tuple = Depends(handletoken)):
    u_data = User.objects(email=udata[2]).fields(id=0).scalar("history")[0]
    return {"History": u_data}


@products.put(
    "/prod/{name}/addtocart",
    summary="Add Product to your cart.",
    description="Adds the particular product in your cart.",
    response_description="Product added Successfully.",
)
def addProductInCart(
    name: Annotated[str, Path(description="Unique Name of the Product", example="bed")],
    udata: tuple = Depends(handletoken),
):
    getProducts = Products.objects(uname=name).first()
    if getProducts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unique name = {name} product does not Exists.",
        )
    if getProducts.email == udata[2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You Cannot add your Own Product to cart",
        )

    present_data = User.objects(__raw__={"carts.uname": name, "email": udata[2]}).first()
    if present_data is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product already Exists in Your Cart",
        )
    User.objects(email=udata[2]).update_one(
        push__carts={
            "name": getProducts.name,
            "uname": getProducts.uname,
            "seller": getProducts.seller,
            "tags": getProducts.tags,
            "addedDate": str(getProducts.addedDate),
            "price": getProducts.price,
            "email": getProducts.email,
        }
    )
    return {"message": "Product Added to Cart."}
