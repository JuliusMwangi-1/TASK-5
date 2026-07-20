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