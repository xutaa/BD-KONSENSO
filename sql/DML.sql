INSERT INTO Pessoa (Cc, Nome, Email, DataNascimento, Morada, NumTelefone) VALUES
('10111213', 'André Faria', 'andre.faria@email.pt', '1990-05-15', 'Rua dos Mercados, 1', '911000001'),
('14151617', 'Beatriz Gomes', 'beatriz.gomes@email.pt', '1985-11-20', 'Av. da Liberdade, 55', '921000002'),
('18192021', 'Carlos Pinto', 'carlos.pinto@email.pt', '1995-03-01', 'Largo Central, 10', '931000003'),
('22232425', 'Daniela Sousa', 'daniela.sousa@email.pt', '1988-08-10', 'Rua Nova, 3', '961000004'),
('26272829', 'Eduardo Neves', 'eduardo.neves@email.pt', '2000-01-25', 'Praça da Alegria, 7', '911000005'),
('30313233', 'Filipa Ramos', 'filipa.ramos@email.pt', '1976-06-03', 'Travessa da Sé, 12', '921000006'),
('34353637', 'Guilherme Lima', 'guilherme.lima@email.pt', '1992-04-18', 'Rua do Ouro, 22', '931000007'),
('38394041', 'Helena Dias', 'helena.dias@email.pt', '1980-12-05', 'Avenida Mar, 45', '961000008'),
('42434445', 'Ivo Ferreira', 'ivo.ferreira@email.pt', '1998-07-30', 'Rua da Praia, 8', '911000009'),
('46474849', 'Joana Lourenço', 'joana.lourenco@email.pt', '1970-02-14', 'Beco dos Anjos, 15', '921000010'),
('50515253', 'Nuno Teixeira', 'nuno.teixeira@email.pt', '1993-09-28', 'Rua da Paz, 33', '931000011'),
('54555657', 'Olívia Martins', 'olivia.martins@email.pt', '1987-03-17', 'Av. dos Descobrimentos, 100', '961000012'),
('58596061', 'Pedro Ribeiro', 'pedro.ribeiro@email.pt', '1999-11-11', 'Estrada Nacional, 20', '911000013'),
('62636465', 'Quitéria Gomes', 'quiteria.gomes@email.pt', '1982-01-08', 'Rua do Castelo, 5', '921000014'),
('66676869', 'Ricardo Mota', 'ricardo.mota@email.pt', '1975-06-23', 'Praça da República, 1', '931000015'),
('70717273', 'Sofia Vieira', 'sofia.vieira@email.pt', '1994-10-02', 'Rua das Oliveiras, 19', '961000016'),
('74757677', 'Tiago Almeida', 'tiago.almeida@email.pt', '1983-04-29', 'Avenida 25 de Abril, 88', '911000017'),
('78798081', 'Vânia Lopes', 'vania.lopes@email.pt', '2001-12-19', 'Travessa dos Moinhos, 30', '921000018'),
('82838485', 'Xavier Costa', 'xavier.costa@email.pt', '1978-09-04', 'Rua da Alfândega, 2', '931000019'),
('86878889', 'Zara Mendes', 'zara.mendes@email.pt', '1991-01-13', 'Largo da Misericórdia, 4', '961000020'),
('11223344', 'Hugo Duarte', 'hugo.duarte@email.pt', '1984-05-09', 'Rua dos Combatentes, 10', '912000001'),
('22334455', 'Inês Barros', 'ines.barros@email.pt', '1996-02-28', 'Av. da Boavista, 150', '922000002'),
('33445566', 'João Gomes', 'joao.gomes@email.pt', '1979-08-12', 'Bairro Novo, 22', '932000003'),
('44556677', 'Luísa Castro', 'luisa.castro@email.pt', '1997-03-25', 'Rua do Sol, 40', '962000004'),
('55667788', 'Miguel Nunes', 'miguel.nunes@email.pt', '1981-11-03', 'Praça Velha, 6', '912000005'),
('66778899', 'Rita Ferreira', 'rita.ferreira@email.pt', '1993-06-19', 'Estrada Principal, 77', '922000006'),
('77889900', 'Sérgio Reis', 'sergio.reis@email.pt', '1974-01-01', 'Rua da Fonte, 35', '932000007'),
('88990011', 'Teresa Santos', 'teresa.santos@email.pt', '1990-10-10', 'Largo da Matriz, 8', '962000008'),
('99001122', 'Vítor Paiva', 'vitor.paiva@email.pt', '1986-04-04', 'Rua da Indústria, 10', '912000009'),
('00112233', 'Yara Pires', 'yara.pires@email.pt', '1995-07-07', 'Avenida das Nações, 15', '922000010');

