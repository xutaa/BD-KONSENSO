from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'bd_konsenso_secret_key_2024'

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def validar_administrador(nome, password):
    """Verifica login na tabela Administradores"""
    conn = get_db_connection()
    if not conn: 
        print("❌ Erro: Sem conexão à base de dados")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Nome FROM Administradores WHERE Nome = ? AND Password = ?", (nome, password))
        admin = cursor.fetchone()
        if admin:
            print(f"✅ Login bem-sucedido: {nome}")
            return True
        else:
            print(f"❌ Login falhou: {nome}")
            return False
    except Exception as e:
        print(f"❌ Erro ao validar login: {e}")
        return False
    finally:
        conn.close()

def criar_novo_administrador(nome, email, password, tipo_admin):
    """Cria novo registo na tabela Administradores"""
    conn = get_db_connection()
    if not conn: 
        print("❌ Erro: Sem conexão à base de dados")
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Nome FROM Administradores WHERE Nome = ?", (nome,))
        if cursor.fetchone():
            print(f"❌ Nome '{nome}' já existe na base de dados")
            return False
        
        cursor.execute(
            "INSERT INTO Administradores (Nome, Email, Password, Tipo_Admin) VALUES (?, ?, ?, ?)", 
            (nome, email, password, tipo_admin)
        )
        conn.commit()
        print(f"✅ Administrador '{nome}' criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar administrador: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# --- ROTAS DE LOGIN / REGISTO / LOGOUT ---

@app.route('/')
def index():
    """Redireciona para dashboard se logado, senão para login"""
    if 'admin_logado' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login - valida e cria sessão"""
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        password = request.form.get('password', '').strip()
        
        if not nome or not password:
            return render_template('login.html', error="Preencha todos os campos.")
        
        if validar_administrador(nome, password):
            session['admin_logado'] = nome
            print(f"🎉 Sessão criada para: {nome}")
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Nome ou Password incorretos.")
    
    # GET request - mostra formulário
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    """Página de registo - cria novo administrador na BD"""
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        tipo_admin = request.form.get('tipo_admin', 'Geral')
        
        # Validações
        if not nome or not email or not password:
            return render_template('registo.html', error="Preencha todos os campos obrigatórios.")
        
        if password != confirm_password:
            return render_template('registo.html', error="As passwords não coincidem.")
        
        if len(password) < 4:
            return render_template('registo.html', error="A password deve ter pelo menos 4 caracteres.")
        
        # Tenta criar na base de dados
        if criar_novo_administrador(nome, email, password, tipo_admin):
            return redirect(url_for('login', success="✅ Conta criada com sucesso! Faça login."))
        else:
            return render_template('registo.html', error="❌ Erro ao criar conta. O nome pode já existir.")
    
    # GET request - mostra formulário
    return render_template('registo.html')

@app.route('/logout')
def logout():
    """Remove sessão e redireciona para login"""
    nome = session.get('admin_logado', 'Desconhecido')
    session.pop('admin_logado', None)
    print(f"👋 Logout: {nome}")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Página principal - só acessível após login"""
    if 'admin_logado' not in session:
        print("⚠️ Tentativa de acesso sem login")
        return redirect(url_for('login'))
    
    roadmap_status = {
        "Fase 1: Leitura (Listagem)": "✅ Concluída",
        "Fase 2: Inserção": "Produtos Done, Outros a Fazer",
        "Fase 3: Edição e Remoção": "Não Iniciada",
        "Fase 4: Relatórios": "Não Iniciada",
    }
    
    return render_template('dashboard.html', 
                         roadmap=roadmap_status, 
                         usuario=session['admin_logado'])

# --- ROTAS DE DADOS (Protegidas por login) ---
@app.route('/armazens')
def lista_armazens():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/armazens.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Localizacao, Capacidade FROM dbo.Armazem")
        armazens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/armazens.html', dados_armazens=armazens, sucesso=True)
    except Exception as e:
        return render_template('tabelas/armazens.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/cargos')
def lista_cargos():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/cargos.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Cargo")
        cargos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/cargos.html', dados_cargos=cargos, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar cargos: {e}")
        return render_template('tabelas/cargos.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/clientes')
def lista_clientes():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/clientes.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT C.Pessoa_Cc, C.Nif, P.Nome, P.Email, P.DataNascimento, P.Morada, P.NumTelefone 
            FROM dbo.Cliente C 
            JOIN dbo.Pessoa P ON C.Pessoa_Cc = P.Cc
        """)
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/clientes.html', dados_clientes=clientes, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar clientes: {e}")
        return render_template('tabelas/clientes.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/contratos_vendedor')
def lista_contratos_vendedor():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/contratos_vendedor.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT DataIn, Empresa_Nif, Vendedor_Id FROM dbo.ContratoVendedor")
        contratos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/contratos_vendedor.html', dados_contratos=contratos, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar contratos vendedor: {e}")
        return render_template('tabelas/contratos_vendedor.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/distribuidoras')
def lista_distribuidoras():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/distribuidoras.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Localizacao FROM dbo.Distribuidora")
        distribuidoras = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/distribuidoras.html', dados_distribuidoras=distribuidoras, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar distribuidoras: {e}")
        return render_template('tabelas/distribuidoras.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/distribuidoras_armazem')
def lista_distribuidoras_armazem():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/distribuidoras_armazem.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Distribuidora_Id, Armazem_Id FROM dbo.DistribuidoraArmazem")
        dados = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/distribuidoras_armazem.html', dados=dados, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar distribuidoras armazem: {e}")
        return render_template('tabelas/distribuidoras_armazem.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/empresas')
def lista_empresas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/empresas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Nif, Nome, Localizacao, NumTelefone, Email FROM dbo.Empresa")
        empresas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/empresas.html', dados_empresas=empresas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar empresas: {e}")
        return render_template('tabelas/empresas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/fabricas')
def lista_fabricas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/fabricas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Localizacao, Empresa_Nif, Distribuidora_Id FROM dbo.Fabrica")
        fabricas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/fabricas.html', dados_fabricas=fabricas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar fabricas: {e}")
        return render_template('tabelas/fabricas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/fornecedores')
def lista_fornecedores():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/fornecedores.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Empresa_Nif FROM dbo.Fornecedor")
        fornecedores = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/fornecedores.html', dados_fornecedores=fornecedores, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar fornecedores: {e}")
        return render_template('tabelas/fornecedores.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/funcionarios')
def lista_funcionarios():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/funcionarios.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id, Pessoa_Cc, Nome, Email, DataNascimento, Morada, NumTelefone, Empresa_Nif, Cargo_Id
            FROM Funcionario F
            JOIN Pessoa P ON F.Pessoa_Cc = P.Cc
        """)
        funcionarios = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/funcionarios.html', dados_funcionarios=funcionarios, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar funcionarios: {e}")
        return render_template('tabelas/funcionarios.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/itens')
