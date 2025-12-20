-- =============================================
-- SCRIPT DE TESTE PARA STORED PROCEDURES DE DELETE
-- =============================================
-- Este script cria dados de teste e depois testa todas as SPs de remoção
-- ATENÇÃO: Execute este script numa base de dados de TESTE, não em produção!
-- =============================================

PRINT '========================================';
PRINT 'INÍCIO DOS TESTES DE DELETE';
PRINT '========================================';
PRINT '';

-- =============================================
-- LIMPEZA: REMOVER DADOS DE TESTES ANTERIORES
-- =============================================

PRINT '--- FASE 0: Limpando dados de testes anteriores ---';
PRINT '';

-- Remover na ordem inversa para respeitar dependências
DELETE FROM ContratoVendedor WHERE Vendedor_Id IN (SELECT Id FROM Vendedor WHERE Pessoa_Cc = '99999998');
DELETE FROM Vendedor WHERE Pessoa_Cc = '99999998';
DELETE FROM Cliente WHERE Pessoa_Cc = '99999999';
DELETE FROM Funcionario WHERE Pessoa_Cc = '99999997';
DELETE FROM Pessoa WHERE Cc IN ('99999999', '99999998', '99999997');
DELETE FROM Stock WHERE Produto_Referencia = 'PROD-TEST-DEL';
DELETE FROM MateriaPrima WHERE Referencia = 'MP-TEST-DEL';
DELETE FROM Produto WHERE Referencia = 'PROD-TEST-DEL';
DELETE FROM Fornecedor WHERE Nome = 'Fornecedor Teste Delete';
DELETE FROM Maquina WHERE Descricao = 'Máquina Teste Delete';
DELETE FROM Loja WHERE Nome = 'Loja Teste Delete';
DELETE FROM Fabrica WHERE Nome = 'Fábrica Teste Delete';
DELETE FROM Distribuidora WHERE Nome = 'Distribuidora Teste Delete';
DELETE FROM Armazem WHERE Localizacao = 'Armazém Teste Delete';
DELETE FROM Cargo WHERE Nome = 'Cargo Teste Delete';
DELETE FROM Empresa WHERE Nif = '999999999';

PRINT '✅ Dados antigos limpos';
PRINT '';

-- =============================================
-- PREPARAÇÃO: CRIAR DADOS DE TESTE
-- =============================================

PRINT '--- FASE 1: Criando dados de teste ---';
PRINT '';

-- 1. Criar Empresa de teste
DECLARE @EmpresaTeste NVARCHAR(9) = '999999999';
INSERT INTO Empresa (Nif, Nome, Localizacao, NumTelefone, Email)
VALUES (@EmpresaTeste, 'Empresa Teste Delete', 'Lisboa', '999999999', 'teste@delete.com');
PRINT '✅ Empresa de teste criada (NIF: 999999999)';

-- 2. Criar Cargo de teste
DECLARE @CargoTesteId INT;
INSERT INTO Cargo (Nome, Descricao)
VALUES ('Cargo Teste Delete', 'Cargo temporário para testes');
SET @CargoTesteId = SCOPE_IDENTITY();
PRINT '✅ Cargo de teste criado (ID: ' + CAST(@CargoTesteId AS VARCHAR) + ')';

-- 3. Criar Armazém de teste
DECLARE @ArmazemTesteId INT;
INSERT INTO Armazem (Localizacao, Capacidade)
VALUES ('Armazém Teste Delete', 1000);
SET @ArmazemTesteId = SCOPE_IDENTITY();
PRINT '✅ Armazém de teste criado (ID: ' + CAST(@ArmazemTesteId AS VARCHAR) + ')';

-- 4. Criar Distribuidora de teste
DECLARE @DistribuidoraTesteId INT;
INSERT INTO Distribuidora (Nome, Localizacao)
VALUES ('Distribuidora Teste Delete', 'Porto');
SET @DistribuidoraTesteId = SCOPE_IDENTITY();
PRINT '✅ Distribuidora de teste criada (ID: ' + CAST(@DistribuidoraTesteId AS VARCHAR) + ')';

