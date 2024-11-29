document.addEventListener("DOMContentLoaded", () => {

    const addNewEntry = (e) => {
        const parent = e.target.closest(".item-list"); 
        const selectTemplate = parent.querySelector(".d-flex"); 

        if (selectTemplate) {
            const newSelect = selectTemplate.cloneNode(true);


            const select = newSelect.querySelector("select");
            if (select) {
                select.value = ""; 
            }

            newSelect.querySelectorAll("button").forEach((btn) => {
                btn.removeEventListener("click", addNewEntry);
                btn.removeEventListener("click", removeEntry);
            });

            const removeButton = newSelect.querySelector(".remove-item");
            if (removeButton) {
                removeButton.addEventListener("click", removeEntry);
            }

            parent.appendChild(newSelect);
        }
    };

    const removeEntry = (e) => {
        const parent = e.target.closest(".item-list"); 
        const item = e.target.closest(".d-flex");

        if (parent.children.length > 1) {

            item.remove();
        } else {

            alert("No puedes eliminar la última opción.");
        }
    };


    const addNewButtonIfEmpty = () => {
        document.querySelectorAll(".item-list").forEach((list) => {
            if (list.children.length === 0) {

                const emptyMessage = document.createElement("div");
                emptyMessage.classList.add("text-center", "mt-2");
                emptyMessage.innerHTML = `
                    <button class="btn btn-dark btn-sm add-item">Agregar una nueva entrada</button>
                `;

                list.appendChild(emptyMessage);


                emptyMessage.querySelector(".add-item").addEventListener("click", (e) => {
                    addNewEntry(e);
                    emptyMessage.remove(); 
                });
            }
        });
    };


    document.querySelectorAll(".add-item").forEach((button) => {
        button.addEventListener("click", addNewEntry);
    });

    document.querySelectorAll(".remove-item").forEach((button) => {
        button.addEventListener("click", removeEntry);
    });


    addNewButtonIfEmpty();
});