INSERT INTO Empresa (Nif, Nome, Localizacao, NumTelefone, Email) VALUES
('500111222', 'TexPrime Confecções SA', 'Guimarães', '253100001', 'geral@texprime.pt'),
('500333444', 'FastFashion Store Portugal', 'Lisboa', '213200002', 'info@fastfashion.pt'),
('500555666', 'Tricot & Malhas do Ave', 'Vila do Conde', '252300003', 'producao@tricotave.pt'),
('500777888', 'Algodão Sustentável Lda', 'Covilhã', '275400004', 'admin@algodaosustentavel.pt'),
('500999000', 'Logística Têxtil Rápida', 'Porto', '225500005', 'suporte@logistex.pt');

INSERT INTO Distribuidora (Nome, Localizacao) VALUES
('DistriVestuário Norte', 'Viana do Castelo'),
('DistriAcessórios Sul', 'Setúbal'),
('DistriTecidos Centro', 'Castelo Branco');

INSERT INTO Armazem (Localizacao, Capacidade) VALUES
('Famalicão', 10000),
('Porto - Centro Logístico', 5000),
('Lisboa - Loja Principal', 8000),
('Guarda', 7000),
('Barcelos', 4500);

INSERT INTO Cargo (Nome, Descricao) VALUES
('Estilista/Designer', 'Criação e desenvolvimento de coleções de vestuário.'),
('Gestor de Compras Têxteis', 'Negociação e aquisição de tecidos e matérias-primas.'),
('Técnico de Manutenção de Máquinas', 'Manutenção de teqs e máquinas de costura.'),
('Operador de Costura', 'Execução de costura industrial e acabamentos.'),
('Diretor de Produção de Confecção', 'Gestão e otimização das linhas de produção.'),
('Analista de Qualidade Têxtil', 'Controlo de qualidade de tecidos e artigos finais.'),
('Vendedor de Retalho', 'Vendas diretas ao público nas lojas.'),
('Responsável de Logística', 'Gestão de transporte e stock.');

INSERT INTO Cliente (Pessoa_Cc, Nif) VALUES
('18192021', '100100100'),
('22232425', '200200200'),
('26272829', '300300300'),
('30313233', '400400400'),
('34353637', '500500500'),
('38394041', '600600600'),
('42434445', '700700700'),
('46474849', '800800800'),
('50515253', '900900900'),
('54555657', '111222333'),
('58596061', '444555666'),
('62636465', '777888999'),
('66778899', '123123123'),
('77889900', '456456456'),
('88990011', '789789789');

INSERT INTO Vendedor (Pessoa_Cc, NumVendas, Cargo_Id) VALUES
('10111213', 150, 7),
('14151617', 280, 2),
('70717273', 95, 7),
('74757677', 310, 2),
('78798081', 40, 7);

INSERT INTO Fornecedor (Nome, Empresa_Nif) VALUES
('Fios e Linhas Premium Lda', '500111222'),
('Aviamentos e Botões SA', '500333444'),
('Malharia Industrial Teixeira', '500555666'),
('Algodão Sustentável Lda', '500777888'),
('Químicos de Tingimento Ecológicos', '500999000');