-- 5. Criar Fábrica de teste
DECLARE @FabricaTesteId INT;
INSERT INTO Fabrica (Nome, Localizacao, Empresa_Nif, Distribuidora_Id)
VALUES ('Fábrica Teste Delete', 'Braga', @EmpresaTeste, @DistribuidoraTesteId);
SET @FabricaTesteId = SCOPE_IDENTITY();
PRINT '✅ Fábrica de teste criada (ID: ' + CAST(@FabricaTesteId AS VARCHAR) + ')';

-- 6. Criar Loja de teste
DECLARE @LojaTesteId INT;
INSERT INTO Loja (Nome, Localizacao, Armazem_Id)
VALUES ('Loja Teste Delete', 'Coimbra', @ArmazemTesteId);
SET @LojaTesteId = SCOPE_IDENTITY();
PRINT '✅ Loja de teste criada (ID: ' + CAST(@LojaTesteId AS VARCHAR) + ')';

-- 7. Criar Máquina de teste
DECLARE @MaquinaTesteId INT;
INSERT INTO Maquina (Descricao, Tipo, Fabrica_Id)
VALUES ('Máquina Teste Delete', 'Teste', @FabricaTesteId);
SET @MaquinaTesteId = SCOPE_IDENTITY();
PRINT '✅ Máquina de teste criada (ID: ' + CAST(@MaquinaTesteId AS VARCHAR) + ')';

-- 8. Criar Fornecedor de teste
DECLARE @FornecedorTesteId INT;
INSERT INTO Fornecedor (Nome, Empresa_Nif)
VALUES ('Fornecedor Teste Delete', @EmpresaTeste);
SET @FornecedorTesteId = SCOPE_IDENTITY();
PRINT '✅ Fornecedor de teste criado (ID: ' + CAST(@FornecedorTesteId AS VARCHAR) + ')';

-- 9. Criar Matéria-Prima de teste
DECLARE @MateriaPrimaTesteRef NVARCHAR(50) = 'MP-TEST-DEL';
INSERT INTO MateriaPrima (Referencia, Descricao, Fornecedor_Id)
VALUES (@MateriaPrimaTesteRef, 'Matéria-Prima Teste Delete', @FornecedorTesteId);
PRINT '✅ Matéria-Prima de teste criada (Ref: MP-TEST-DEL)';

-- 10. Criar Produto de teste
DECLARE @ProdutoTesteRef NVARCHAR(50) = 'PROD-TEST-DEL';
INSERT INTO Produto (Referencia, Nome, Descricao, Preco, Maquina_Id, Distribuidora_Id)
VALUES (@ProdutoTesteRef, 'Produto Teste Delete', 'Produto temporário', 99.99, @MaquinaTesteId, @DistribuidoraTesteId);
PRINT '✅ Produto de teste criado (Ref: PROD-TEST-DEL)';

-- 11. Criar Stock de teste
INSERT INTO Stock (Produto_Referencia, Armazem_Id, Quantidade, UltimoMov)
VALUES (@ProdutoTesteRef, @ArmazemTesteId, 50, GETDATE());
PRINT '✅ Stock de teste criado';

-- 12. Criar Cliente de teste
DECLARE @ClienteTesteCC NVARCHAR(8) = '99999999';
INSERT INTO Pessoa (Cc, Nome, Email, DataNascimento, Morada, NumTelefone)
VALUES (@ClienteTesteCC, 'Cliente Teste Delete', 'cliente@teste.com', '1990-01-01', 'Rua Teste', '999999999');
INSERT INTO Cliente (Pessoa_Cc, Nif)
VALUES (@ClienteTesteCC, '999999991');
PRINT '✅ Cliente de teste criado (CC: 99999999)';

