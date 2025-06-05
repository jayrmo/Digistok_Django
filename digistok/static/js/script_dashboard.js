// Função auxiliar para gerar cores aleatórias para os gráficos
function generateRandomColors(numColors) {
    const colors = [];
    for (let i = 0; i < numColors; i++) {
        const hue = Math.floor(Math.random() * 360); // 0-359
        const saturation = 70 + Math.random() * 20; // 70-90%
        const lightness = 60 + Math.random() * 10; // 60-70%
        colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
    }
    return colors;
}

// --- Gráfico de Produtos por Categoria (Pizza) ---
function renderProdutosPorCategoriaChart(data) {
    if (Object.keys(data).length === 0) {
        console.warn("Nenhum dado para o gráfico de Produtos por Categoria.");
        document.getElementById('produtosPorCategoriaChart').style.display = 'none';
        return;
    }

    const ctxPizza = document.getElementById('produtosPorCategoriaChart').getContext('2d');
    const labelsPizza = Object.keys(data);
    const dataPizza = Object.values(data);
    const backgroundColorsPizza = generateRandomColors(labelsPizza.length);

    new Chart(ctxPizza, {
        type: 'pie',
        data: {
            labels: labelsPizza,
            datasets: [{
                data: dataPizza,
                backgroundColor: backgroundColorsPizza,
                hoverOffset: 8,
                borderColor: 'white',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((sum, current) => sum + current, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                label += `${value} produtos (${percentage}%)`;
                            }
                            return label;
                        }
                    }
                }
            }
        }
    })
}

// --- Gráfico de Quantidade por Local de Estoque (Barra) ---
function renderQuantidadePorEstoqueChart(data) {
    if (Object.keys(data).length === 0) {
        // Opcional: mostrar uma mensagem ou esconder o canvas se não houver dados
        console.warn("Nenhum dado para o gráfico de Quantidade por Local de Estoque.");
        document.getElementById('quantidadePorEstoqueChart').style.display = 'none';
        return;
    }

    const ctxBarra = document.getElementById('quantidadePorEstoqueChart').getContext('2d');
    const labelsBarra = Object.keys(data);
    const dataBarra = Object.values(data);
    const backgroundColorsBarra = generateRandomColors(labelsBarra.length);

    new Chart(ctxBarra, {
        type: 'bar',
        data: {
            labels: labelsBarra,
            datasets: [{
                label: 'Quantidade Recebida',
                data: dataBarra,
                backgroundColor: backgroundColorsBarra,
                borderColor: backgroundColorsBarra.map(color => color.replace('60%)', '40%)')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantidade'
                    },
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Local de Estoque'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += `${context.parsed.y} unidades`;
                            }
                            return label;
                        }
                    }
                }
            }
        }
    })

}

document.addEventListener('DOMContentLoaded', function () {
    // Estas variáveis globais são definidas no template HTML
    if (typeof produtosPorCategoriaJson !== 'undefined') {
        const produtosPorCategoriaData = JSON.parse(produtosPorCategoriaJson);
        renderProdutosPorCategoriaChart(produtosPorCategoriaData);
    }

    if (typeof quantidadePorEstoqueJson !== 'undefined') {
        const quantidadePorEstoqueData = JSON.parse(quantidadePorEstoqueJson);
        renderQuantidadePorEstoqueChart(quantidadePorEstoqueData);
    }
});