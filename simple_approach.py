import sqlalchemy as sa


# normally this is not something you're going to be doing often
engine = sa.create_engine(
    "sqlite:///:memory:"
)  # echo=True is a way to make the logs more verbose
connection = (
    engine.connect()
)  # this is what we would use to interact with the database all of the codebase that
# follows this functional approach


metadata = (
    sa.MetaData()
)  # this create a metadata object which defines a schema for the database

# create a table for the database
# in this case the table is called User and has 3 columns
user_table = sa.Table(
    "User",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String),
    sa.Column("email", sa.String),
)
# You're not just creating a table — you're registering that table with the metadata object you created.
# sa.Table(...) adds itself to metadata.tables — a dictionary that maps table names to Table objects.


def insert_user(username: str, email: str):
    query = user_table.insert().values(username=username, email=email)
    connection.execute(query)


def select_user(username: str):
    query = user_table.select().where(user_table.c.username == username)
    result = connection.execute(query)
    return result.fetchone()


def select_users(usernames: list[str]):
    # TODO: fix this to select all the users with their username in the list
    query = user_table.select().where(user_table.c.username in usernames)
    result = connection.execute(query)
    return result.fetchall()


def main():
    metadata.create_all(
        engine
    )  # this would create the database tables that are neccesary
    # It looks at everything in metadata.tables, and creates those tables on the database using the engine.
    insert_user("Brian Obot", "brianobot9@gmail.com")
    insert_user("Maryann Obot", "maryannokweu@gmail.com")
    print(select_user("Brian Obot"))
    print(select_users(["Brian Obot", "Maryann Obot"]))
    connection.close()


if __name__ == "__main__":
    main()
