-- ==============================
-- View: vw_VendasPorProduto
-- Descrição: Exibe o total de vendas, quantidade vendida e receita total por produto
-- ==============================
CREATE OR ALTER VIEW VendasPorProduto AS
SELECT 
    p.Referencia,
    p.Nome,
    p.Descricao,
    COUNT(i.Id) as TotalVendas,
    SUM(i.Quantidade) as QuantidadeVendida,
    SUM(i.Quantidade * i.Preco) as ReceitaTotal
FROM Produto p
LEFT JOIN Item i ON p.Referencia = i.Produto_Referencia
GROUP BY p.Referencia, p.Nome, p.Descricao;
GO