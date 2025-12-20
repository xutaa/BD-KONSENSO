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
