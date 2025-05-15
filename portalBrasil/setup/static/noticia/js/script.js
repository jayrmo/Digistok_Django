document.addEventListener('DOMContentLoaded', function() {
    iniciarCarrossel();
    iniciarAbas();
    iniciarBotoesLeiaMais();
});


//Controla a alternância automática dos slides e os controles de navegação

function iniciarCarrossel() {
    const slides = document.querySelectorAll('.carrossel-slide');
    const indicadores = document.querySelectorAll('.indicador');
    const btnAnterior = document.getElementById('anterior');
    const btnProximo = document.getElementById('proximo');
    let slideAtual = 0;
    let intervaloSlide;
    
    function mostrarSlide(indice) {
        // Remove a classe ativo de todos os slides e indicadores
        slides.forEach(slide => slide.classList.remove('ativo'));
        indicadores.forEach(indicador => indicador.classList.remove('ativo'));
        
        // Adiciona a classe ativo ao slide atual e seu indicador
        slides[indice].classList.add('ativo');
        indicadores[indice].classList.add('ativo');
        
        // Atualiza o índice do slide atual
        slideAtual = indice;
    }
    
    function proximoSlide() {
        const novoIndice = (slideAtual + 1) % slides.length;
        mostrarSlide(novoIndice);
    }

    function slideAnterior() {
        const novoIndice = (slideAtual - 1 + slides.length) % slides.length;
        mostrarSlide(novoIndice);
    }
    
    function iniciarIntervalo() {
        intervaloSlide = setInterval(proximoSlide, 5000);
    }
    
    // Reinicia o intervalo quando houver interação manual
    function reiniciarIntervalo() {
        clearInterval(intervaloSlide);
        iniciarIntervalo();
    }
    
    btnAnterior.addEventListener('click', () => {
        slideAnterior();
        reiniciarIntervalo();
    });
    
    btnProximo.addEventListener('click', () => {
        proximoSlide();
        reiniciarIntervalo();
    });
    
    indicadores.forEach((indicador, indice) => {
        indicador.addEventListener('click', () => {
            mostrarSlide(indice);
            reiniciarIntervalo();
        });
    });
    
    // Inicia o carrossel
    mostrarSlide(0);
    iniciarIntervalo();
    
}


// Controla a exibição do conteúdo correspondente à aba selecionada
function iniciarAbas() {
    const botoesAba = document.querySelectorAll('.botao-aba');
    const paineis = document.querySelectorAll('.painel-aba');
    
    botoesAba.forEach(botao => {
        botao.addEventListener('click', () => {
            // Remove a classe ativo de todos os botões e painéis
            botoesAba.forEach(b => b.classList.remove('ativo'));
            paineis.forEach(p => p.classList.remove('ativo'));
            
            // Adiciona a classe ativo ao botão clicado
            botao.classList.add('ativo');
            
            // Identifica e ativa o painel correspondente
            const abaId = botao.getAttribute('data-aba');
            document.getElementById(abaId).classList.add('ativo');
        });
    });
}

/**
 * Função para inicializar os botões de "Leia mais"
 * Controla a exibição do conteúdo completo das notícias
 */
function iniciarBotoesLeiaMais() {
    const botoesLeiaMais = document.querySelectorAll('.btn-leia-mais');
    
    botoesLeiaMais.forEach(botao => {
        botao.addEventListener('click', function() {
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
    
    // Inicializa os botões de "Leia mais" do carrossel
    const botoesDestaque = document.querySelectorAll('.btn-destaque');
    
    botoesDestaque.forEach(botao => {
        botao.addEventListener('click', function() {
            alert('Não implementado ainda!');
        });
    });
}