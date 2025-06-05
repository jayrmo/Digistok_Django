document.addEventListener('DOMContentLoaded', function () {
    const chartDataElement = document.getElementById('chart-data');
    if (!chartDataElement) {
        console.error('Elemento com dados para os gráficos (ID: chart-data) não encontrado.');
        return;
    }

    // 2. Lê e converte os dados JSON passados pelo Django.
    const chartData = JSON.parse(chartDataElement.textContent);

    const digistokPrimary = '#00488b';
    const digistokSecondary = '#d8a602';
    const chartColors = [digistokPrimary, digistokSecondary, '#5cb85c', '#d9534f', '#5bc0de', '#f0ad4e'];

    // --- INICIALIZAÇÃO DOS GRÁFICOS ---

    // Gráfico de Movimentações por Tempo (Linha)
    const ctxMovimentacoes = document.getElementById('movimentacoesPorTempoChart');
    if (ctxMovimentacoes) {
        new Chart(ctxMovimentacoes.getContext('2d'), {
            type: 'line',
            data: {
                labels: chartData.mov_tempo.labels,
                datasets: [{
                    label: 'Entradas',
                    data: chartData.mov_tempo.entradas,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'Saídas',
                    data: chartData.mov_tempo.saidas,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } },
                plugins: { legend: { position: 'top' } }
            }
        });
    }

    // Gráfico de Tipos de Movimentação (Doughnut)
    const ctxTipos = document.getElementById('tiposMovimentacaoChart');
    if (ctxTipos) {
        new Chart(ctxTipos.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: chartData.tipos_mov.labels,
                datasets: [{
                    label: 'Quantidade',
                    data: chartData.tipos_mov.data,
                    backgroundColor: chartColors,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'right' } }
            }
        });
    }

    // Gráfico de Produtos por Categoria (Pizza)
    const ctxCategorias = document.getElementById('produtosPorCategoriaChart');
    if (ctxCategorias) {
        new Chart(ctxCategorias.getContext('2d'), {
            type: 'pie',
            data: {
                labels: chartData.prod_cat.labels,
                datasets: [{
                    label: 'Nº de Produtos',
                    data: chartData.prod_cat.data,
                    backgroundColor: chartColors,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'right' } }
            }
        });
    }

    // Gráfico de Top Fornecedores (Barra Horizontal)
    const ctxFornecedores = document.getElementById('topFornecedoresChart');
    if (ctxFornecedores) {
        new Chart(ctxFornecedores.getContext('2d'), {
            type: 'bar',
            data: {
                labels: chartData.top_fornecedores.labels,
                datasets: [{
                    label: 'Nº de Produtos Cadastrados',
                    data: chartData.top_fornecedores.data,
                    backgroundColor: digistokPrimary,
                    borderColor: '#003a70',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y', // Isso torna o gráfico de barras horizontal
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
});