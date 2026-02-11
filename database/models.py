import aiosqlite
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, Integer, ForeignKey, select, BigInteger, func, DateTime
from datetime import datetime

DB_PATH = "database.db"

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass



def get_db():
    return aiosqlite.connect(DB_PATH)


class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[String] = mapped_column(String(20))
    email: Mapped[String] = mapped_column(String(50), default="none")
    hashed_password: Mapped[str] = mapped_column(default="none")
    login: Mapped[str] = mapped_column(String,default="none")


class Broadcast(Base):
    __tablename__ = "broadcasts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[String] = mapped_column(String,default="none")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    sent_count: Mapped[int] = mapped_column(default=0)




