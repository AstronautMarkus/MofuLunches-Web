document.addEventListener('DOMContentLoaded', () => {
    const categories = ['almuerzo', 'ensalada', 'bebestible', 'postre'];

    categories.forEach(category => {
        const list = document.getElementById(`${category}-list`);

        // Add Alimento
        list.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-item')) {
                const newItem = document.createElement('div');
                newItem.className = 'd-flex align-items-center mb-2';
                newItem.innerHTML = `
                    <select class="form-select">
                        <option value="" disabled selected>Seleccionar</option>
                        <option value="Nuevo Item">Nuevo Item</option>
                    </select>
                    <div class="ms-2">
                        <button class="btn btn-dark btn-sm add-item">+</button>
                        <button class="btn btn-danger btn-sm remove-item">-</button>
                    </div>
                `;
                list.appendChild(newItem);
            }

            // Delete alimento
            if (e.target.classList.contains('remove-item')) {
                e.target.closest('.d-flex').remove();
            }
        });
    });
});
