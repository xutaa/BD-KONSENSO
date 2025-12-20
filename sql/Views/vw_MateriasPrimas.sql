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