def lista_itens():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/itens.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Quantidade, Preco, Venda_Id, Produto_Referencia FROM dbo.Item")
        itens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/itens.html', dados_itens=itens, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar itens: {e}")
        return render_template('tabelas/itens.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/lojas')
def lista_lojas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/lojas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
                SELECT Id, Nome, Localizacao, Armazem_Id FROM dbo.Loja
            """)
        lojas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/lojas.html', dados_lojas=lojas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar lojas: {e}")
        return render_template('tabelas/lojas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/maquinas')
def lista_maquinas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/maquinas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Descricao, Tipo, Fabrica_Id FROM dbo.Maquina")
        maquinas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/maquinas.html', dados_maquinas=maquinas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar maquinas: {e}")
        return render_template('tabelas/maquinas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/materias_primas')
def lista_materias_primas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/materias_primas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Referencia, Descricao, Fornecedor_Id FROM dbo.MateriaPrima
            """)
        materias_primas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/materias_primas.html', dados_materias_primas=materias_primas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar materias primas: {e}")
        return render_template('tabelas/materias_primas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/pessoas')
def lista_pessoas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/pessoas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Cc, Nome, Email, DataNascimento, Morada, NumTelefone FROM dbo.Pessoa
        """)
        pessoas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/pessoas.html', dados_pessoas=pessoas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar pessoas: {e}")
        return render_template('tabelas/pessoas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/produtos')
def lista_produtos():
    """
    Rota /produtos. 
    1. Lista todos os produtos para a tabela.
    2. Busca Máquinas e Distribuidoras para preencher os Selects do Modal.
    """
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    
    conn = None
    dados_produtos = []
    maquinas = []           # Lista para o Dropdown
    distribuidoras = []     # Lista para o Dropdown
    sucesso = False
    erro = None

    try:
        conn = get_db_connection()
        if conn is None:
             raise ConnectionError("Conexão com o banco de dados falhou.")

        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT Referencia, Descricao, Nome, Preco, Maquina_Id, Distribuidora_Id 
            FROM dbo.Produto
        """) 
        dados_produtos = cursor.fetchall()
        
        cursor.execute("SELECT Id, Descricao FROM dbo.Maquina") 
        maquinas = cursor.fetchall()

        cursor.execute("SELECT Id, Nome FROM dbo.Distribuidora")
        distribuidoras = cursor.fetchall()
        
        sucesso = True

    except Exception as e:
        erro = f"Erro ao carregar dados: {str(e)}"
        print(f"❌ {erro}")
        
    finally:
        if conn:
            conn.close()

    return render_template('tabelas/produtos.html', 
                           dados_produtos=dados_produtos,
                           maquinas=maquinas,            
                           distribuidoras=distribuidoras,
                           sucesso=sucesso,
                           erro=erro)

