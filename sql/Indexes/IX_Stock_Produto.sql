-- =============================================
-- Index: IX_Stock_Produto
-- Descrição: Acelera pesquisas de stock por produto e armazém
-- =============================================
CREATE NONCLUSTERED INDEX IX_Stock_Produto 
ON Stock(Produto_Referencia, Armazem_Id) 
INCLUDE (Quantidade);
GO
