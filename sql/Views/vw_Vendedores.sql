-- =============================================
-- View: vw_Vendedores
-- Descrição: Junta Vendedor + Pessoa + Cargo
-- =============================================
CREATE OR ALTER VIEW vw_Vendedores AS
SELECT 
    v.Pessoa_Cc,
    p.Nome,
    c.Nome AS Cargo,
    v.NumVendas,
    p.NumTelefone
FROM Vendedor v
JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
JOIN Cargo c ON v.Cargo_Id = c.Id;
GO
