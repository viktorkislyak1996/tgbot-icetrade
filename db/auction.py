from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Date,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    select,
    UniqueConstraint,
    func,
    Text
)
from sqlalchemy.orm import relationship, sessionmaker

from .base import BaseModel


class Auction(BaseModel):
    __tablename__ = 'auction'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    customer_name = Column(String(256), nullable=True)
    country = Column(String(64), nullable=True)
    number = Column(String(128), nullable=True)
    price = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(64), nullable=True)
    expires_at = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())
    keyword = Column(String(128))
    tracking = Column(Boolean, nullable=False, default=False)
    link = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates="auctions")

    __table_args__ = (
        UniqueConstraint('user_id', 'keyword'),
    )

    def __repr__(self):
        return f'<Auction: {self.keyword}>'


# async def get_product(product_wb_id: int, user_id: int, session: sessionmaker) -> Product:
#     async with session() as session:
#         async with session.begin():
#             result = await session.execute(
#                 select(Product).filter(Product.wb_id == product_wb_id, Product.user_id == user_id)
#             )
#             product = result.scalar()
#             return product
#
#
# async def get_all_tracking_products(session: sessionmaker) -> list[Product]:
#     async with session() as session:
#         async with session.begin():
#             result = await session.execute(select(Product).where(Product.tracking == True))
#             products = result.scalars().all()
#             return products
#
#
async def get_all_tracking_auctions_by_user_id(user_id: int, session: sessionmaker) -> list[Auction]:
    async with session() as session:
        async with session.begin():
            result = await session.execute(
                select(Auction).filter(Auction.tracking == True, Auction.user_id == user_id)
            )
            auctions = result.scalars().all()
            return auctions
#
#
# async def get_all_products(user_id: int, session: sessionmaker) -> list[Product]:
#     async with session() as session:
#         async with session.begin():
#             result = await session.execute(select(Product).filter(Product.user_id == user_id))
#             products = result.scalars().all()
#             return products
#
#
# async def get_products_count(user_id: int, session: sessionmaker) -> int:
#     async with session() as session:
#         async with session.begin():
#             result = await session.execute(
#                 select(func.count())
#                 .select_from(Product)
#                 .filter(Product.user_id == user_id, Product.tracking == True)
#             )
#             total_count = result.scalar()
#             return total_count
#
#
# async def create_product(product_data: dict, session: sessionmaker) -> Product:
#     async with session() as session:
#         async with session.begin():
#             product = Product(**product_data)
#             session.add(product)
#         await session.commit()
#         return product
#
#
# async def update_product(product: Product, update_data: dict, session: sessionmaker) -> Product:
#     async with session() as session:
#         async with session.begin():
#             merged_product = await session.merge(product)
#             for key, value in update_data.items():
#                 setattr(merged_product, key, value)
#         await session.commit()
#         return merged_product
#
#
# async def delete_product(product: Product, session: sessionmaker) -> None:
#     async with session() as session:
#         async with session.begin():
#             merged_product = await session.merge(product)
#             await session.delete(merged_product)
#         await session.commit()
