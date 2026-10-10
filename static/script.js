let products = [];


async function loadProducts() {

    const response = await fetch("/products");

    products = await response.json();

    displayProducts(products);
}


function displayProducts(data) {

    const table = document.getElementById("productTable");

    table.innerHTML = "";

    data.forEach(product => {

        let status = "";
        let statusClass = "";

        if (product.quantity === 0) {

            status = "Out of Stock";
            statusClass = "out";

        } else if (product.quantity <= 5) {

            status = "Low Stock";
            statusClass = "low";

        } else {

            status = "Available";
            statusClass = "available";
        }


        table.innerHTML += `

            <tr>

                <td>${product.id}</td>

                <td>${product.name}</td>

                <td>${product.category}</td>

                <td>${product.quantity}</td>

                <td>₹${product.price}</td>

                <td class="${statusClass}">
                    ${status}
                </td>

                <td>

                    <button
                        class="edit-btn"
                        onclick="editProduct(${product.id})">
                        Edit
                    </button>

                    <button
                        class="delete-btn"
                        onclick="deleteProduct(${product.id})">
                        Delete
                    </button>

                </td>

            </tr>
        `;
    });
}


async function addProduct() {

    const name = document.getElementById("name").value.trim();

    const category = document.getElementById("category").value.trim();

    const quantity = document.getElementById("quantity").value;

    const price = document.getElementById("price").value;


    if (name === "" || category === "" || quantity === "" || price === "") {

        alert("Please fill all fields");

        return;

    }


    try {

        const response = await fetch("/products", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                name: name,
                category: category,
                quantity: Number(quantity),
                price: Number(price)

            })

        });


        const result = await response.json();

        alert(result.message);


        document.getElementById("name").value = "";

        document.getElementById("category").value = "";

        document.getElementById("quantity").value = "";

        document.getElementById("price").value = "";


        modal.style.display = "none";


        loadProducts();

    }

    catch (error) {

        console.error(error);

        alert("Something went wrong!");

    }

}


async function deleteProduct(id) {

    if (!confirm("Are you sure you want to delete this product?")) {
        return;
    }


    await fetch(`/products/${id}`, {

        method: "DELETE"

    });


    loadProducts();
}


async function editProduct(id) {

    const product = products.find(p => p.id === id);


    const name = prompt("Enter product name:", product.name);

    if (name === null) return;


    const category = prompt(
        "Enter category:",
        product.category
    );

    if (category === null) return;


    const quantity = prompt(
        "Enter quantity:",
        product.quantity
    );

    if (quantity === null) return;


    const price = prompt(
        "Enter price:",
        product.price
    );

    if (price === null) return;


    await fetch(`/products/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            name: name,
            category: category,
            quantity: quantity,
            price: price

        })

    });


    loadProducts();
}


function searchProduct() {

    const search =
        document.getElementById("search").value.toLowerCase();


    const filtered = products.filter(product =>

        product.name.toLowerCase().includes(search) ||

        product.category.toLowerCase().includes(search)

    );


    displayProducts(filtered);
}


loadProducts();
const addProductBtn = document.getElementById("addProductBtn");

const closeModalBtn = document.getElementById("closeModalBtn");

const modal = document.getElementById("productModal");


addProductBtn.addEventListener("click", function () {

    modal.style.display = "flex";

});


closeModalBtn.addEventListener("click", function () {

    modal.style.display = "none";

});


window.addEventListener("click", function (event) {

    if (event.target === modal) {

        modal.style.display = "none";

    }

});