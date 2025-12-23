-- =============================================
-- Index: IX_Produto_Referencia
-- Descrição: Acelera ordenação e pesquisa de produtos por referência
-- =============================================
USE p2g4;
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Produto_Referencia')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Produto_Referencia 
    ON Produto(Referencia ASC) 
    INCLUDE (Nome, Descricao, Preco, Maquina_Id, Distribuidora_Id);
    PRINT '✅ Index IX_Produto_Referencia criado';
END
GO
