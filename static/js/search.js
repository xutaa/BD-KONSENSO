/**
 * Função genérica para filtrar tabelas
 * @param {string} inputId - ID do input de pesquisa
 * @param {string} tableId - ID da tabela
 * @param {string} counterId - ID do elemento contador
 * @param {string} noResultId - ID do alerta de "nenhum resultado"
 */
function filtrarTabela(inputId, tableId, counterId, noResultId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');
    const clearBtn = document.getElementById('clearBtn');
    let visibleCount = 0;

    // Mostrar/esconder botão limpar
    if (clearBtn) {
        clearBtn.style.display = filter ? 'block' : 'none';
    }

    // Percorrer todas as linhas da tabela (exceto cabeçalho)
    for (let i = 1; i < tr.length; i++) {
        const td = tr[i].getElementsByTagName('td');
        let found = false;

        // Verificar se alguma coluna contém o texto pesquisado
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }

        // Mostrar/esconder linha
        if (found) {
            tr[i].style.display = "";
            visibleCount++;
        } else {
            tr[i].style.display = "none";
        }
    }

    // Atualizar contador
    if (counterId) {
        const counter = document.getElementById(counterId);
        if (counter) {
            counter.textContent = visibleCount;
        }
    }

    // Mostrar mensagem se não houver resultados
    if (noResultId) {
        const nenhumResultado = document.getElementById(noResultId);
        if (nenhumResultado) {
            if (visibleCount === 0 && filter !== '') {
                nenhumResultado.style.display = 'block';
            } else {
                nenhumResultado.style.display = 'none';
            }
        }
    }
}

/**
 * Limpar pesquisa
 * @param {string} inputId - ID do input de pesquisa
 */
function limparPesquisa(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.value = '';
        input.dispatchEvent(new Event('keyup'));
        input.focus();
    }
}

/**
 * Configurar atalhos de teclado
 * @param {string} inputId - ID do input de pesquisa
 */
function configurarAtalhos(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        // ESC para limpar
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                limparPesquisa(inputId);
            }
        });

        // Focar automaticamente ao carregar
        window.addEventListener('load', function() {
            input.focus();
        });
    }
}