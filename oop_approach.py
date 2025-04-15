import sqlalchemy as sa
from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, relationship
from sqlalchemy.orm import DeclarativeBase

db = sa.create_engine("sqlite:///:memory:")

Session = sessionmaker(bind=db)

class Base(DeclarativeBase):
    pass
# This creates a base class for your ORM models. 
# When you subclass it (class User(Base)), SQLAlchemy knows to treat it as a database table.


# all our models must inherit from the Base model, this is so because
# the base model has to be keep track of models it has to create or change or update
# this structure is known as a declarative mapping,
class User(Base):
    __tablename__ = "users" # defines the name of the table in the DB.

    # The class attributes (like id, username, email) define the table's columns.
    # every model musy have an primary key column
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True) 
    # for simple fields, just a Mapped[<field_type>] is enough
    # but if you want more constraint, use a mapped_column function to declare your requirements
    username: Mapped[str]
    email: Mapped[str]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    # This class will automatically be registered with Base.metadata — 
    # just like how Table(..., metadata, ...) did it manually before.

    # taken together the combination of the string table bane as well as the list of column declaration is known
    # in SQLAlchemy as table metadata, the example above is know as Annotated Declarative Tbale configuration


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    # relationship denotes a linktage between two ORM classes
    address: Mapped[str]

    def __repr__(self) -> str:
        return f"Address(id={self.id}, address={self.address[:15]}{"..." if len(self.address) > 15 else ""})"
    

def main():
    Base.metadata.create_all(db)
    # It creates all tables tracked by Base.metadata using the bound engine (db).

    user = User(
        username="Brian Obot", 
        email="brianobot9@gmail.com",
        addresses = [
            Address(address="Short address"),
            Address(address="SOme random address"),
        ]
    )
    another_user = User(
        username="Maryann Obot", 
        email="maryannokewu@gmail.com",
        addresses = []
    )

    # A Session is your gateway to the database in ORM land.
    # You use it to add, query, update, or 
    # delete Python objects that map to DB rows.
    with Session() as session:
        session.add(user) # Prepared an INSERT query
        session.commit() # Executed the query & persisted the user

        session.add(another_user)
        session.commit()

        print(session.query(User).all())
        print(session.query(Address).all())

        first_user = session.query(User).all()[0]
        print(f"{first_user.addresses = }")

        isolated_address = Address(user_id=first_user.id, address="Special Isolated Address")
        session.add(isolated_address)
        session.commit()

        address_x = Address(user=first_user, address="Address x")
        session.add(address_x)
        session.commit()

        print(f"{first_user.addresses[-1].address = }")

        # use the session's add_all method to add multiple objects of the same type
        users = [User(username=f"username_{i}", email=f"email{i}@gmail.com") for i in range(3)]
        addresses = [Address(user=first_user, address=f"address {i}") for i in range(3)]

        session.add_all(users)
        session.add_all(addresses)

        # this is also possible, interesting stuffs
        mixed_classes = users + addresses
        session.add_all(mixed_classes)


if __name__ == "__main__":
    main()