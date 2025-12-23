-- =============================================
-- Index: IX_Item_Produto
-- Descrição: Acelera pesquisas de itens por produto
-- =============================================
CREATE NONCLUSTERED INDEX IX_Item_Produto 
ON Item(Produto_Referencia) 
INCLUDE (Quantidade, Preco);
GO
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
-- =============================================
-- Index: IX_Stock_Produto
-- Descrição: Acelera pesquisas de stock por produto e armazém
-- =============================================
CREATE NONCLUSTERED INDEX IX_Stock_Produto 
ON Stock(Produto_Referencia, Armazem_Id) 
INCLUDE (Quantidade);
GO
-- =============================================
-- Index: IX_Venda_LojaData
-- Descrição: Acelera pesquisas de vendas por loja e data
-- =============================================
CREATE NONCLUSTERED INDEX IX_Venda_LojaData 
ON Venda(Loja_Id, DataHora DESC) 
INCLUDE (ValorTotal);
GO
