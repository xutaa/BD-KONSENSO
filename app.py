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
        
        return render_template('produtos.html', 
                               dados_produtos=produtos,
                               sucesso=True)

    except ConnectionError as e:
        return render_template('produtos.html', erro=str(e), sucesso=False)
        
    except Exception as e:
        return render_template('produtos.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
        
    finally:
        if conn:
            conn.close()

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
        
        return render_template('empresas.html', 
                               dados_empresas=empresas,
                               sucesso=True)

    except ConnectionError as e:
        return render_template('empresas.html', erro=str(e), sucesso=False)
        
    except Exception as e:
        return render_template('empresas.html', erro=f"Erro na query SQL: {str(e)}", sucesso=False)
        
    finally:
        if conn:
            conn.close()

@app.route('/produtos/novo')
def novo_produto():
    return "Aqui será o formulário para Novo Produto (Fase 2)"

if __name__ == '__main__':
    app.run(debug=True)