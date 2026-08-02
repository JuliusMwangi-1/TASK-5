from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


# PRODUCT CRUD

def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(models.Product)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_product(
    db: Session,
    product_id: int
):
    return (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )


def create_product(
    db: Session,
    product: schemas.ProductCreate,
    admin_id: int
):

    db_product = models.Product(
        **product.model_dump(),
        admin_id=admin_id
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductUpdate
):

    db_product = get_product(
        db,
        product_id
    )

    if db_product is None:
        return None

    update_data = product.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(
    db: Session,
    product_id: int
):

    db_product = get_product(
        db,
        product_id
    )

    if db_product is None:
        return None

    db.delete(db_product)
    db.commit()

    return db_product


# USER CRUD

def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def create_user(
    db: Session,
    user: schemas.UserCreate,
    hashed_password: str,
    role: str = "user"
):

    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        role=role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_password(
    db: Session,
    email: str,
    hashed_password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if user is None:
        return None

    user.password = hashed_password

    db.commit()
    db.refresh(user)

    return user

# ORDER CRUD

def create_order(
    db: Session,
    user_id: int,
    order: schemas.OrderCreate
):
    total_cost = 0

    db_order = models.Order(
        user_id=user_id,
        total_cost=0,
        status="Pending"
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:

        product = (
            db.query(models.Product)
            .filter(models.Product.id == item.product_id)
            .first()
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found."
            )

        subtotal = product.cost * item.quantity
        total_cost += subtotal

        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=item.quantity,
            subtotal=subtotal
        )

        db.add(order_item)

    db_order.total_cost = total_cost

    db.commit()
    db.refresh(db_order)

    return db_order


def get_order(
    db: Session,
    order_id: int
):
    return (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )


def update_order_status(
    db: Session,
    order_id: int,
    status: str
):
    order = get_order(
        db,
        order_id
    )

    if order is None:
        return None

    order.status = status

    db.commit()
    db.refresh(order)

    return order