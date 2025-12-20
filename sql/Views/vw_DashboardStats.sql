-- =============================================
-- View: vw_DashboardStats
-- Descrição: Estatísticas gerais para o dashboard
-- USO: SELECT * FROM vw_DashboardStats
-- =============================================
CREATE OR ALTER VIEW vw_DashboardStats AS
SELECT 
    (SELECT COUNT(*) FROM Produto) AS TotalProdutos,
    (SELECT COUNT(*) FROM Cliente) AS TotalClientes,
    (SELECT COUNT(*) FROM Venda) AS TotalVendas,
    (SELECT COUNT(*) FROM Funcionario) AS TotalFuncionarios;
GO
