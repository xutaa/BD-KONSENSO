-- =============================================
-- Index: IX_Venda_LojaData
-- Descrição: Acelera pesquisas de vendas por loja e data
-- =============================================
CREATE NONCLUSTERED INDEX IX_Venda_LojaData 
ON Venda(Loja_Id, DataHora DESC) 
INCLUDE (ValorTotal);
GO
