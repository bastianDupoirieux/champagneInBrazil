from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# --- DB setup ---
DATABASE_URL = "sqlite:///../db/champagneInBrazil.db"
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

# Reflect existing table
metadata = MetaData()
user_wine = Table("user_wine", metadata, autoload_with=engine)

# Use Inspector to get column info
inspector = inspect(engine)
columns = [col["name"] for col in inspector.get_columns("user_wine") if col["name"] != "id"]


@app.route("/", methods=["GET", "POST"])
def index():
    session = SessionLocal()

    if request.method == "POST":
        # Build insert dict dynamically from form values
        data = {col: request.form[col] for col in columns}
        session.execute(user_wine.insert().values(**data))
        session.commit()
        return redirect(url_for("index"))

    wines = session.execute(user_wine.select()).fetchall()
    session.close()

    return render_template("index.html", columns=columns, wines=wines)
