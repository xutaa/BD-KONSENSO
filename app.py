import flask
from flask import render_template
from database import get_db_connection

app = flask.Flask(__name__)

@app.route('/')
def index():
    """
    Rota padrão. Exibe o roadmap de desenvolvimento e links essenciais.
    Esta função não faz conexão com o BD.
    """
    roadmap_status = {
        "Fase 1: Leitura (Listagem)": "✅ Concluída (Produtos)",
        "Fase 2: Inserção (Novo Produto)": "Em Desenvolvimento",
        "Fase 3: Edição e Remoção": "A Iniciar",
        "Fase 4: Relatórios Complexos": "A Iniciar"
    }
    
    return render_template('dashboard.html', roadmap=roadmap_status)


@app.route('/armazens')
def lista_armazens():
    """
    Rota /armazens. Lista todos os armazéns da tabela dbo.Armazem.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise ConnectionError("Conexão com o banco de dados falhou. Verifique os logs.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Localizacao, Capacidade FROM dbo.Armazem")
        armazens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/armazens.html', 
                               dados_armazens=armazens,
                               sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/armazens.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/armazens.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/cargos')
def lista_cargos():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Descricao FROM dbo.Cargo")
        cargos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/cargos.html', dados_cargos=cargos, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/cargos.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/cargos.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/clientes')
def lista_clientes():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Pessoa_Cc, Nif, Nome, Email, DataNascimento, Morada, NumTelefone " \
            "FROM dbo.Cliente C " \
            "JOIN dbo.Pessoa P ON C.Pessoa_Cc = P.Cc"
        )
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/clientes.html', dados_clientes=clientes, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/clientes.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/clientes.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/contratos_vendedor')
def lista_contratos_vendedor():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT DataIn, Empresa_Nif, Vendedor_Id FROM dbo.ContratoVendedor")
        contratos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/contratos_vendedor.html', dados_contratos=contratos, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/contratos_vendedor.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/contratos_vendedor.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/distribuidoras')
def lista_distribuidoras():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Localizacao FROM dbo.Distribuidora")
        distribuidoras = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/distribuidoras.html', dados_distribuidoras=distribuidoras, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/distribuidoras.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/distribuidoras.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/distribuidoras_armazem')
def lista_distribuidoras_armazem():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Distribuidora_Id, Armazem_Id FROM dbo.DistribuidoraArmazem")
        dados = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/distribuidoras_armazem.html', dados=dados, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/distribuidoras_armazem.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/distribuidoras_armazem.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/empresas')
def lista_empresas():
    """
    Rota /empresas. Lista todos as empresas da tabela dbo.Empresa.
    """
    conn = None
    try:
        conn = get_db_connection()
        
        if conn is None:
            raise ConnectionError("Conexão com o banco de dados falhou. Verifique os logs.")

        cursor = conn.cursor()
        
        cursor.execute("SELECT Nif, Nome, Localizacao, NumTelefone, Email FROM dbo.Empresa")
        empresas = cursor.fetchall()
        cursor.close()
        
        return render_template('tabelas/empresas.html', 
                               dados_empresas=empresas,
                               sucesso=True)

    except ConnectionError as e:
        return render_template('tabelas/empresas.html', erro=str(e), sucesso=False)
        
    except Exception as e:
        return render_template('tabelas/empresas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
        
    finally:
        if conn:
            conn.close()

@app.route('/fabricas')
def lista_fabricas():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Localizacao, Empresa_Nif, Distribuidora_Id FROM dbo.Fabrica")
        fabricas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/fabricas.html', dados_fabricas=fabricas, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/fabricas.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/fabricas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/fornecedores')
def lista_fornecedores():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Empresa_Nif FROM dbo.Fornecedor")
        fornecedores = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/fornecedores.html', dados_fornecedores=fornecedores, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/fornecedores.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/fornecedores.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/funcionarios')
def lista_funcionarios():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Funcionario")
        funcionarios = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/funcionarios.html', dados_funcionarios=funcionarios, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/funcionarios.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/funcionarios.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/itens')
def lista_itens():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Quantidade, Preco, Venda_Id, Produto_Referencia FROM dbo.Item")
        itens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/itens.html', dados_itens=itens, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/itens.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/itens.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/lojas')
def lista_lojas():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: LojaID, Nome, Localizacao
        cursor.execute("SELECT * FROM dbo.Loja")
        lojas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/lojas.html', dados_lojas=lojas, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/lojas.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/lojas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/maquinas')
def lista_maquinas():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: MaquinaID, Modelo, Tipo
        cursor.execute("SELECT * FROM dbo.Maquina")
        maquinas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/maquinas.html', dados_maquinas=maquinas, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/maquinas.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/maquinas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/materias_primas')
def lista_materias_primas():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: MateriaPrimaID, Nome, UnidadeMedida
        cursor.execute("SELECT * FROM dbo.MateriaPrima")
        materias_primas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/materias_primas.html', dados_materias_primas=materias_primas, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/materias_primas.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/materias_primas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/pessoas')
def lista_pessoas():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: PessoaID, Nome, NIF
        cursor.execute("SELECT * FROM dbo.Pessoa")
        pessoas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/pessoas.html', dados_pessoas=pessoas, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/pessoas.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/pessoas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/produtos')
def lista_produtos():
    """
    Rota /produtos. Lista todos os produtos da tabela dbo.Produto.
    """
    conn = None
    try:
        conn = get_db_connection()
        
        if conn is None:
            raise ConnectionError("Conexão com o banco de dados falhou. Verifique os logs.")

        cursor = conn.cursor()
        
        cursor.execute("SELECT Referencia, Descricao, Nome, Preco, Maquina_ID, Distribuidora_ID FROM dbo.Produto")
        produtos = cursor.fetchall()
        cursor.close()
        
        return render_template('tabelas/produtos.html', 
                               dados_produtos=produtos,
                               sucesso=True)

    except ConnectionError as e:
        return render_template('tabelas/produtos.html', erro=str(e), sucesso=False)
        
    except Exception as e:
        return render_template('tabelas/produtos.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
        
    finally:
        if conn:
            conn.close()

@app.route('/stock')
def lista_stock():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: StockID, ProdutoID/MateriaPrimaID, Quantidade
        cursor.execute("SELECT * FROM dbo.Stock")
        stock = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/stock.html', dados_stock=stock, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/stock.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/stock.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/vendas')
def lista_vendas():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: VendaID, Data, ClienteID, VendedorID
        cursor.execute("SELECT * FROM dbo.Venda")
        vendas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/vendas.html', dados_vendas=vendas, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/vendas.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/vendas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/vendedores')
def lista_vendedores():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        # Ajuste as colunas: VendedorID, PessoaID, Salario
        cursor.execute("SELECT * FROM dbo.Vendedor")
        vendedores = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/vendedores.html', dados_vendedores=vendedores, sucesso=True)
    except ConnectionError as e:
        return render_template('tabelas/vendedores.html', erro=str(e), sucesso=False)
    except Exception as e:
        return render_template('tabelas/vendedores.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/produtos/novo')
def novo_produto():
    return "Aqui será o formulário para Novo Produto (Fase 2)"

if __name__ == '__main__':
    app.run(debug=True)