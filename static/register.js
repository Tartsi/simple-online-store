function checkUsernameAndPassword() {

    let username = document.getElementById("username").value;

    if (username.length < 4) {
        alert("Username must be atleast 4 characters long!")
        document.getElementById("username").value = "";
        return false;
    }

    let onlyLetters = /^[A-Za-z]+$/;

    if (!onlyLetters.test(username)) {
        alert("Username can only contain characters from A-Z!")
        document.getElementById("username").value = "";
        return false;
    }

    let password = document.getElementById("password").value;

    if (password.length < 5) {
        alert("Password must be at least 5 characters long!")
        document.getElementById("password").value = "";
        document.getElementById("confirm").value = "";
        return false;
    }

    let hasNumber = /\d/;

    if (!hasNumber.test(password)) {
        alert("Password must include atleast 1 number!")
        document.getElementById("password").value = "";
        document.getElementById("confirm").value = "";
        return false;
    }

    let confirmPassword = document.getElementById("confirm").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        document.getElementById("password").value = "";
        document.getElementById("confirm").value = "";
        return false;
    }

    return true;
}

function showError() {
    alert("This username is already in use!");
}

function togglePassword() {
    let passwordDiv = document.getElementById("password_div");
    let adminCheckbox = document.getElementById("admin");
    if (adminCheckbox.checked) {
        passwordDiv.style.display = "block";
    } else {
        passwordDiv.style.display = "none";
    }
}

function wrongAdminPassword() {
    alert("Admin password is incorrect!");
}