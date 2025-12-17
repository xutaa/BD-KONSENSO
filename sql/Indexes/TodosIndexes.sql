CREATE OR ALTER NONCLUSTERED INDEX Venda_LojaData 
ON Venda(Loja_Id, Data_Venda) INCLUDE (ValorTotal);

CREATE OR ALTER NONCLUSTERED INDEX Item_Produto 
ON Item(Produto_Referencia) INCLUDE (Quantidade, Preco);

CREATE OR ALTER NONCLUSTERED INDEX Stock_Produto 
ON Stock(Produto_Referencia, Armazem_Id) INCLUDE (Quantidade);

-- Ainda NADA usado