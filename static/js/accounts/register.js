function get_form_data() {
    return new FormData(
        document.getElementById("registerForm")
    );
}

function try_register() {
    let form_data = get_form_data();
    console.log(form_data);
    let request = new XMLHttpRequest();
    request.open("POST", REGISTER_REQUEST_URL);
    request.onreadystatechange = () => {
        if (request.readyState !== 4) {
            return;
        }
        if (request.status !== 200) {
            // TODO - No content from backend
            console.log(request)
            alert(`Something went wrong, try again. Error: ${request.response}`);
        } else {
            console.log("HERE");
            window.location.href = REGISTER_SUCCESS_URL;
        }
    }
    request.send(form_data);
}