-- =============================================
-- View: vw_Funcionarios
-- Descrição: Junta Funcionario + Pessoa + Cargo + Empresa + Fabrica
-- =============================================
CREATE OR ALTER VIEW vw_Funcionarios AS
SELECT 
    f.Pessoa_Cc,
    p.Nome,
    c.Nome AS Cargo,
    e.Nome AS Empresa,
    COALESCE(fab.Nome, 'N/A') AS Fabrica
FROM Funcionario f
JOIN Pessoa p ON f.Pessoa_Cc = p.Cc
JOIN Cargo c ON f.Cargo_Id = c.Id
JOIN Empresa e ON f.Empresa_Nif = e.Nif
LEFT JOIN Fabrica fab ON f.Fabrica_Id = fab.Id;
GO
