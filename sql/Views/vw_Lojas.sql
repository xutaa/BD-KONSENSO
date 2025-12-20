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