INSERT INTO DistribuidoraArmazem (Distribuidora_Id, Armazem_Id) VALUES
(1, 1),
(1, 3),
(2, 2),
(3, 4),
(3, 5);

INSERT INTO Loja (Nome, Localizacao, Armazem_Id) VALUES
('Loja Flagship Lisboa', 'Lisboa', 3),
('Loja Shopping Porto', 'Porto', 2),
('Outlet Setúbal', 'Setúbal', 2),
('Loja Aveiro', 'Aveiro', 4),
('Pop-up Guimarães', 'Guimarães', 1);

INSERT INTO Fabrica (Nome, Localizacao, Empresa_Nif, Distribuidora_Id) VALUES
('Unidade Confecção 1', 'Braga', '500111222', 1),
('Unidade Malhas', 'Évora', '500333444', 2),
('Unidade Estamparia e Acabamentos', 'Leiria', '500111222', 3);

INSERT INTO ContratoVendedor (DataIn, Empresa_Nif, Vendedor_Id, DataOut) VALUES
('2024-01-10', '500333444', 1, NULL),
('2023-05-20', '500555666', 2, NULL),
('2024-03-01', '500333444', 3, NULL),
('2022-11-15', '500555666', 4, NULL),
('2024-06-25', '500333444', 5, NULL);

INSERT INTO MateriaPrima (Referencia, Descricao, Fornecedor_Id) VALUES
('FIO001', 'Fio de Algodão Penteado, Cor Branca', 1),
('BTO002', 'Botão de Madrepérola (Pack 1000)', 2),
('TEC003', 'Tecido de Ganga Raw Denim', 3),
('ALG004', 'Fardo de Algodão Orgânico Cru', 4),
('QIM005', 'Corante Azul Índigo Ecológico', 5);

INSERT INTO Maquina (Descricao, Tipo, Fabrica_Id) VALUES
('Máquina de Corte Automático Laser', 'Corte', 1),
('Linha de Costura Modular Programável', 'Costura', 1),
('Máquina de Tricô Retilíneo', 'Malhas', 2),
('Impressora Digital Têxtil (DTG)', 'Estamparia', 3),
('Máquina de Overlock Industrial', 'Acabamento', 1);

INSERT INTO Funcionario (Pessoa_Cc, Cargo_Id, Empresa_Nif, Fabrica_Id) VALUES
('11223344', 3, '500111222', 1),
('22334455', 4, '500111222', 1),
('33445566', 4, '500333444', 2),
('44556677', 5, '500111222', 1),
('55667788', 1, '500111222', NULL),
('82838485', 6, '500333444', 2),
('86878889', 8, '500999000', NULL),
('99001122', 7, '500333444', NULL),
('00112233', 6, '500111222', 3),
('14151617', 5, '500333444', 2);

INSERT INTO Produto (Referencia, Descricao, Nome, Preco, Maquina_Id, Distribuidora_Id) VALUES
('CAM001', 'Camisa de algodão orgânico, corte slim', 'Camisa Casual Eco', 45, 2, 1),
('JNS002', 'Calças de ganga com lavagem a frio', 'Jeans Denim Vintage', 65, 1, 2),
('SWE003', 'Camisola de malha fina, gola redonda', 'Sweater Fio Merino', 79, 3, 3),
('ACR004', 'Cachecol de lã acrílica tingida', 'Cachecol Inverno', 18, 5, 2),
('TEC005', 'Tecido de Sarja de Algodão (por metro)', 'Sarja 100% Algodão', 8, 1, 1),
('TSH006', 'T-shirt básica com estampa DTG', 'T-shirt Logo Urbano', 25, 4, 1),
('BLZ007', 'Blazer de linho com forro de seda', 'Blazer Executivo', 140, 2, 3),
('SAI008', 'Saia plissada de comprimento médio', 'Saia Plissé Verão', 35, 2, 2),
('MCH009', 'Máscara de proteção reutilizável (pack 5)', 'Máscaras Higiénicas', 10, 5, 1),
('LUZ010', 'Camisola em Ponto de Arroz', 'Camisola Ponto Arroz', 55, 3, 3),
('VEST011', 'Vestido comprido de padrão floral', 'Vestido Boho', 89, 2, 1),
('TEC012', 'Rolo de Malha Canelada (100 metros)', 'Malha Canelada Premium', 300, 3, 3),
('PUL013', 'Pullover de Caxemira sintética', 'Pullover Macio', 49, 3, 2),
('MEIAS014', 'Meias desportivas de compressão (pack 3)', 'Meias Sports', 12, 5, 1),
('CASA015', 'Casaco de penas leve e impermeável', 'Parka Ultralight', 99, 1, 3);

