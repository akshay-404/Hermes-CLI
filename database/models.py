from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, String, LargeBinary, UniqueConstraint

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    ed25519_public_key: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    x25519_public_key: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<User {self.id} {self.username}>"
        

class SenderKeyState(Base):
    __tablename__ = "sender_keys"

    __table_args__ = (
        UniqueConstraint(
            "sender",
            "room_id",
            "key_id",
            name="uq_sender_room_key"
        ),
    )
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    sender: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    room_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    key_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    chain_key: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False
    )

    message_index: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<SenderKeyState "
            f"sender={self.sender} "
            f"room={self.room_id} "
            f"key_id={self.key_id}>"
        )
