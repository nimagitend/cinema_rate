document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.password-toggle');

    toggles.forEach((toggle) => {
        toggle.addEventListener('click', () => {
            const inputId = toggle.dataset.target;
            const input = document.getElementById(inputId);
            if (!input) return;

            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            toggle.innerHTML = isPassword
                ? '<i class="fa-solid fa-eye-slash"></i>'
                : '<i class="fa-solid fa-eye"></i>';
        });
    });

    const countrySelects = document.querySelectorAll('select.country-select');
    countrySelects.forEach((select) => {
        const searchInput = document.createElement('input');
        searchInput.type = 'search';
        searchInput.placeholder = 'Search country...';
        searchInput.className = 'country-search';
        select.parentNode.insertBefore(searchInput, select);

        const allOptions = Array.from(select.options).map((option) => ({
            value: option.value,
            text: option.text,
            selected: option.selected,
        }));

        searchInput.addEventListener('input', () => {
            const keyword = searchInput.value.trim().toLowerCase();
            const currentValue = select.value;
            select.innerHTML = '';

            allOptions
                .filter((option) => option.text.toLowerCase().includes(keyword) || option.value === '')
                .forEach((option) => {
                    const node = document.createElement('option');
                    node.value = option.value;
                    node.textContent = option.text;
                    node.selected = option.value === currentValue;
                    select.appendChild(node);
                });
        });
    });
});