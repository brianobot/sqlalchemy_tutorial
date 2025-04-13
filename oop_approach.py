import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

db = sa.create_engine("sqlite:///:memory:")

Session = sessionmaker(bind=db)

Base = declarative_base()
# This creates a base class for your ORM models. 
# When you subclass it (class User(Base)), SQLAlchemy knows to treat it as a database table.


class User(Base):
    __tablename__ = "users" # defines the name of the table in the DB.

    # The class attributes (like id, username, email) define the table's columns.
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    
    # This class will automatically be registered with Base.metadata — 
    # just like how Table(..., metadata, ...) did it manually before.
    

def main():
    Base.metadata.create_all(db)
    # It creates all tables tracked by Base.metadata using the bound engine (db).

    user = User(username="Brian Obot", email="brianobot9@gmail.com")

    # A Session is your gateway to the database in ORM land.
    # You use it to add, query, update, or 
    # delete Python objects that map to DB rows.
    with Session() as session:
        session.add(user) # Prepared an INSERT query
        session.commit() # Executed the query & persisted the user


if __name__ == "__main__":
    main()