-- 13. Criar Vendedor de teste (COM NumVendas)
DECLARE @VendedorTesteCC NVARCHAR(8) = '99999998';
DECLARE @VendedorTesteId INT;
INSERT INTO Pessoa (Cc, Nome, Email, DataNascimento, Morada, NumTelefone)
VALUES (@VendedorTesteCC, 'Vendedor Teste Delete', 'vendedor@teste.com', '1985-05-05', 'Rua Vendedor', '988888888');
INSERT INTO Vendedor (Pessoa_Cc, Cargo_Id, NumVendas)
VALUES (@VendedorTesteCC, @CargoTesteId, 0);
SET @VendedorTesteId = SCOPE_IDENTITY();
PRINT '✅ Vendedor de teste criado (ID: ' + CAST(@VendedorTesteId AS VARCHAR) + ', CC: 99999998)';

-- 14. Criar Contrato Vendedor de teste
INSERT INTO ContratoVendedor (Vendedor_Id, Empresa_Nif, DataIn)
VALUES (@VendedorTesteId, @EmpresaTeste, GETDATE());
PRINT '✅ Contrato Vendedor de teste criado';

-- 15. Criar Funcionário de teste
DECLARE @FuncionarioTesteCC NVARCHAR(8) = '99999997';
INSERT INTO Pessoa (Cc, Nome, Email, DataNascimento, Morada, NumTelefone)
VALUES (@FuncionarioTesteCC, 'Funcionário Teste Delete', 'func@teste.com', '1992-03-15', 'Rua Func', '977777777');
INSERT INTO Funcionario (Pessoa_Cc, Cargo_Id, Empresa_Nif, Fabrica_Id)
VALUES (@FuncionarioTesteCC, @CargoTesteId, @EmpresaTeste, @FabricaTesteId);
PRINT '✅ Funcionário de teste criado (CC: 99999997)';

PRINT '';
PRINT '========================================';
PRINT 'DADOS DE TESTE CRIADOS COM SUCESSO!';
PRINT '========================================';
PRINT '';
WAITFOR DELAY '00:00:02'; -- Pausa de 2 segundos

-- =============================================
-- TESTES DE DELETE
-- =============================================

PRINT '--- FASE 2: Testando Stored Procedures de DELETE ---';
PRINT '';

-- TESTE 1: RemoverStock (CORRIGIDO: @ProdutoReferencia e @ArmazemId)
PRINT '📝 Teste 1: SP_RemoverStock';
BEGIN TRY
    EXEC dbo.RemoverStock @ProdutoReferencia = @ProdutoTesteRef, @ArmazemId = @ArmazemTesteId;
    PRINT '✅ RemoverStock executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 2: RemoverMateriaPrima
PRINT '📝 Teste 2: SP_RemoverMateriaPrima';
BEGIN TRY
    EXEC dbo.RemoverMateriaPrima @Referencia = @MateriaPrimaTesteRef;
    PRINT '✅ RemoverMateriaPrima executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 3: RemoverProduto
PRINT '📝 Teste 3: SP_RemoverProduto';
BEGIN TRY
    EXEC dbo.RemoverProduto @Referencia = @ProdutoTesteRef;
    PRINT '✅ RemoverProduto executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 4: RemoverContratoVendedor (CORRIGIDO: @VendedorId e @EmpresaNif)
PRINT '📝 Teste 4: SP_RemoverContratoVendedor';
BEGIN TRY
    EXEC dbo.RemoverContratoVendedor @VendedorId = @VendedorTesteId, @EmpresaNif = @EmpresaTeste;
    PRINT '✅ RemoverContratoVendedor executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 5: RemoverVendedor (CORRIGIDO: @Cc)
PRINT '📝 Teste 5: SP_RemoverVendedor';
BEGIN TRY
    EXEC dbo.RemoverVendedor @Cc = @VendedorTesteCC;
    PRINT '✅ RemoverVendedor executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 6: RemoverCliente (CORRIGIDO: @Cc)
