function checkUserInput() {

    let searchQuery = document.getElementById("search_query").value;
    let maliciousCharacters = [">", "<", ">=", "<=", "/", "'", "&", "%", ";", "--", "/*", "*/", "<script>",
        "javascript:"
    ]

    for (let i = 0; i < maliciousCharacters.length; i++) {
        if (searchQuery.indexOf(maliciousCharacters[i]) !== -1) {
            alert("Malicious characters found. Please enter a valid input!");
            return false;
        }
    }

    return true;
}

function confirmDelete(productId) {
    if (window.confirm("Are you sure you want to delete this product?")) {
        window.location.href = "/delete_product/" + productId;
    }
}

function outOfStock() {
    alert("Error when adding to cart: Not enough stock available!")
}

function noProductFound() {
    alert("Error when adding to cart: Could not find product!")
}