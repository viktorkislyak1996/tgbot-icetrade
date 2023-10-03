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
    offers_number = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates="auctions")

    __table_args__ = (
        UniqueConstraint('user_id', 'keyword'),
    )

    def __repr__(self):
        return f'<Auction: {self.keyword}>'


async def get_auction(keyword: str, user_id: int, session: sessionmaker) -> Auction:
    async with session() as session:
        async with session.begin():
            result = await session.execute(
                select(Auction).filter(Auction.keyword == keyword, Auction.user_id == user_id)
            )
            auction = result.scalar()
            return auction


async def get_all_tracking_auctions(session: sessionmaker) -> list[Auction]:
    async with session() as session:
        async with session.begin():
            result = await session.execute(select(Auction).where(Auction.tracking == True))
            auctions = result.scalars().all()
            return auctions


async def get_all_tracking_auctions_by_user_id(user_id: int, session: sessionmaker) -> list[Auction]:
    async with session() as session:
        async with session.begin():
            result = await session.execute(
                select(Auction).filter(Auction.tracking == True, Auction.user_id == user_id)
            )
            auctions = result.scalars().all()
            return auctions


async def get_all_auctions(user_id: int, session: sessionmaker) -> list[Auction]:
    async with session() as session:
        async with session.begin():
            result = await session.execute(select(Auction).filter(Auction.user_id == user_id))
            auctions = result.scalars().all()
            return auctions


async def get_keywords_count(user_id: int, session: sessionmaker) -> int:
    async with session() as session:
        async with session.begin():
            result = await session.execute(
                select(func.count())
                .select_from(Auction)
                .filter(Auction.user_id == user_id, Auction.tracking == True)
            )
            total_count = result.scalar()
            return total_count


async def create_auction(auction_data: dict, session: sessionmaker) -> Auction:
    async with session() as session:
        async with session.begin():
            auction = Auction(**auction_data)
            session.add(auction)
        await session.commit()
        return auction


async def update_auction(auction: Auction, update_data: dict, session: sessionmaker) -> Auction:
    async with session() as session:
        async with session.begin():
            merged_auction = await session.merge(auction)
            for key, value in update_data.items():
                setattr(merged_auction, key, value)
        await session.commit()
        return merged_auction


async def delete_auction(auction: Auction, session: sessionmaker) -> None:
    async with session() as session:
        async with session.begin():
            merged_auction = await session.merge(auction)
            await session.delete(merged_auction)
        await session.commit()
