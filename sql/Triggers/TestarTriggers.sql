-- =============================================
-- SCRIPT DE TESTE PARA TRIGGERS
-- BD-KONSENSO
-- Data: 20/12/2025
-- =============================================

-- PASSO 1: PRIMEIRO EXECUTE OS TRIGGERS (TodosTriggers.sql)
-- Depois execute este script para testar

USE p2g4;
GO

-- =============================================
-- VERIFICAR SE OS TRIGGERS EXISTEM
-- =============================================
PRINT '=== VERIFICANDO TRIGGERS EXISTENTES ===';

SELECT 
    name AS NomeTrigger,
    OBJECT_NAME(parent_id) AS TabelaAssociada,
    create_date AS DataCriacao,
    is_disabled AS Desativado
FROM sys.triggers
WHERE OBJECT_NAME(parent_id) IN ('Stock', 'Item', 'Cliente', 'Venda')
ORDER BY name;
GO

-- =============================================
-- TESTE 1: TR_ValidarCapacidadeArmazem
-- Deve FALHAR se tentarmos exceder a capacidade
-- =============================================
PRINT '';
PRINT '=== TESTE 1: Validar Capacidade Armazém ===';

-- Primeiro, ver a capacidade de um armazém
SELECT TOP 1 
    Id, 
    Localizacao, 
    Capacidade,
    (SELECT ISNULL(SUM(Quantidade), 0) FROM Stock WHERE Armazem_Id = Armazem.Id) AS StockAtual
FROM Armazem;

-- Ver um produto existente
DECLARE @ProdutoRef VARCHAR(20);
DECLARE @ArmazemId INT;
DECLARE @CapacidadeArmazem INT;

SELECT TOP 1 @ProdutoRef = Referencia FROM Produto;
SELECT TOP 1 @ArmazemId = Id, @CapacidadeArmazem = Capacidade FROM Armazem;

PRINT 'Produto para teste: ' + ISNULL(@ProdutoRef, 'N/A');
PRINT 'Armazém para teste: ' + CAST(@ArmazemId AS VARCHAR);
PRINT 'Capacidade: ' + CAST(@CapacidadeArmazem AS VARCHAR);

-- TESTE: Tentar adicionar stock que excede a capacidade
-- (Este INSERT deve FALHAR se o trigger funcionar corretamente)
BEGIN TRY
    BEGIN TRANSACTION;
    
    PRINT 'Tentando inserir stock que excede capacidade...';
    
    -- Tentar inserir quantidade enorme (deve falhar)
    INSERT INTO Stock (Produto_Referencia, Armazem_Id, Quantidade, UltimoMov)
    VALUES (@ProdutoRef, @ArmazemId, 999999999, GETDATE());
    
    PRINT '❌ FALHA: O trigger NÃO bloqueou a operação!';
    ROLLBACK TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    PRINT '✅ SUCESSO: Trigger bloqueou - ' + ERROR_MESSAGE();
END CATCH
GO

-- =============================================
-- TESTE 2: TR_BloquearExclusaoClienteComVendas
-- Deve FALHAR ao tentar eliminar cliente com vendas
-- =============================================
PRINT '';
PRINT '=== TESTE 2: Bloquear Exclusão Cliente com Vendas ===';

-- Encontrar um cliente que tenha vendas
DECLARE @ClienteNif VARCHAR(20);
DECLARE @ClienteCc VARCHAR(20);

SELECT TOP 1 
    @ClienteNif = c.Nif,
    @ClienteCc = c.Pessoa_Cc
FROM Cliente c
INNER JOIN Venda v ON c.Nif = v.Cliente_Nif;

IF @ClienteNif IS NOT NULL
BEGIN
    PRINT 'Cliente com vendas encontrado: NIF = ' + @ClienteNif;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        PRINT 'Tentando eliminar cliente com histórico de vendas...';
        DELETE FROM Cliente WHERE Nif = @ClienteNif;
        
        PRINT '❌ FALHA: O trigger NÃO bloqueou a eliminação!';
        ROLLBACK TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        PRINT '✅ SUCESSO: Trigger bloqueou - ' + ERROR_MESSAGE();
    END CATCH
