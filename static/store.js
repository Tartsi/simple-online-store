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
    alert("Error when updating cart: Not enough stock available!");
}

function noProductFound() {
    alert("Could not find searched product!");
}

function addCartSuccess() {
    alert("Updated cart successfully!");
}

function purchaseSuccess() {
    alert("Thank you for your purchase!");
}