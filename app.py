from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection
import pyodbc

app = Flask(__name__)
app.secret_key = 'bd_konsenso_secret_key_2024'  # Necessário para o login funcionar

# --- FUNÇÕES DE AUTENTICAÇÃO ---

print("--- A INICIAR APLICAÇÃO ---")
try:
    from flask import Flask
    print("Flask importado com sucesso")
except ImportError:
    print("ERRO: Flask não está instalado! Corra: pip install flask")

def validar_administrador(nome, password):
    """Verifica login na tabela Administradores"""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Nome FROM Administradores WHERE Nome = ? AND Password = ?", (nome, password))
        admin = cursor.fetchone()
        return admin is not None
    except Exception as e:
        print(f"Erro login: {e}")
        return False
    finally:
        conn.close()

def criar_novo_administrador(nome, email, password, tipo_admin):
    """Cria novo registo na tabela Administradores"""
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Administradores (Nome, Email, Password, Tipo_Admin) VALUES (?, ?, ?, ?)", 
                      (nome, email, password, tipo_admin))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao criar admin: {e}")
        return False
    finally:
        conn.close()

# --- ROTAS DE LOGIN / REGISTO / LOGOUT ---

@app.route('/')
def index():
    # Redireciona para dashboard se logado, ou login se não
    if 'admin_logado' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        password = request.form['password']
        if validar_administrador(nome, password):
            session['admin_logado'] = nome
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        tipo_admin = request.form.get('tipo_admin')
        
        if password != confirm_password:
            return render_template('registo.html', error='As passwords não coincidem')
        
        if criar_novo_administrador(nome, email, password, tipo_admin):
            return redirect(url_for('login', success='Administrador registado com sucesso!'))
        else:
            return render_template('registo.html', error='Erro: Nome ou Email já existem.')
    return render_template('registo.html')

@app.route('/logout')
def logout():
    session.pop('admin_logado', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    
    roadmap_status = {
        "Fase 1: Leitura (Listagem)": "✅ Concluída (Todas as Tabelas)",
        "Fase 2: Inserção (Novo Produto)": "Em Desenvolvimento",
        "Fase 3: Edição e Remoção": "A Iniciar",
        "Fase 4: Relatórios Complexos": "A Iniciar"
    }
    return render_template('dashboard.html', roadmap=roadmap_status, usuario=session['admin_logado'])

# --- ROTAS DE DADOS (DO SEU COLEGA) COM PROTEÇÃO DE LOGIN ---

@app.route('/armazens')
def lista_armazens():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Localizacao, Capacidade FROM dbo.Armazem")
        armazens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/armazens.html', dados_armazens=armazens, sucesso=True)
    except Exception as e:
        return render_template('tabelas/armazens.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/cargos')
def lista_cargos():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Descricao FROM dbo.Cargo")
        cargos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/cargos.html', dados_cargos=cargos, sucesso=True)
    except Exception as e:
        return render_template('tabelas/cargos.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/clientes')
def lista_clientes():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Pessoa_Cc, Nif, Nome, Email, DataNascimento, Morada, NumTelefone FROM dbo.Cliente C JOIN dbo.Pessoa P ON C.Pessoa_Cc = P.Cc")
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/clientes.html', dados_clientes=clientes, sucesso=True)
    except Exception as e:
        return render_template('tabelas/clientes.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/contratos_vendedor')
def lista_contratos_vendedor():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT DataIn, Empresa_Nif, Vendedor_Id FROM dbo.ContratoVendedor")
        contratos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/contratos_vendedor.html', dados_contratos=contratos, sucesso=True)
    except Exception as e:
        return render_template('tabelas/contratos_vendedor.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/distribuidoras')
def lista_distribuidoras():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Localizacao FROM dbo.Distribuidora")
        distribuidoras = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/distribuidoras.html', dados_distribuidoras=distribuidoras, sucesso=True)
    except Exception as e:
        return render_template('tabelas/distribuidoras.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/distribuidoras_armazem')
def lista_distribuidoras_armazem():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Distribuidora_Id, Armazem_Id FROM dbo.DistribuidoraArmazem")
        dados = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/distribuidoras_armazem.html', dados=dados, sucesso=True)
    except Exception as e:
        return render_template('tabelas/distribuidoras_armazem.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/empresas')
def lista_empresas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Nif, Nome, Localizacao, NumTelefone, Email FROM dbo.Empresa")
        empresas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/empresas.html', dados_empresas=empresas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/empresas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/fabricas')
def lista_fabricas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Localizacao, Empresa_Nif, Distribuidora_Id FROM dbo.Fabrica")
        fabricas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/fabricas.html', dados_fabricas=fabricas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/fabricas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/fornecedores')
def lista_fornecedores():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Empresa_Nif FROM dbo.Fornecedor")
        fornecedores = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/fornecedores.html', dados_fornecedores=fornecedores, sucesso=True)
    except Exception as e:
        return render_template('tabelas/fornecedores.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/funcionarios')
def lista_funcionarios():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Funcionario")
        funcionarios = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/funcionarios.html', dados_funcionarios=funcionarios, sucesso=True)
    except Exception as e:
        return render_template('tabelas/funcionarios.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/itens')
def lista_itens():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Quantidade, Preco, Venda_Id, Produto_Referencia FROM dbo.Item")
        itens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/itens.html', dados_itens=itens, sucesso=True)
    except Exception as e:
        return render_template('tabelas/itens.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/lojas')
def lista_lojas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Loja")
        lojas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/lojas.html', dados_lojas=lojas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/lojas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/maquinas')
def lista_maquinas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Maquina")
        maquinas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/maquinas.html', dados_maquinas=maquinas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/maquinas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/materias_primas')
def lista_materias_primas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.MateriaPrima")
        materias_primas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/materias_primas.html', dados_materias_primas=materias_primas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/materias_primas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/pessoas')
def lista_pessoas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Pessoa")
        pessoas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/pessoas.html', dados_pessoas=pessoas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/pessoas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/produtos')
def lista_produtos():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT Referencia, Descricao, Nome, Preco, Maquina_ID, Distribuidora_ID FROM dbo.Produto")
        produtos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/produtos.html', dados_produtos=produtos, sucesso=True)
    except Exception as e:
        return render_template('tabelas/produtos.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/stock')
def lista_stock():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Stock")
        stock = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/stock.html', dados_stock=stock, sucesso=True)
    except Exception as e:
        return render_template('tabelas/stock.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/vendas')
def lista_vendas():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Venda")
        vendas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/vendas.html', dados_vendas=vendas, sucesso=True)
    except Exception as e:
        return render_template('tabelas/vendas.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/vendedores')
def lista_vendedores():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: raise ConnectionError("Conexão falhou.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Vendedor")
        vendedores = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/vendedores.html', dados_vendedores=vendedores, sucesso=True)
    except Exception as e:
        return render_template('tabelas/vendedores.html', erro=str(e), sucesso=False)
    finally:
        if conn: conn.close()

@app.route('/produtos/novo')
def novo_produto():
    if 'admin_logado' not in session: return redirect(url_for('login'))
    return "Aqui será o formulário para Novo Produto"

if __name__ == '__main__':
    app.run(debug=True)