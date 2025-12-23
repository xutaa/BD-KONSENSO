-- =============================================
-- Index: IX_Produto_Preco
-- Descrição: Acelera ordenação de produtos por preço
-- =============================================
USE p2g4;
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Produto_Preco')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Produto_Preco 
    ON Produto(Preco ASC) 
    INCLUDE (Nome, Referencia, Descricao, Maquina_Id, Distribuidora_Id);
    PRINT '✅ Index IX_Produto_Preco criado';
END
GO
