-- =============================================
-- View: vw_StockPorArmazem
-- Descrição: Mostra ocupação de cada armazém
-- USO: SELECT * FROM vw_StockPorArmazem
-- =============================================
CREATE OR ALTER VIEW vw_StockPorArmazem AS
SELECT 
    a.Id AS ArmazemId,
    a.Localizacao,
    a.Capacidade,
    ISNULL(SUM(s.Quantidade), 0) AS StockAtual,
    a.Capacidade - ISNULL(SUM(s.Quantidade), 0) AS EspacoLivre,
    CASE 
        WHEN a.Capacidade = 0 THEN 0
        ELSE CAST(ISNULL(SUM(s.Quantidade), 0) * 100.0 / a.Capacidade AS DECIMAL(5,2))
    END AS PercentagemOcupada
FROM Armazem a
LEFT JOIN Stock s ON a.Id = s.Armazem_Id
GROUP BY a.Id, a.Localizacao, a.Capacidade;
GO
