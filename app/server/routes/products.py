from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..database import (
    add_product,
    delete_product,
    retrieve_product,
    update_product,
)
from ..models.products import (
    ErrorResponseModel,
    ResponseModel,
    ProductBase,
    UpdateProduct
)

router = APIRouter()