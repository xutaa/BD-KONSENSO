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