PRINT '📝 Teste 6: SP_RemoverCliente';
BEGIN TRY
    EXEC dbo.RemoverCliente @Cc = @ClienteTesteCC;
    PRINT '✅ RemoverCliente executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 7: RemoverFuncionario (CORRIGIDO: @Cc)
PRINT '📝 Teste 7: SP_RemoverFuncionario';
BEGIN TRY
    EXEC dbo.RemoverFuncionario @Cc = @FuncionarioTesteCC;
    PRINT '✅ RemoverFuncionario executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 8: RemoverFornecedor
PRINT '📝 Teste 8: SP_RemoverFornecedor';
BEGIN TRY
    EXEC dbo.RemoverFornecedor @Id = @FornecedorTesteId;
    PRINT '✅ RemoverFornecedor executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 9: RemoverMaquina
PRINT '📝 Teste 9: SP_RemoverMaquina';
BEGIN TRY
    EXEC dbo.RemoverMaquina @Id = @MaquinaTesteId;
    PRINT '✅ RemoverMaquina executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 10: RemoverLoja
PRINT '📝 Teste 10: SP_RemoverLoja';
BEGIN TRY
    EXEC dbo.RemoverLoja @Id = @LojaTesteId;
    PRINT '✅ RemoverLoja executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 11: RemoverFabrica
PRINT '📝 Teste 11: SP_RemoverFabrica';
BEGIN TRY
    EXEC dbo.RemoverFabrica @Id = @FabricaTesteId;
    PRINT '✅ RemoverFabrica executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 12: RemoverDistribuidora
PRINT '📝 Teste 12: SP_RemoverDistribuidora';
BEGIN TRY
    EXEC dbo.RemoverDistribuidora @Id = @DistribuidoraTesteId;
    PRINT '✅ RemoverDistribuidora executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 13: RemoverArmazem
PRINT '📝 Teste 13: SP_RemoverArmazem';
BEGIN TRY
    EXEC dbo.RemoverArmazem @Id = @ArmazemTesteId;
    PRINT '✅ RemoverArmazem executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 14: RemoverCargo
PRINT '📝 Teste 14: SP_RemoverCargo';
BEGIN TRY
    EXEC dbo.RemoverCargo @Id = @CargoTesteId;
    PRINT '✅ RemoverCargo executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE 15: RemoverEmpresa
PRINT '📝 Teste 15: SP_RemoverEmpresa';
BEGIN TRY
    EXEC dbo.RemoverEmpresa @Nif = @EmpresaTeste;
    PRINT '✅ RemoverEmpresa executado com sucesso';
END TRY
BEGIN CATCH
    PRINT '❌ Erro: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- =============================================
-- TESTES DE VALIDAÇÃO (Tentativas que DEVEM FALHAR)
-- =============================================

PRINT '';
PRINT '========================================';
PRINT 'FASE 3: Testes de Validação (Devem Falhar)';
PRINT '========================================';
PRINT '';

-- TESTE V1: Tentar remover registro inexistente
PRINT '📝 Teste V1: Remover Produto Inexistente (DEVE FALHAR)';
BEGIN TRY
    EXEC dbo.RemoverProduto @Referencia = 'PROD-NAO-EXISTE';
    PRINT '❌ ERRO: Deveria ter falhado mas não falhou!';
END TRY
BEGIN CATCH
    PRINT '✅ Falhou conforme esperado: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE V2: Tentar remover Cliente Inexistente
PRINT '📝 Teste V2: Remover Cliente Inexistente (DEVE FALHAR)';
BEGIN TRY
    EXEC dbo.RemoverCliente @Cc = '00000000';
    PRINT '❌ ERRO: Deveria ter falhado mas não falhou!';
