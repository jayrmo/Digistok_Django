#### Atividade ADS WEB-1
# Digistok

Este projeto é uma aplicação web completa para gerenciamento de estoque, projetada para facilitar o controle e a organização de produtos. A plataforma permite aos usuários criar, editar e excluir itens de estoque de forma eficiente, além de oferecer funcionalidades avançadas, como filtragem e ordenação de produtos. O sistema também suporta operações financeiras e fiscais, bem como a manipulação detalhada de estoque, tornando o gerenciamento de inventário mais intuitivo e automatizado.


 ## Funcionalidades
- [x] Cadastro de Produtos
- [x] Autenticação e autorização
- [x] Gerenciamento de Estoque
- [x] Filtro por Categoria, Estoque, etc

## Este projeto é um exemplo simples para demonstrar o uso de:

- MVT(MODEL,VIEW,TEMPLATE)
- Django com PostgreSQL
- Views baseadas em Classes
- Templates com dados dinâmicos
- Upload e exibição de imagens (mídia)
- Organização de templates, estáticos e media
- Authorization e Accounting Django
- CRUD

---
## 🛠 Com o que o app foi construído

O sistema foi desenvolvido com as seguintes tecnologias e ferramentas:

- *Linguagens:* Python, HTML5, CSS3, JavaScript
- *Framework principal:* Django (backend e sistema de templates)
- *Bibliotecas e ferramentas adicionais:*
  - Bootstrap
- *Banco de Dados:* Postrgrees
- *Gerenciamento de arquivos estáticos:* Django Staticfiles
- *Controle de versão:* Git e GitHub


### 📁 Estrutura:

```
digistok/
├── core/
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   └── digistok/
│   │       └── login.html
│   │       └── homepage.html
│   │       └── ...
│   ├── templatetags/
│   │   └── core_tags.py
├── media/
│   └── images/
│   └── digistok/
│       └── produto/
│           └── produto.png...
│   └── digistok/
|
├── static/
│   └── css/
│   └── icon/
│   └── js/
│       └── css/style_adm.css
│       └── css/style_login.css
│       └── css/styles.css
│       └── js/script_adm.js
│       └── js/script_login.js
│       └── js/script.js


```

## 🚀 Como usar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure seu banco PostgreSQL no `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'digistok',
        'USER': 'digistok',
        'PASSWORD': 'digistok',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Execute migrações

```bash
python manage.py migrate
```

### 4. Rode o servidor de desenvolvimento

```bash
python manage.py runserver
```

### 5. Acesse a aplicação

- Visite [http://localhost:8000](http://localhost:8000) para página de login.
- Visite [http://localhost:8000/login](http://localhost:8000/homepage) para página de dashboard.


---





