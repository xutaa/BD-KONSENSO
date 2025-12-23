-- =============================================
-- Index: IX_Produto_Nome
-- Descrição: Acelera ordenação de produtos por nome
-- =============================================
USE p2g4;
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Produto_Nome')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Produto_Nome 
    ON Produto(Nome ASC) 
    INCLUDE (Referencia, Descricao, Preco, Maquina_Id, Distribuidora_Id);
    PRINT '✅ Index IX_Produto_Nome criado';
END
GO
