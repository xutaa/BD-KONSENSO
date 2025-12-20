-- =============================================
-- TODOS OS INDEXES - BD-KONSENSO
-- Executa este ficheiro no SSMS para criar todos os Indexes
-- =============================================

USE p2g4;
GO

-- =============================================
-- Index 1: IX_Venda_LojaData
-- =============================================
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Venda_LojaData')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Venda_LojaData 
    ON Venda(Loja_Id, DataHora DESC) 
    INCLUDE (ValorTotal);
    PRINT '✅ Index IX_Venda_LojaData criado';
END
GO

-- =============================================
-- Index 2: IX_Item_Produto
-- =============================================
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Item_Produto')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Item_Produto 
    ON Item(Produto_Referencia) 
    INCLUDE (Quantidade, Preco);
    PRINT '✅ Index IX_Item_Produto criado';
END
GO

-- =============================================
-- Index 3: IX_Stock_Produto
-- =============================================
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Stock_Produto')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Stock_Produto 
    ON Stock(Produto_Referencia, Armazem_Id) 
    INCLUDE (Quantidade);
    PRINT '✅ Index IX_Stock_Produto criado';
END
GO

PRINT '';
PRINT '✅ Todos os 3 Indexes verificados/criados com sucesso!';
GO