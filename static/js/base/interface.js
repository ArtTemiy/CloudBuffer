function go_to_page(url) {
    window.location.href = url;
}

const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;
