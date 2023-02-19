function checkIfEmpty() {

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username == "" || password == "") {
        alert("Username or password field cannot be empty!");
        return false;
    }

    return true;

}

function showSuccess() {
    alert("User created successfully! You can now login!");
}

function showAdminSuccess() {
    alert("Admin-status user created successfully! You can now login!");
}

function showError() {
    alert("Wrong username or password!");
}