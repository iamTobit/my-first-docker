function loadProducts() {
    fetch("http://localhost:5005/products")
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch products");
            }
            return response.json();
        })
        .then(data => {
            const list = document.getElementById("productList");
            list.innerHTML = "";

            if (Array.isArray(data.products)) {
                data.products.forEach(product => {
                    const li = document.createElement("li");
                    li.textContent = `${product.id} - ${product.name}`;
                    list.appendChild(li);
                });
            } else {
                console.error("Unexpected response:", data);
            }
        })
        .catch(error => console.error("Error:", error));
}