@app.route('/produto/novo', methods=['POST'])
def adicionar_produto():
    """
    Processa a submissão do Modal e insere um novo produto no BD através de uma SP.
    """
    if 'admin_logado' not in session: 
        flash('Sessão expirada. Faça login novamente.', 'error')
        return redirect(url_for('login'))

    referencia = request.form.get('referencia', '').strip()
    descricao = request.form.get('descricao', '').strip()
    nome = request.form.get('nome', '').strip()
    preco_str = request.form.get('preco', '').replace(',', '.')
    maquina_id_str = request.form.get('maquina_id', '').strip()
    distribuidora_id_str = request.form.get('distribuidora_id', '').strip()
    
    conn = None
    
    try:
        if not referencia or not nome or not preco_str:
            flash('Erro: Os campos Referência, Nome e Preço são obrigatórios.', 'error')
            return redirect(url_for('lista_produtos'))

        try:
            preco = float(preco_str)
            if preco <= 0:
                raise ValueError("O preço deve ser positivo.")
            
            maquina_id = int(maquina_id_str) if maquina_id_str else None
            distribuidora_id = int(distribuidora_id_str) if distribuidora_id_str else None
            
        except ValueError as e:
            flash(f'Erro de formato: Preço, Máquina ID e Distribuidora ID devem ser numéricos válidos. Detalhe: {e}', 'error')
            return redirect(url_for('lista_produtos'))

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("{CALL dbo.InserirNovoProduto (?, ?, ?, ?, ?, ?)}", 
                       referencia, 
                       descricao, 
                       nome, 
                       preco, 
                       maquina_id, 
                       distribuidora_id)
        
        conn.commit()
        
        try:
            produto_id = cursor.fetchone()[0]
            flash(f'Produto "{nome}" (Ref: {referencia}) registado com sucesso! ID: {produto_id}', 'success')
        except:
            flash(f'Produto "{nome}" (Ref: {referencia}) registado com sucesso!', 'success')
        
        return redirect(url_for('lista_produtos'))
        
    except Exception as e:
        if conn:
            conn.rollback()
        
        print(f"❌ Erro ao inserir produto: {e}")
        flash(f'Falha ao registar o produto no banco de dados. Detalhe: {str(e)}', 'error')
        
        return redirect(url_for('lista_produtos'))
            
    finally:
        if conn:
            conn.close()

@app.route('/stock')
def lista_stock():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/stock.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT UltimoMov, Quantidade, Produto_Referencia, Armazem_Id FROM dbo.Stock
        """)
        stock = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/stock.html', dados_stock=stock, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar stock: {e}")
        return render_template('tabelas/stock.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/vendas')
def lista_vendas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/vendas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, DataHora, ValorTotal, MetodoPagamento, Loja_Id, Cliente_Pessoa_Cc FROM dbo.Venda")
        vendas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/vendas.html', dados_vendas=vendas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar vendas: {e}")
        return render_template('tabelas/vendas.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/vendedores')
def lista_vendedores():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/vendedores.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id, Pessoa_Cc, Nome, Email, DataNascimento, Morada, NumTelefone, Cargo_Id, NumVendas
            FROM Vendedor V
            JOIN Pessoa P ON P.Cc = V.Pessoa_Cc
        """)
        vendedores = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/vendedores.html', dados_vendedores=vendedores, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar vendedores: {e}")
        return render_template('tabelas/vendedores.html', erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("🚀 A iniciar servidor Flask...")
    print("📍 Aceda a: http://127.0.0.1:5000")
    app.run(debug=True)