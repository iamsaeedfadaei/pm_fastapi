from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ProductBase(BaseModel):
    id: int = Field(default=None)
    name: str = Field(..., max_length=100)
    price: int = Field(..., gt=0, description="قیمت باید بیشتر از صفر باشد")
    description: Optional[str] = Field(..., max_length=300)

    class Config:
        schema_extra = {
            "example": {
                "name": "نام محصول",
                "price": "قیمت",
                "description": "توضیحات",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 201,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error,
            "code": code,
            "message": message
            }


class UpdateProduct(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "نام محصول",
                "price": "قیمت",
                "description": "توضیحات",
            }
        }