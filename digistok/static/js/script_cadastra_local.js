document.addEventListener('DOMContentLoaded', function () {
    const selectAllCheckbox = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('input[name="locais_selecionados"]');

    selectAllCheckbox.addEventListener('change', function () {
        checkboxes.forEach(checkbox => checkbox.checked = this.checked);
    });


    // Função para resetar o formulário
    const limparBtn = document.querySelector('#btn-limpar');
    const form = document.querySelector('#localForm');

    // if (!limparBtn || !form) return;

    limparBtn.addEventListener('click', function () {
        form.reset();

    });

});
