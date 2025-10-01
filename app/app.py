from flask import Flask, render_template, request, redirect, url_for, abort
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
_all_columns = [col for col in inspector.get_columns("user_wine")]

# Expose column names (except id) for form generation
columns = [col["name"] for col in _all_columns if col["name"] != "id"]

# Build column metadata maps for validation and casting
column_meta_by_name = {col["name"]: col for col in _all_columns}

def _cast_form_value_to_column_type(raw_value, column_meta):
    """Convert form input string to appropriate Python type for the given column.

    - Empty strings become None if the column is nullable; otherwise left as empty to trigger validation.
    - Integers/REAL are cast to int/float when provided.
    - Text remains as-is.
    """
    # Normalize whitespace
    value = raw_value.strip() if isinstance(raw_value, str) else raw_value

    # Handle empty string
    if value == "":
        return None if column_meta.get("nullable", True) else ""

    # Best-effort type casting based on SQLAlchemy-reflected type
    col_type = column_meta.get("type")
    try:
        python_type = getattr(col_type, "python_type")  # may raise NotImplementedError when accessed
        # Accessing attribute returns a property; call to get the type
        python_type = col_type.python_type
    except Exception:
        python_type = str

    # Numeric casting
    try:
        if python_type is int:
            return int(value)
        if python_type is float:
            return float(value)
    except ValueError:
        # Leave as original string if casting fails; DB may still accept text-compatible values
        return value

    # Default: keep string
    return value


@app.route("/", methods=["GET", "POST"])
def index():
    session = SessionLocal()

    if request.method == "POST":
        # Build insert dict dynamically from form values with proper NULL handling and type casting
        data = {}
        for col_name in columns:
            col_meta = column_meta_by_name.get(col_name, {})
            raw_value = request.form.get(col_name, "")
            cast_value = _cast_form_value_to_column_type(raw_value, col_meta)
            data[col_name] = cast_value

        # Enforce NOT NULL constraints (DDL: name text not null, producer text not null)
        required_fields = [c for c in columns if not column_meta_by_name.get(c, {}).get("nullable", True)]
        missing_required = [c for c in required_fields if data.get(c) in (None, "")]
        if missing_required:
            session.close()
            return abort(400, description=f"Missing required fields: {', '.join(missing_required)}")

        session.execute(user_wine.insert().values(**data))
        session.commit()
        return redirect(url_for("index"))

    wines = session.execute(user_wine.select()).fetchall()
    session.close()

    return render_template("index.html", columns=columns, wines=wines)
