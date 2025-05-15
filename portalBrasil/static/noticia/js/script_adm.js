document.addEventListener('DOMContentLoaded', function () {
    // Adicionar ação para o botão leia mais
    iniciarBotoesLeiaMais();


    
    const form = document.getElementById('newsForm');
    const fileUpload = document.getElementById('fileUpload');
    const fileInput = document.getElementById('imagem_url');
    const fileName = document.getElementById('fileName');

    fileUpload.addEventListener('click', function () {
        fileInput.click();
    });


    // Faz o upload da imagem usando preview 
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            // Atualiza o nome do arquivo
            fileName.textContent = file.name;
            fileName.classList.remove('hidden');
            fileUpload.classList.add('active');

            // Se for imagem, gera preview
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    let imgPreview = fileUpload.querySelector('img#filePreview');
                    if (!imgPreview) {
                        imgPreview = document.createElement('img');
                        imgPreview.id = 'filePreview';
                        imgPreview.style.maxWidth = '150px';
                        imgPreview.style.maxHeight = '150px';
                        imgPreview.style.marginTop = '10px';
                        fileUpload.appendChild(imgPreview);
                    }
                    imgPreview.src = e.target.result;
                    imgPreview.classList.remove('hidden');
                };

                reader.readAsDataURL(file);
            }
        } else {
            fileName.classList.add('hidden');
            fileUpload.classList.remove('active');

            // Remove preview se existir
            const imgPreview = fileUpload.querySelector('img#filePreview');
            if (imgPreview) {
                imgPreview.remove();
            }
        }
    });

    // Adiconar a função de arrastar e soltar arquivo no html
    fileUpload.addEventListener('dragover', function (e) {
        e.preventDefault();
        fileUpload.classList.add('bg-blue-50', 'border-blue-300');
    });

    fileUpload.addEventListener('dragleave', function () {
        fileUpload.classList.remove('bg-blue-50', 'border-blue-300');
    });

    fileUpload.addEventListener('drop', function (e) {
        e.preventDefault();
        fileUpload.classList.remove('bg-blue-50', 'border-blue-300');

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            const event = new Event('change');
            fileInput.dispatchEvent(event);
        }
    });

    // Preenche a data e hora atual
    const now = new Date();
    const timezoneOffset = now.getTimezoneOffset() * 60000;
    const localISOTime = (new Date(now - timezoneOffset)).toISOString().slice(0, 16);
    document.getElementById('data_publicacao').value = localISOTime;


    // Implementação de editor de texto para formulário
    const editorButtons = document.querySelectorAll('.editor-toolbar button');
    const conteudo = document.getElementById('conteudo');

    editorButtons.forEach(button => {
        button.addEventListener('click', function () {
            const command = this.querySelector('i').className.split(' ')[1];

            switch (command) {
                case 'fa-bold':
                    document.execCommand('bold', false, null);
                    break;
                case 'fa-italic':
                    document.execCommand('italic', false, null);
                    break;
                case 'fa-list-ul':
                    document.execCommand('insertUnorderedList', false, null);
                    break;
                case 'fa-link':
                    const url = prompt('Digite a URL do link:');
                    if (url) document.execCommand('createLink', false, url);
                    break;
                case 'fa-image':
                    const imgUrl = prompt('Digite a URL da imagem:');
                    if (imgUrl) document.execCommand('insertImage', false, imgUrl);
                    break;
            }

            conteudo.focus();
        });
    });


    // Executa o Botão Leia Mais
    function iniciarBotoesLeiaMais() {
        const botoesLeiaMais = document.querySelectorAll('.btn-leia-mais');

        botoesLeiaMais.forEach(botao => {
            botao.addEventListener('click', function () {
                // Encontra o conteúdo completo relacionado ao botão
                const conteudoCompleto = this.parentElement.querySelector('.conteudo-completo');

                // Verifica se o conteúdo está visível
                const estaVisivel = conteudoCompleto.style.display === 'block';

                // Alterna a visibilidade do conteúdo e o texto do botão
                if (estaVisivel) {
                    conteudoCompleto.style.display = 'none';
                    this.textContent = 'Leia mais';
                } else {
                    conteudoCompleto.style.display = 'block';
                    this.textContent = 'Mostrar menos';
                }
            });
        });
    }

    // Limpa todo formulário inclusive o preview da imagem
    form.addEventListener('reset', () => {
        // Esconde nome do arquivo
        fileName.textContent = '';
        fileName.classList.add('hidden');

        // Remove preview da imagem, se existir
        const imgPreview = fileUpload.querySelector('img#filePreview');
        if (imgPreview) {
            imgPreview.remove();
        }

        // Remove classe "active" do fileUpload
        fileUpload.classList.remove('active');
    });
})
