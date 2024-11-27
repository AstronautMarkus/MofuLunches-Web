function setModalTitle(role) {
    document.getElementById('loginModalLabel').innerText = 'Login - ' + role;
}

function formatRUT(input) {
    let value = input.value.replace(/[^0-9kK]/g, '');
    if (value.length > 1) {
        value = value.slice(0, -1) + '-' + value.slice(-1);
    }
    if (value.length > 4) {
        value = value.slice(0, -5) + '.' + value.slice(-5);
    }
    if (value.length > 8) {
        value = value.slice(0, -9) + '.' + value.slice(-9);
    }
    input.value = value;
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

    const loadingSpinner = document.getElementById("loading-spinner");

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();
    
        let username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !password) {
            flashContainer.innerHTML = '<div class="alert alert-error">RUT y contraseña son requeridos.</div>';
            return;
        }

        // Remove formatting from RUT
        username = username.replace(/[\.\-]/g, '');

        loadingSpinner.style.display = "block";
    
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        loadingSpinner.style.display = "none";
    
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
