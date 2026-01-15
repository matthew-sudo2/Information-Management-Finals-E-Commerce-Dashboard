from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..models import models
from .auth import get_current_user

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/customers", response_model=schemas.CustomerOut)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    existing = db.query(models.Customer).filter(models.Customer.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer already exists")
    customer = models.Customer(**payload.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/customers", response_model=list[schemas.CustomerOut])
def list_customers(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return db.query(models.Customer).all()


@router.post("/products", response_model=schemas.ProductOut)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    existing = db.query(models.Product).filter(models.Product.sku == payload.sku).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")
    product = models.Product(**payload.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return db.query(models.Product).all()


@router.post("/orders", response_model=schemas.SalesOrderOut)
def create_order(payload: schemas.SalesOrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == payload.product_id).first()
    customer = db.query(models.Customer).filter(models.Customer.id == payload.customer_id).first()
    if not product or not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product or customer not found")
    total_amount = product.price * payload.quantity
    order = models.SalesOrder(
        customer_id=payload.customer_id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        status=payload.status,
        total_amount=total_amount,
        sales_rep_id=current_user.id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders", response_model=list[schemas.SalesOrderOut])
def list_orders(db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    return db.query(models.SalesOrder).all()


@router.get("/orders/{order_id}", response_model=schemas.SalesOrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    order = db.query(models.SalesOrder).filter(models.SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=schemas.SalesOrderOut)
def update_order(order_id: int, payload: schemas.SalesOrderUpdate, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    order = db.query(models.SalesOrder).filter(models.SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if payload.quantity is not None:
        product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
        if product:
            order.quantity = payload.quantity
            order.total_amount = product.price * payload.quantity
    if payload.status is not None:
        order.status = payload.status

    db.commit()
    db.refresh(order)
    return order


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), _: models.User = Depends(get_current_user)):
    order = db.query(models.SalesOrder).filter(models.SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(order)
    db.commit()
    return None