INSERT INTO Stock (UltimoMov, Quantidade, Produto_Referencia, Armazem_Id) VALUES
('2025-11-20', 300, 'CAM001', 1),
('2025-11-21', 150, 'JNS002', 2),
('2025-11-19', 200, 'SWE003', 1),
('2025-11-22', 500, 'ACR004', 2),
('2025-11-20', 1000, 'TEC005', 5),
('2025-11-18', 400, 'TSH006', 3),
('2025-11-23', 80, 'BLZ007', 2),
('2025-11-20', 120, 'SAI008', 1),
('2025-11-24', 900, 'MCH009', 4),
('2025-11-17', 150, 'LUZ010', 3),
('2025-11-21', 110, 'VEST011', 5),
('2025-11-25', 20, 'TEC012', 3),
('2025-11-20', 250, 'PUL013', 2),
('2025-11-22', 600, 'MEIAS014', 4),
('2025-11-19', 70, 'CASA015', 1);

INSERT INTO Venda (DataHora, ValorTotal, MetodoPagamento, Loja_Id, Cliente_Pessoa_Cc) VALUES
('2025-11-22 10:30:00', 118, 'Cartão de Crédito', 1, '18192021'),
('2025-11-22 14:00:00', 176, 'MB WAY', 2, '22232425'),
('2025-11-23 09:15:00', 180, 'Dinheiro', 3, '26272829'),
('2025-11-23 16:45:00', 94, 'Transferência Bancária', 4, '30313233'),
('2025-11-24 11:20:00', 10, 'Cartão de Débito', 5, '34353637'),
('2025-11-24 15:50:00', 90, 'MB WAY', 1, '38394041'),
('2025-11-25 10:05:00', 300, 'Cartão de Crédito', 2, '42434445'),
('2025-11-25 13:30:00', 70, 'Dinheiro', 3, '46474849'),
('2025-11-26 12:40:00', 122, 'MB WAY', 4, '50515253'),
('2025-11-26 17:10:00', 124, 'Cartão de Débito', 5, '54555657');

INSERT INTO Item (Quantidade, Preco, Venda_Id, Produto_Referencia) VALUES
(1, 45.00, 1, 'CAM001'),
(1, 65.00, 1, 'JNS002'),
(1, 8.00, 1, 'TEC005'),
(2, 79.00, 2, 'SWE003'),
(1, 18.00, 2, 'ACR004'),
(1, 140.00, 3, 'BLZ007'),
(5, 8.00, 3, 'TEC005'),
(1, 25.00, 3, 'TSH006'),
(1, 89.00, 4, 'VEST011'),
(1, 5.00, 4, 'ACR004'),
(1, 10.00, 5, 'MCH009'),
(1, 35.00, 6, 'SAI008'),
(1, 55.00, 6, 'LUZ010'),
(1, 300.00, 7, 'TEC012'),
(2, 25.00, 8, 'TSH006'),
(1, 20.00, 8, 'ACR004'),
(2, 49.00, 9, 'PUL013'),
(2, 12.00, 9, 'MEIAS014'),
(1, 99.00, 10, 'CASA015'),
(1, 25.00, 10, 'TSH006');