END TRY
BEGIN CATCH
    PRINT '✅ Falhou conforme esperado: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- TESTE V3: Tentar remover Empresa Inexistente
PRINT '📝 Teste V3: Remover Empresa Inexistente (DEVE FALHAR)';
BEGIN TRY
    EXEC dbo.RemoverEmpresa @Nif = '000000000';
    PRINT '❌ ERRO: Deveria ter falhado mas não falhou!';
END TRY
BEGIN CATCH
    PRINT '✅ Falhou conforme esperado: ' + ERROR_MESSAGE();
END CATCH
PRINT '';

-- =============================================
-- VERIFICAÇÃO FINAL
-- =============================================

PRINT '';
PRINT '========================================';
PRINT 'VERIFICAÇÃO FINAL';
PRINT '========================================';
PRINT '';

-- Verificar se os dados de teste foram realmente removidos
PRINT 'Verificando se os dados foram removidos...';
PRINT '';

IF NOT EXISTS (SELECT 1 FROM Stock WHERE Produto_Referencia = @ProdutoTesteRef)
    PRINT '✅ Stock removido com sucesso';
ELSE
    PRINT '❌ Stock ainda existe!';

IF NOT EXISTS (SELECT 1 FROM MateriaPrima WHERE Referencia = @MateriaPrimaTesteRef)
    PRINT '✅ Matéria-Prima removida com sucesso';
ELSE
    PRINT '❌ Matéria-Prima ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Produto WHERE Referencia = @ProdutoTesteRef)
    PRINT '✅ Produto removido com sucesso';
ELSE
    PRINT '❌ Produto ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Cliente WHERE Pessoa_Cc = @ClienteTesteCC)
    PRINT '✅ Cliente removido com sucesso';
ELSE
    PRINT '❌ Cliente ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Vendedor WHERE Pessoa_Cc = @VendedorTesteCC)
    PRINT '✅ Vendedor removido com sucesso';
ELSE
    PRINT '❌ Vendedor ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Funcionario WHERE Pessoa_Cc = @FuncionarioTesteCC)
    PRINT '✅ Funcionário removido com sucesso';
ELSE
    PRINT '❌ Funcionário ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Fornecedor WHERE Id = @FornecedorTesteId)
    PRINT '✅ Fornecedor removido com sucesso';
ELSE
    PRINT '❌ Fornecedor ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Maquina WHERE Id = @MaquinaTesteId)
    PRINT '✅ Máquina removida com sucesso';
ELSE
    PRINT '❌ Máquina ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Loja WHERE Id = @LojaTesteId)
    PRINT '✅ Loja removida com sucesso';
ELSE
    PRINT '❌ Loja ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Fabrica WHERE Id = @FabricaTesteId)
    PRINT '✅ Fábrica removida com sucesso';
ELSE
    PRINT '❌ Fábrica ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Distribuidora WHERE Id = @DistribuidoraTesteId)
    PRINT '✅ Distribuidora removida com sucesso';
ELSE
    PRINT '❌ Distribuidora ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Armazem WHERE Id = @ArmazemTesteId)
    PRINT '✅ Armazém removido com sucesso';
ELSE
    PRINT '❌ Armazém ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Cargo WHERE Id = @CargoTesteId)
    PRINT '✅ Cargo removido com sucesso';
ELSE
    PRINT '❌ Cargo ainda existe!';

IF NOT EXISTS (SELECT 1 FROM Empresa WHERE Nif = @EmpresaTeste)
    PRINT '✅ Empresa removida com sucesso';
ELSE
    PRINT '❌ Empresa ainda existe!';

PRINT '';
PRINT '========================================';
PRINT 'TESTES CONCLUÍDOS!';
PRINT '========================================';
PRINT '';
PRINT 'Todas as Stored Procedures de DELETE foram testadas.';
PRINT 'Reveja os resultados acima para verificar se tudo funcionou corretamente.';
PRINT '';

GO
