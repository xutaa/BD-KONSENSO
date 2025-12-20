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
