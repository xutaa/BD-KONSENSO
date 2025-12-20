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
