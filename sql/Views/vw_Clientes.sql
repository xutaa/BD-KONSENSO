-- =============================================
-- View: vw_Clientes
-- Descrição: Junta Cliente + Pessoa
-- =============================================
CREATE OR ALTER VIEW vw_Clientes AS
SELECT 
    c.Pessoa_Cc,
    p.Nome,
    p.Email,
    p.DataNascimento,
    p.NumTelefone,
    c.Nif
FROM Cliente c
JOIN Pessoa p ON c.Pessoa_Cc = p.Cc;
GO
