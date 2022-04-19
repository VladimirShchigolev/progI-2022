import re

from sqlalchemy import Column, Integer, String, Float, ForeignKey, select
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    personal_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    orders = relationship("Order", back_populates='client', cascade="all,delete")

    def __repr__(self):
        return f"Client(id={self.id!r}, name={self.name!r}, surname={self.surname!r})"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer, default=0)

    order_details = relationship("OrderDetail", back_populates='product', cascade="all,delete")

    @staticmethod
    def validate(name, price, amount, engine=None):
        if not name or not isinstance(name, str):
            raise TypeError("Wrong name format!")

        if not isinstance(price, str) or not re.search("^\d+(\.\d{0,2}){0,1}$", price):
            raise TypeError("Wrong price format!")

        if not isinstance(amount, int) or amount < 0:
            raise TypeError("Wrong amount format!")

        if engine:
            with Session(engine) as session:
                product = select(Product).where(Product.name == name)
                product = session.scalars(product).one_or_none()

                if product:
                    raise TypeError("Product with such name already exists!")

        return True

    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r})"

    def __str__(self):
        return f"{self.name}, {self.price}"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    number = Column(String, nullable=False)

    client = relationship("Client", back_populates='orders')
    order_details = relationship("OrderDetail", back_populates='order', cascade="all,delete")

    def __repr__(self):
        return f"Order(id={self.id!r}, number={self.number!r}, " + \
            f"client name={self.client.name}, client surname={self.client.surname})"


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

    amount = Column(Integer, default=1)

    order = relationship("Order", back_populates='order_details')
    product = relationship("Product", back_populates='order_details')

    def __repr__(self):
        return f"OrderDetail(id={self.id!r}, order={self.order.number!r}," + \
               f"product={self.product.name!r}, amount={self.amount!r})"
