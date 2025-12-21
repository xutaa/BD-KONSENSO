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
