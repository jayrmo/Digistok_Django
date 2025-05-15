
document.addEventListener('DOMContentLoaded', function () {
    // Toggle password visibility
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    togglePassword.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.querySelector('i').classList.toggle('fa-eye-slash');
        this.querySelector('i').classList.toggle('fa-eye');
    });

    // Form submission
    // const loginForm = document.getElementById('loginForm');
    // loginForm.addEventListener('submit', function (e) {
    //     e.preventDefault();

    //     const email = document.getElementById('email').value;
    //     const password = document.getElementById('password').value;

    //     // Simple validation
    //     if (!email || !password) {
    //         alert('Por favor, preencha todos os campos.');
    //         return;
    //     }

    //     // Here you would typically send the data to your server
    //     console.log('Login attempt with:', { email, password });

    //     // Simulate successful login
    //     alert('Login realizado com sucesso! Redirecionando...');
    //     // window.location.href = 'dashboard.html';
    // });
});