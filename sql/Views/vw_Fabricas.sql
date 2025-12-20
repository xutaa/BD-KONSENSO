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
