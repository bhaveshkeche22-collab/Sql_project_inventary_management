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

    data = request.json

    name = data["name"]
    category = data["category"]
    quantity = data["quantity"]
    price = data["price"]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO products
        (name, category, quantity, price)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (name, category, quantity, price))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Product added successfully"})


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