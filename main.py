from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import engine
from auth import (
    get_db,
    hash_password,
    verify_password,
    create_access_token,
    get_current_admin
)


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0"
)


# USER ROUTES

@app.post("/register", response_model=schemas.UserOut)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    hashed_password = hash_password(
        user.password
    )

    return crud.create_user(
        db=db,
        user=user,
        hashed_password=hashed_password,
        role="user"
    )


@app.post("/admin/register", response_model=schemas.UserOut)
def register_admin(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    hashed_password = hash_password(
        user.password
    )

    return crud.create_user(
        db=db,
        user=user,
        hashed_password=hashed_password,
        role="admin"
    )


# LOGIN

@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(
        db,
        form_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/admin/login", response_model=schemas.Token)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(
        db,
        form_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins only."
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# PASSWORD ROUTES

@app.post("/forget-password")
def forget_password(
    request: schemas.ForgotPassword,
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_email(
        db,
        request.email
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "message": "User found. Proceed to reset password."
    }


@app.post("/reset-password")
def reset_password(
    request: schemas.ResetPassword,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(
        request.new_password
    )

    user = crud.update_password(
        db,
        request.email,
        hashed_password
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "message": "Password updated successfully."
    }


# PRODUCT ROUTES

@app.get("/products", response_model=list[schemas.ProductOut])
def get_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return crud.get_products(
        db,
        skip,
        limit
    )


@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = crud.get_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product


@app.post("/products", response_model=schemas.ProductOut)
def create_product(
    product: schemas.ProductCreate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    return crud.create_product(
        db,
        product,
        current_admin.id
    )


@app.put("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    updated_product = crud.update_product(
        db,
        product_id,
        product
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return updated_product


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    deleted_product = crud.delete_product(
        db,
        product_id
    )

    if deleted_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return {
        "message": "Product deleted successfully."
    }