END
ELSE
BEGIN
    PRINT '⚠️ Nenhum cliente com vendas encontrado para testar.';
    PRINT 'Criando dados de teste...';
    
    -- Se não há cliente com vendas, podemos testar com cliente SEM vendas (deve permitir eliminar)
    SELECT TOP 1 
        @ClienteNif = c.Nif,
        @ClienteCc = c.Pessoa_Cc
    FROM Cliente c
    WHERE c.Nif NOT IN (SELECT DISTINCT Cliente_Nif FROM Venda WHERE Cliente_Nif IS NOT NULL);
    
    IF @ClienteNif IS NOT NULL
    BEGIN
        PRINT 'Cliente SEM vendas encontrado: NIF = ' + @ClienteNif;
        PRINT 'Este cliente PODE ser eliminado (trigger só bloqueia se tiver vendas).';
    END
END
GO

-- =============================================
-- TESTE 3: AtualizarTotalVenda (já existente)
-- Verifica se o total da venda é atualizado automaticamente
-- =============================================
PRINT '';
PRINT '=== TESTE 3: Atualizar Total Venda ===';

-- Ver uma venda e comparar o total calculado
SELECT TOP 5
    v.Id AS VendaId,
    v.ValorTotal AS TotalRegistado,
    (SELECT SUM(i.Quantidade * i.Preco) FROM Item i WHERE i.Venda_Id = v.Id) AS TotalCalculado,
    CASE 
        WHEN v.ValorTotal = (SELECT SUM(i.Quantidade * i.Preco) FROM Item i WHERE i.Venda_Id = v.Id)
        THEN '✅ OK'
        ELSE '❌ DIVERGÊNCIA'
    END AS Status
FROM Venda v
ORDER BY v.Id DESC;
GO

-- =============================================
-- TESTE 4: GarantirStockPositivo
-- Deve falhar se stock ficar negativo
-- =============================================
PRINT '';
PRINT '=== TESTE 4: Garantir Stock Positivo ===';

DECLARE @StockProduto VARCHAR(20);
DECLARE @StockArmazem INT;

SELECT TOP 1 
    @StockProduto = Produto_Referencia,
    @StockArmazem = Armazem_Id
FROM Stock
WHERE Quantidade > 0;

IF @StockProduto IS NOT NULL
BEGIN
    PRINT 'Stock encontrado para teste: Produto = ' + @StockProduto;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        PRINT 'Tentando colocar stock negativo...';
        UPDATE Stock SET Quantidade = -100 
        WHERE Produto_Referencia = @StockProduto AND Armazem_Id = @StockArmazem;
        
        PRINT '❌ FALHA: O trigger NÃO bloqueou stock negativo!';
        ROLLBACK TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        PRINT '✅ SUCESSO: Trigger bloqueou - ' + ERROR_MESSAGE();
    END CATCH
END
ELSE
BEGIN
    PRINT '⚠️ Nenhum registo de stock encontrado para testar.';
END
GO

-- =============================================
-- RESUMO FINAL
-- =============================================
PRINT '';
PRINT '=== RESUMO DOS TRIGGERS ===';

SELECT 
    t.name AS Trigger,
    OBJECT_NAME(t.parent_id) AS Tabela,
    CASE WHEN t.is_disabled = 0 THEN '✅ Ativo' ELSE '❌ Desativado' END AS Estado,
    te.type_desc AS Tipo
FROM sys.triggers t
INNER JOIN sys.trigger_events te ON t.object_id = te.object_id
WHERE OBJECT_NAME(t.parent_id) IN ('Stock', 'Item', 'Cliente', 'Venda')
ORDER BY t.name;
GO

PRINT '';
PRINT '=== TESTES CONCLUÍDOS ===';
PRINT 'Verifica os resultados acima para confirmar se os triggers funcionam.';
GO
