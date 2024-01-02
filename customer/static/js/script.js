const sunIcon = document.getElementById('light-mode');
const moonIcon = document.getElementById('dark-mode');

sunIcon.addEventListener('click', () => {
    document.body.classList.remove('dark-mode');
});

moonIcon.addEventListener('click', () => {
    document.body.classList.add('dark-mode');
});