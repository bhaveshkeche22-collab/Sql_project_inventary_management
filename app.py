from flask import Flask, render_template, request, jsonify
from database import get_connection



app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# Get all products
@app.route("/products", methods=["GET"])
def get_products():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products ORDER BY id DESC")

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(products)



# Add product
@app.route("/products", methods=["POST"])
def add_product():
    conn = None
    cursor = None

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "No valid JSON data received"}), 400

        name = data.get("name")
        category = data.get("category")
        quantity = data.get("quantity")
        price = data.get("price")

        if not name or not category or quantity is None or price is None:
            return jsonify({"error": "All fields are required"}), 400

        quantity = int(quantity)
        price = float(price)

        if quantity < 0 or price < 0:
            return jsonify({"error": "Quantity and price cannot be negative"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO products (name, category, quantity, price)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, category, quantity, price))
        conn.commit()

        return jsonify({"message": "Product added successfully"}), 201

    except (ValueError, TypeError):
        return jsonify({"error": "Quantity and price must be valid numbers"}), 400

    except Exception:
        app.logger.exception("Failed to add product")
        return jsonify({"error": "Database operation failed. Check server logs."}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# Update product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    data = request.json

    name = data["name"]
    category = data["category"]
    quantity = data["quantity"]
    price = data["price"]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE products
        SET name=%s,
            category=%s,
            quantity=%s,
            price=%s
        WHERE id=%s
    """

    cursor.execute(
        query,
        (name, category, quantity, price, id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Product updated successfully"})


# Delete product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Product deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)