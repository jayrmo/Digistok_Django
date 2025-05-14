document.addEventListener('DOMContentLoaded', function () {
    // File upload handling
    const fileUpload = document.getElementById('fileUpload');
    const fileInput = document.getElementById('imagem_url');
    const fileName = document.getElementById('fileName');

    fileUpload.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileName.textContent = file.name;
            fileName.classList.remove('hidden');
            fileUpload.classList.add('active');
        } else {
            fileName.classList.add('hidden');
            fileUpload.classList.remove('active');
        }
    });

    // Drag and drop functionality
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

    // Set default publication date to now
    const now = new Date();
    const timezoneOffset = now.getTimezoneOffset() * 60000;
    const localISOTime = (new Date(now - timezoneOffset)).toISOString().slice(0, 16);
    document.getElementById('data_publicacao').value = localISOTime;

    // Form submission
    const newsForm = document.getElementById('newsForm');
    newsForm.addEventListener('submit', function (e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(newsForm);
        const newsData = {};
        formData.forEach((value, key) => {
            newsData[key] = value;
        });

        // Here you would typically send the data to your server
        console.log('News data to be submitted:', newsData);

        // Simulate successful submission
        alert('Notícia enviada com sucesso! Será revisada antes da publicação.');
        newsForm.reset();
        fileName.classList.add('hidden');
        fileUpload.classList.remove('active');

        // Reset publication date to now
        document.getElementById('data_publicacao').value = localISOTime;
    });

    // Simple rich text editor functionality
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
});