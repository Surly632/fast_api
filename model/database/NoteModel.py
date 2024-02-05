from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ARRAY, UUID, Column, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from config.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    notes = relationship("NoteModel")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self, **kwargs):
        res = dict(self.__dict__)
        del res['password']
        del res['created_at']
        res.pop('updated_at')
        return res


class NoteModel(Base):
    __tablename__ = "notes"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(String(255))
    tags: Mapped[list[str]] = mapped_column(ARRAY(String(255)), default=[])
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class User(Base):
    __tablename__ = "_users_"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = "_addresses_"
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    user_id = Column(Integer, ForeignKey("_users_.id"))
    user = relationship("User", back_populates="addresses")
