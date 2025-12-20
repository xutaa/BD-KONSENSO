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
