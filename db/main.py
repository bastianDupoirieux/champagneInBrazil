from sqlalchemy import create_engine, MetaData, Table, select

# Path to your SQLite DB
engine = create_engine("sqlite:///champagneInBrazil.db")
print("Successfully connected to database")

metadata = MetaData()
user_wine = Table("user_wine", metadata, autoload_with=engine)


with engine.connect() as conn:
    stmt = select(user_wine)
    results = conn.execute(stmt).fetchall()
    for row in results:
        print(row)