function setModalTitle(role) {
    document.getElementById('loginModalLabel').innerText = 'Login - ' + role;
}

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#loginModal form");
    const flashContainer = document.createElement("div");
    flashContainer.classList.add("flash-container");
    document.querySelector(".modal-body").prepend(flashContainer);

    let roleRequired = "";

    window.setModalTitle = function (role) {
        document.getElementById('loginModalLabel').innerText = 'Login - ' + role;
        roleRequired = role;
    };

    const loginModal = document.getElementById('loginModal');
    loginModal.addEventListener('hidden.bs.modal', function () {
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        flashContainer.innerHTML = '';
    });

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();
    
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
    
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });
    
        const result = await response.json();
    
        flashContainer.innerHTML = "";
    
        if (result.message) {
            const flashMessage = document.createElement("div");
            flashMessage.classList.add("alert", `alert-${response.ok ? "success" : "error"}`);
            flashMessage.textContent = result.message;
            flashContainer.appendChild(flashMessage);
        }
    
        if (response.ok) {
            setTimeout(() => {
                window.location.href = result.redirect_url;
            }, 1500);
        }
    });
    
});
