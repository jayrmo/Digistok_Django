// Simulação de banco de dados para categorias
// let categories = ['Eletrônicos', 'Alimentos', 'Bebidas', 'Limpeza', 'Escritório'];

// Simulação de banco de dados para fornecedores
// let suppliers = ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D', 'Fornecedor E', 'Fornecedor F'];

// Carrega as categorias quando a página é carregada
// document.addEventListener('DOMContentLoaded', function () {
    // loadCategories();
    // loadExistingCategories();

    // Configura os dropdowns
    // document.getElementById('unit').addEventListener('click', function () {
    //     document.getElementById('unitDropdown').classList.toggle('show');
    // });

    // document.getElementById('supplier').addEventListener('click', function () {
    //     document.getElementById('supplierDropdown').classList.toggle('show');
    // });

    // Fecha os dropdowns se clicar fora
//     window.onclick = function (event) {
//         if (!event.target.matches('#unit') && !event.target.matches('#supplier')) {
//             var dropdowns = document.getElementsByClassName("dropdown-content");
//             for (var i = 0; i < dropdowns.length; i++) {
//                 var openDropdown = dropdowns[i];
//                 if (openDropdown.classList.contains('show')) {
//                     openDropdown.classList.remove('show');
//                 }
//             }

//             if (!event.target.matches('#category') && !event.target.matches('#categoryDropdownButton')) {
//                 document.getElementById('categoryList').classList.remove('show');
//             }
//         }
//     }
// });

// Função para selecionar um item nos dropdowns
// function selectDropdown(field, value) {
//     document.getElementById(field).value = value;
//     document.getElementById(field + 'Dropdown').classList.remove('show');
// }

// Função para alternar a lista de categorias
// function toggleCategoryList() {
//     document.getElementById('categoryList').classList.toggle('show');
// }


// Função para selecionar uma categoria
// function selectCategory(category) {
//     document.getElementById('category').value = category;
//     document.getElementById('categoryList').classList.remove('show');
// }

// Função para carregar categorias no dropdown
// function loadCategories() {
//     const categoryList = document.getElementById('categoryList');
//     categoryList.innerHTML = '';

//     categories.forEach(category => {
//         const item = document.createElement('li');
//         item.className = 'category-item';
//         item.textContent = category;
//         item.onclick = function () { selectCategory(category); };
//         categoryList.appendChild(item);
//     });
// }

// Função para carregar categorias existentes no modal
// function loadExistingCategories() {
//     const existingCategories = document.getElementById('existingCategories');
//     existingCategories.innerHTML = '';

//     if (categories.length === 0) {
//         existingCategories.innerHTML = '<div class="text-muted">Nenhuma categoria cadastrada</div>';
//         return;
//     }

//     categories.forEach((category, index) => {
//         const item = document.createElement('div');
//         item.className = 'list-group-item d-flex justify-content-between align-items-center';

//         const categoryName = document.createElement('span');
//         categoryName.textContent = category;

//         const deleteBtn = document.createElement('button');
//         deleteBtn.className = 'btn btn-sm btn-danger';
//         deleteBtn.innerHTML = '<i class="bi bi-trash"></i>';
//         deleteBtn.onclick = function () { deleteCategory(index); };

//         item.appendChild(categoryName);
//         item.appendChild(deleteBtn);
//         existingCategories.appendChild(item);
//     });
// }

// Função para adicionar uma nova categoria
// function addCategory() {
//     const newCategoryInput = document.getElementById('newCategory');
//     const newCategory = newCategoryInput.value.trim();

//     if (newCategory === '') {
//         alert('Por favor, digite o nome da categoria');
//         return;
//     }

//     if (categories.includes(newCategory)) {
//         alert('Esta categoria já existe');
//         return;
//     }

//     categories.push(newCategory);
//     newCategoryInput.value = '';

//     loadCategories();
//     loadExistingCategories();
// }

// Função para deletar uma categoria
// function deleteCategory(index) {
//     if (confirm('Tem certeza que deseja excluir esta categoria?')) {
//         categories.splice(index, 1);
//         loadCategories();
//         loadExistingCategories();

//         // Limpa o campo de categoria se a categoria selecionada foi removida
//         const currentCategory = document.getElementById('category').value;
//         if (!categories.includes(currentCategory)) {
//             document.getElementById('category').value = '';
//         }
//     }
// }

// Função para resetar o formulário
// function resetForm() {
//     document.getElementById('productForm').reset();
// }

// Função para submeter o formulário
// document.getElementById('productForm').addEventListener('submit', function (e) {
//     e.preventDefault();

//     const productName = document.getElementById('productName').value;
//     const quantity = document.getElementById('quantity').value;
//     const unit = document.getElementById('unit').value;
//     const supplier = document.getElementById('supplier').value;
//     const category = document.getElementById('category').value;

//     if (!productName || !quantity || !unit || !supplier || !category) {
//         alert('Por favor, preencha todos os campos obrigatórios');
//         return;
//     }

    // Aqui você faria a submissão para o servidor
    // alert(`Produto cadastrado com sucesso!\n\nNome: ${productName}\nQuantidade: ${quantity}\nUnidade: ${unit}\nFornecedor: ${supplier}\nCategoria: ${category}`);

    // Limpa o formulário após o cadastro
//     resetForm();
// });