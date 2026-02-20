document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.password-toggle');

    toggles.forEach((toggle) => {
        toggle.addEventListener('click', () => {
            const inputId = toggle.dataset.target;
            const input = document.getElementById(inputId);
            if (!input) return;

            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            toggle.textContent = isPassword ? '🙈' : '👁';
        });
    });
});