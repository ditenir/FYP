
function checkPasswords() {
    var password = document.getElementById('registerPassword').value;
    var confirmPassword = document.getElementById('registerRepeatPassword').value;

    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }

    return true;
}
