from fastapi import FastAPI, Body, Depends
from fastapi.encoders import jsonable_encoder

from .database import retrieve_products, add_product, retrieve_product, delete_product, update_product
from .models.products import ProductBase, ResponseModel, ErrorResponseModel, UpdateProduct
from .models.users import UserBase, UserLogin
from .auth.auth_handler import signJWT
from .auth.auth_bearer import JWTBearer

from .routes.products import router as ProductRouter

products = [
    {
        "id": 1,
        "name": "Thing",
        "price": "100.00",
        "description": "Lorem Ipsum ..."
    }
]

users = []

app = FastAPI()

app.include_router(ProductRouter, tags=["Product"], prefix="/product")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to fastapi!"}


@app.get("/", tags=["products_list"])
async def get_products() -> dict:
    products = await retrieve_products()
    if products:
        return ResponseModel(products, "Products data retrieved successfully")
    return ResponseModel(products, "Empty list returned")


@ProductRouter.get("/{id}", tags=["product_detail"])
async def get_single_product(id: int) -> dict:
    product = await retrieve_product(id)
    if product:
        return ResponseModel(product, "product data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "product doesn't exist.")


@app.post("/", dependencies=[Depends(JWTBearer())], tags=["product_create"])
async def add_product(product: ProductBase) -> dict:
    product.id = len(products) + 1
    product = jsonable_encoder(product)
    new_product = await add_product(product)
    return ResponseModel(new_product, "Product added successfully.")


@app.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_product_data(id: str, req: UpdateProduct= Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_product = await update_product(id, req)
    if updated_product:
        return ResponseModel(
            "Product with ID: {} name update is successful".format(id),
            "Product name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the product data.",
    )


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserBase = Body(...)):
    users.append(user)  # replace with db call, making sure to hash the password first
    return signJWT(user.email)


def check_user(data: UserLogin):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLogin = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
