from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

""" Contains all the model also known as REST Structure """


class Register(BaseModel):
    name: str = Field(examples=["Prathamesh Dhande"])
    email: EmailStr = Field(examples=["prathamesh@gmail.com"])
    phoneno: int = Field(examples=[1234567890])
    age: int = Field(examples=[21])
    address: str = Field(examples=["Gokuldham Society"])
    city: str = Field(examples=["Dadar"])
    state: str = Field(examples=["Maharashtra"])
    pincode: int = Field(examples=[400001])
    password: str = Field(examples=[1234578])


class UserData(BaseModel):
    name: str = Field(examples=["Prathamesh Dhande"])
    email: EmailStr = Field(examples=["prathamesh@gmail.com"])
    phoneno: int = Field(examples=[1234567890])
    age: int = Field(examples=[21])
    address: str = Field(examples=["Gokuldham Society"])
    city: str = Field(examples=["Dadar"])
    state: str = Field(examples=["Maharashtra"])
    pincode: int = Field(examples=[400001])


class UpdateUser(BaseModel):
    name: str = Field(examples=["Prathamesh Dhande"], default=None)
    phoneno: int = Field(examples=[1234567890], default=None)
    age: int = Field(examples=[21], default=None)
    address: str = Field(examples=["Gokuldham Society"], default=None)
    city: str = Field(examples=["Dadar"], default=None)
    state: str = Field(examples=["Maharashtra"], default=None)
    pincode: int = Field(examples=[400001], default=None)
    password: str = Field(examples=[1234578], default=None)


class Tags(str, Enum):
    FURNITURE = "Furniture"
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    HOME_APPLIANCES = "Home Appliances"
    BEAUTY_PERSONAL_CARE = "Beauty and Personal Care"
    BOOKS_STATIONERY = "Books and Stationery"
    SPORTS_FITNESS = "Sports and Fitness"
    TOYS_GAMES = "Toys and Games"
    AUTOMOTIVE = "Automotive"
    HEALTH_WELLNESS = "Health and Wellness"
    KITCHEN_DINING = "Kitchen and Dining"
    JEWELRY_ACCESSORIES = "Jewelry and Accessories"
    BABY_KIDS = "Baby and Kids"
    PET_SUPPLIES = "Pet Supplies"
    OUTDOOR_GARDEN = "Outdoor and Garden"
    OFFICE_SUPPLIES = "Office Supplies"
    ENTERTAINMENT = "Movies, Music, and Entertainment"
    GROCERIES_FOOD = "Groceries and Food"
    HOME_DECOR = "Home Decor"
    TOOLS_HARDWARE = "Tools and Hardware"


class ProductModel(BaseModel):
    name: str = Field(examples=["iPhone 13x with 11GB Ram"])
    uname: str = Field(examples=["iphone13"])
    tags: Tags = Field(examples=["Home Decor"])
    price: float = Field(examples=[1999])


class RealProduct(ProductModel):
    seller: str = Field(examples=["Seller Name"], default=None, hidden=True)
    addedDate: date = Field(default=datetime.today().date(), examples=["2023-03-21"])
    email: EmailStr = Field(default=None, examples=["john@gmail.com"])
