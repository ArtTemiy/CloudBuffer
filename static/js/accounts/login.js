function get_form_data() {
    return new FormData(
        document.getElementById("loginForm")
    );
}

const urlParams = new URLSearchParams(window.location.search);
const nextUrlParam = urlParams.get('next');
const nextUrlParamIsValid =
    nextUrlParam === "" ||
    nextUrlParam === undefined ||
    nextUrlParam === null;
const urlOnSuccess = nextUrlParamIsValid ? LOGIN_SUCCESS_URL : nextUrlParam;

function try_login() {
    let form_data = get_form_data();
    console.log(form_data);
    let request = new XMLHttpRequest();
    request.open("POST", LOGIN_REQUEST_URL);
    request.onreadystatechange = () => {
        if (request.readyState !== 4) {
            return;
        }
        if (request.status !== 200) {
            // TODO - No content from backend
            alert(`Something went wrong, try again. Error: ${request.response}`);
        } else {
            window.location.href = urlOnSuccess;
        }
    }
    request.send(form_data);
}