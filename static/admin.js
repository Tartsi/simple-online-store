function checkAddNewProduct() {

    let name = document.getElementById("add_name").value;
    let description = document.getElementById("description").value;
    let price = document.getElementById("price").value;
    let amount = document.getElementById("add_product_amount").value;
    let onlyLetters = /^[A-Za-z]+$/;
    let onlyNumbers = /^\d+$/;

    if (name.length < 3) {
        alert("Product name must be at least 3 characters long!");
        document.getElementById("add_name").value = "";
        return false;
    }

    if (!onlyLetters.test(name)) {
        alert("Product name can contain only letters!");
        document.getElementById("add_name").value = "";
        return false;
    }

    if (description.length < 5) {
        alert("Product description must be atleast 5 characters long!");
        document.getElementById("description").value = "";
        return false;
    }

    if (price <= 0) {
        alert("Price must be greater than zero!")
        document.getElementById("price").value = "";
        return false;
    }

    if (!onlyNumbers.test(price)) {
        alert("Price must contain only numbers!");
        document.getElementById("price").value = "";
        return false;
    }

    if (amount <= 0) {
        alert("Product amount must be greater than 0!")
        document.getElementById("add_product_amount").value = "";
        return false;
    }

    return true;
}

function checkIncreaseStock() {

    let name = document.getElementById("increase_name").value;
    let increaseAmount = document.getElementById("increase_amount").value;
    let onlyLetters = /^[A-Za-z]+$/;

    if (name.length < 3) {
        alert("Products name that you want to increase must be at least 3 characters long!");
        document.getElementById("increase_name").value = "";
        return false;
    }

    if (!onlyLetters.test(name)) {
        alert("Product name can contain only letters!");
        document.getElementById("increase_name").value = "";
        return false;
    }

    if (increaseAmount <= 0) {
        alert("Amount to increase must be greater that 0!");
        document.getElementById("increase_amount").value = "";
        return false;
    }

    return true;

}

function showDuplicateError() {
    alert("This product is already in the list of products!");
}

function showAddSuccess() {
    alert("Product has been successfully added!");
}

function showIncreaseError() {
    alert("This product does not exist!");
}

function showIncreaseSuccess() {
    alert("Product stock increased succesfully!");
}

function userDeleteError() {
    alert("Failed to delete user!");
}

function userDeleteSuccess() {
    alert("User deleted successfully!");
}