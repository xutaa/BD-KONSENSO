-- =============================================
-- View: vw_Clientes
-- Descrição: Junta Cliente + Pessoa
-- =============================================
CREATE OR ALTER VIEW vw_Clientes AS
SELECT 
    c.Pessoa_Cc,
    p.Nome,
    p.Email,
    p.DataNascimento,
    p.NumTelefone,
    c.Nif
FROM Cliente c
JOIN Pessoa p ON c.Pessoa_Cc = p.Cc;
GO
-- =============================================
-- View: vw_ContratosVendedor
-- Descrição: Junta ContratoVendedor + Vendedor + Pessoa + Empresa
-- =============================================
CREATE OR ALTER VIEW vw_ContratosVendedor AS
SELECT 
    cv.Vendedor_Id,
    p.Nome AS Vendedor,
    e.Nome AS Empresa,
    cv.DataIn,
    cv.DataOut
FROM ContratoVendedor cv
JOIN Vendedor v ON cv.Vendedor_Id = v.Id
JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
JOIN Empresa e ON cv.Empresa_Nif = e.Nif;
GO
-- =============================================
-- View: vw_DashboardStats
-- Descrição: Estatísticas gerais para o dashboard
-- USO: SELECT * FROM vw_DashboardStats
-- =============================================
CREATE OR ALTER VIEW vw_DashboardStats AS
SELECT 
    (SELECT COUNT(*) FROM Produto) AS TotalProdutos,
    (SELECT COUNT(*) FROM Cliente) AS TotalClientes,
    (SELECT COUNT(*) FROM Venda) AS TotalVendas,
    (SELECT COUNT(*) FROM Funcionario) AS TotalFuncionarios;
GO
-- =============================================
-- View: vw_Fabricas
-- Descrição: Junta Fabrica + Empresa + Distribuidora
-- =============================================
CREATE OR ALTER VIEW vw_Fabricas AS
SELECT 
    f.Id,
    f.Nome,
    f.Localizacao,
    e.Nome AS Empresa,
    d.Nome AS Distribuidora
FROM Fabrica f
JOIN Empresa e ON f.Empresa_Nif = e.Nif
JOIN Distribuidora d ON f.Distribuidora_Id = d.Id;
GO
-- =============================================
-- View: vw_Fornecedores
-- Descrição: Junta Fornecedor + Empresa
-- =============================================
CREATE OR ALTER VIEW vw_Fornecedores AS
SELECT 
    f.Id,
    f.Nome,
    e.Nome AS Empresa,
    e.Nif
FROM Fornecedor f
JOIN Empresa e ON f.Empresa_Nif = e.Nif;
GO
-- =============================================
-- View: vw_Funcionarios
-- Descrição: Junta Funcionario + Pessoa + Cargo + Empresa + Fabrica
-- =============================================
CREATE OR ALTER VIEW vw_Funcionarios AS
SELECT 
    f.Pessoa_Cc,
    p.Nome,
    c.Nome AS Cargo,
    e.Nome AS Empresa,
    COALESCE(fab.Nome, 'N/A') AS Fabrica
FROM Funcionario f
JOIN Pessoa p ON f.Pessoa_Cc = p.Cc
JOIN Cargo c ON f.Cargo_Id = c.Id
JOIN Empresa e ON f.Empresa_Nif = e.Nif
LEFT JOIN Fabrica fab ON f.Fabrica_Id = fab.Id;
GO
-- =============================================
-- View: vw_Itens
-- Descrição: Junta Item + Produto
-- =============================================
CREATE OR ALTER VIEW vw_Itens AS
SELECT 
    i.Venda_Id,
    p.Nome AS Produto,
    i.Produto_Referencia,
    i.Quantidade,
    i.Preco,
    (i.Quantidade * i.Preco) AS Total
FROM Item i
JOIN Produto p ON i.Produto_Referencia = p.Referencia;
GO
-- =============================================
-- View: vw_Lojas
-- Descrição: Junta Loja + Armazem
-- =============================================
CREATE OR ALTER VIEW vw_Lojas AS
SELECT 
    l.Id,
    l.Nome,
    l.Localizacao,
    a.Localizacao AS Armazem
