document.addEventListener('DOMContentLoaded', function () {


    // Previe para Foto
    const input = document.querySelector('#photo');
    const preview = document.querySelector('#photoPreview');

    if (input) {
        input.addEventListener('change', function (event) {
            if (event.target.files && event.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(event.target.files[0]);
            } else {
                preview.src = '#';
                preview.style.display = 'none';
            }
        });
    }
    // Função para resetar o formulário
    const limparBtn = document.querySelector('#btn-limpar');
    const form = document.querySelector('#productForm');

    // if (!limparBtn || !form) return;

    limparBtn.addEventListener('click', function () {
        form.reset();

        // Esconder o preview da imagem
        if (preview) {
            preview.src = "#";
            preview.style.display = "none";
        }
    });



});

