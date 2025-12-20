-- =============================================
-- View: vw_VendasMensais
-- Descrição: Agregado de vendas por mês
-- USO: SELECT * FROM vw_VendasMensais ORDER BY Ano DESC, Mes DESC
-- =============================================
CREATE OR ALTER VIEW vw_VendasMensais AS
SELECT 
    YEAR(DataHora) AS Ano,
    MONTH(DataHora) AS Mes,
    DATENAME(MONTH, DataHora) AS NomeMes,
    COUNT(*) AS NumVendas,
    ISNULL(SUM(ValorTotal), 0) AS ReceitaTotal
FROM Venda
GROUP BY YEAR(DataHora), MONTH(DataHora), DATENAME(MONTH, DataHora);
GO