FROM Loja l
LEFT JOIN Armazem a ON l.Armazem_Id = a.Id;
GO
-- =============================================
-- View: vw_Maquinas
-- Descrição: Junta Maquina + Fabrica
-- =============================================
CREATE OR ALTER VIEW vw_Maquinas AS
SELECT 
    m.Id,
    m.Descricao,
    m.Tipo,
    f.Nome AS Fabrica
FROM Maquina m
JOIN Fabrica f ON m.Fabrica_Id = f.Id;
GO
-- =============================================
-- View: vw_MateriasPrimas
-- Descrição: Junta MateriaPrima + Fornecedor
-- =============================================
CREATE OR ALTER VIEW vw_MateriasPrimas AS
SELECT 
    mp.Referencia,
    mp.Descricao,
    f.Nome AS Fornecedor
FROM MateriaPrima mp
JOIN Fornecedor f ON mp.Fornecedor_Id = f.Id;
GO
-- =============================================
-- View: vw_Stock
-- Descrição: Junta Stock + Produto + Armazem
-- =============================================
CREATE OR ALTER VIEW vw_Stock AS
SELECT 
    s.Produto_Referencia,
    p.Nome AS Produto,
    a.Localizacao AS Armazem,
    s.Quantidade,
    s.UltimoMov,
    s.Armazem_Id
FROM Stock s
JOIN Produto p ON s.Produto_Referencia = p.Referencia
JOIN Armazem a ON s.Armazem_Id = a.Id;
GO
-- =============================================
-- View: vw_StockPorArmazem
-- Descrição: Mostra ocupação de cada armazém
-- USO: SELECT * FROM vw_StockPorArmazem
-- =============================================
CREATE OR ALTER VIEW vw_StockPorArmazem AS
SELECT 
    a.Id AS ArmazemId,
    a.Localizacao,
    a.Capacidade,
    ISNULL(SUM(s.Quantidade), 0) AS StockAtual,
    a.Capacidade - ISNULL(SUM(s.Quantidade), 0) AS EspacoLivre,
    CASE 
        WHEN a.Capacidade = 0 THEN 0
        ELSE CAST(ISNULL(SUM(s.Quantidade), 0) * 100.0 / a.Capacidade AS DECIMAL(5,2))
    END AS PercentagemOcupada
FROM Armazem a
LEFT JOIN Stock s ON a.Id = s.Armazem_Id
GROUP BY a.Id, a.Localizacao, a.Capacidade;
GO
-- =============================================
-- View: vw_VendasMensais
-- Descrição: Agregado de vendas por mês
-- USO: SELECT * FROM vw_VendasMensais ORDER BY Ano DESC, Mes DESC
-- =============================================
CREATE OR ALTER VIEW vw_VendasMensais AS
SELECT 
    YEAR(DataHora) AS Ano,
    MONTH(DataHora) AS Mes,
    DATENAME(MONTH, DataHora) AS NomeMes,
    COUNT(*) AS NumVendas,
    ISNULL(SUM(ValorTotal), 0) AS ReceitaTotal
FROM Venda
GROUP BY YEAR(DataHora), MONTH(DataHora), DATENAME(MONTH, DataHora);
GO
-- =============================================
-- View: VendasPorProduto
-- Descrição: Total de vendas, quantidade e receita por produto
-- USO: SELECT * FROM VendasPorProduto ORDER BY ReceitaTotal DESC
-- =============================================
CREATE OR ALTER VIEW VendasPorProduto AS
SELECT 
    p.Referencia,
    p.Nome,
    p.Descricao,
    COUNT(i.Venda_Id) as TotalVendas,
    SUM(i.Quantidade) as QuantidadeVendida,
    SUM(i.Quantidade * i.Preco) as ReceitaTotal
FROM Produto p
LEFT JOIN Item i ON p.Referencia = i.Produto_Referencia
GROUP BY p.Referencia, p.Nome, p.Descricao;
GO
-- =============================================
-- View: vw_Vendedores
-- Descrição: Junta Vendedor + Pessoa + Cargo
-- =============================================
CREATE OR ALTER VIEW vw_Vendedores AS
SELECT 
    v.Pessoa_Cc,
    p.Nome,
    c.Nome AS Cargo,
    v.NumVendas,
    p.NumTelefone
FROM Vendedor v
JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
JOIN Cargo c ON v.Cargo_Id = c.Id;
GO
