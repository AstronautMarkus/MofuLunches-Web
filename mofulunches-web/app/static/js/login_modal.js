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

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password, role: roleRequired })
        });

        const result = await response.json();

        
        flashContainer.innerHTML = "";

        
        const flashMessages = await fetch("/get-flashes").then(res => res.json());

        flashMessages.forEach(message => {
            const flashMessage = document.createElement("div");
            flashMessage.classList.add("alert", `alert-${message.category}`);
            flashMessage.textContent = message.message;
            flashContainer.appendChild(flashMessage);
        });

        if (response.ok) {
            if (result.role === "Admin") {
                window.location.href = "/admin-dashboard";
            } else if (result.role === "Cocinero") {
                window.location.href = "/cocinero-dashboard";
            }
        }
    });
});
