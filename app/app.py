from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# --- DB setup ---
DATABASE_URL = "sqlite:///../db/champagneInBrazil.db"
engine = create_engine(DATABASE_URL, future=True)
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


@app.route("/")
def entry_page():
    # Default to My Cellar view
    return redirect(url_for('my_cellar'))


@app.route("/add", methods=["GET", "POST"])
def add_wine():
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
        return redirect(url_for("entry_page"))

    wines = session.execute(user_wine.select()).fetchall()
    session.close()

    return render_template("index.html", columns=columns, wines=wines)


@app.route("/cellar")
def my_cellar():
    session = SessionLocal()
    wines = session.execute(user_wine.select().where(user_wine.c.expired == 0)).fetchall()
    session.close()
    return render_template("my_cellar.html", wines=wines, columns=columns)


@app.route("/experienced")
def experienced_wines():
    session = SessionLocal()
    wines = session.execute(user_wine.select().where(user_wine.c.expired == 1)).fetchall()
    session.close()
    return render_template("experienced_wines.html", wines=wines, columns=columns)


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/map")
def map_page():
    return render_template("map.html")


@app.route("/wine/<int:wine_id>")
def wine_detail(wine_id):
    session = SessionLocal()
    wine = session.execute(user_wine.select().where(user_wine.c.id == wine_id)).fetchone()
    session.close()
    
    if not wine:
        return abort(404, description="Wine not found")
    
    return render_template("wine_detail.html", wine=wine, columns=columns)


@app.route("/wine/<int:wine_id>/edit", methods=["GET", "POST"])
def edit_wine(wine_id):
    session = SessionLocal()
    wine = session.execute(user_wine.select().where(user_wine.c.id == wine_id)).fetchone()

    if not wine:
        session.close()
        return abort(404, description="Wine not found")
    
    if request.method == "POST":
        # Build update dict dynamically from form values with proper NULL handling and type casting
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
        
        # Update the wine
        session.execute(user_wine.update().where(user_wine.c.id == wine_id).values(**data))
        session.commit()
        session.close()
        
        return redirect(url_for('wine_detail', wine_id=wine_id))
    
    session.close()
    return render_template("edit_wine.html", wine=wine, columns=columns)


@app.route("/wine/<int:wine_id>/field/<field_name>", methods=["POST"])
def update_wine_field(wine_id, field_name):
    session = SessionLocal()
    wine = session.execute(user_wine.select().where(user_wine.c.id == wine_id)).fetchone()
    
    if not wine:
        session.close()
        return jsonify({"success": False, "error": "Wine not found"})
    
    if field_name not in columns:
        session.close()
        return jsonify({"success": False, "error": "Invalid field"})
    
    try:
        data = request.get_json()
        new_value = data.get('value', '')
        
        # Type casting and validation
        col_meta = column_meta_by_name.get(field_name, {})
        cast_value = _cast_form_value_to_column_type(new_value, col_meta)
        
        # Check required fields
        if not column_meta_by_name.get(field_name, {}).get("nullable", True) and cast_value in (None, ""):
            session.close()
            return jsonify({"success": False, "error": f"{field_name} is required"})
        
        # Update the field
        session.execute(user_wine.update().where(user_wine.c.id == wine_id).values(**{field_name: cast_value}))
        session.commit()
        session.close()
        
        return jsonify({"success": True})
    except Exception as e:
        session.close()
        return jsonify({"success": False, "error": str(e)})


@app.route("/wine/<int:wine_id>/delete", methods=["GET", "POST"]) 
def delete_wine(wine_id):
    session = SessionLocal()
    wine = session.execute(user_wine.select().where(user_wine.c.id == wine_id)).fetchone()
    
    if not wine:
        session.close()
        return abort(404, description="Wine not found")
    
    if request.method == "POST":
        # Delete the wine
        session.execute(user_wine.delete().where(user_wine.c.id == wine_id))
        session.commit()
        session.close()
        
        # Redirect to the appropriate list based on expired status
        if wine.expired == 0:
            return redirect(url_for('my_cellar'))
        else:
            return redirect(url_for('experienced_wines'))
    
    # GET request - show confirmation page
    session.close()
    return render_template("delete_confirm.html", wine=wine)

@app.route("/wine/<int:wine_id>/json")
def wine_json(wine_id):
    session = SessionLocal()
    wine = session.execute(user_wine.select().where(user_wine.c.id == wine_id)).fetchone()
    session.close()
    if not wine:
        return abort(404)
    return dict(wine._mapping)  # convert SQLAlchemy Row to dict
