function addReviewSuccess() {
    alert("Review added successfully!");
}

function addReviewFailure() {
    alert("Failed to add review!");
}

function checkReview() {

    const description = document.getElementById("description").value;
    const allowedChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.!? ';

    if (description.length === 0) {
        alert("Please do not add an empty review!")
        document.getElementById("description").value = "";
        return false;
    }

    if (description.length > 100) {
        alert("Please do not add too long reviews!")
        document.getElementById("description").value = "";
        return false;
    }

    for (let i = 0; i < description.length; i++) {
        if (allowedChars.indexOf(description[i]) === -1) {
          alert("Unwanted characters in review! Please use only basic characters!")
          document.getElementById("description").value = "";
          return false;
        }
      }

    return true;
}