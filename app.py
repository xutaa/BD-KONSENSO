from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'bd_konsenso_secret_key_2024'

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def validar_administrador(nome, password):
    """Verifica login na tabela Administradores e retorna dados do admin"""
    conn = get_db_connection()
    if not conn: 
        print("❌ Erro: Sem conexão à base de dados")
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Nome, Tipo_Admin, Loja_Id, Fabrica_Id 
            FROM Administradores 
            WHERE Nome = ? AND Password = ?
        """, (nome, password))
        admin = cursor.fetchone()
        if admin:
            print(f"✅ Login bem-sucedido: {nome} ({admin[1]})")
            return {
                'nome': admin[0],
                'tipo_admin': admin[1],
                'loja_id': admin[2],
                'fabrica_id': admin[3]
            }
        else:
            print(f"❌ Login falhou: {nome}")
            return None
    except Exception as e:
        print(f"❌ Erro ao validar login: {e}")
        return None
    finally:
        conn.close()

def criar_novo_administrador(nome, email, password, tipo_admin, loja_id=None, fabrica_id=None):
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
        
        cursor.execute("""
            INSERT INTO Administradores (Nome, Email, Password, Tipo_Admin, Loja_Id, Fabrica_Id) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, email, password, tipo_admin, loja_id, fabrica_id))
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
            flash('❌ Preencha todos os campos!', 'error')
            return render_template('login.html')
        
        admin_data = validar_administrador(nome, password)
        if admin_data:
            session['admin_logado'] = admin_data['nome']
            session['tipo_admin'] = admin_data['tipo_admin']
            session['loja_id'] = admin_data['loja_id']
            session['fabrica_id'] = admin_data['fabrica_id']
            print(f"✅ Sessão criada para {nome} ({admin_data['tipo_admin']})")
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Nome ou password incorretos!', 'error')
            return render_template('login.html')
    
    # GET request - mostra formulário
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    """Página de registo - cria novo administrador na BD"""
    lojas = []
    fabricas = []
    
    # Buscar Lojas e Fábricas para os dropdowns
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Localizacao FROM Loja ORDER BY Localizacao")
            lojas = cursor.fetchall()
            cursor.execute("SELECT Id, Localizacao FROM Fabrica ORDER BY Localizacao")
            fabricas = cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao buscar lojas/fábricas: {e}")
        finally:
            conn.close()
    
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        tipo_admin = request.form.get('tipo_admin', 'Geral')
        loja_id = request.form.get('loja_id') if tipo_admin == 'Loja' else None
        fabrica_id = request.form.get('fabrica_id') if tipo_admin == 'Fabrica' else None
        
        # Validações
        if not nome or not email or not password:
            flash('❌ Preencha todos os campos obrigatórios!', 'error')
            return render_template('registo.html', lojas=lojas, fabricas=fabricas)
        
        if password != confirm_password:
            flash('❌ As passwords não coincidem!', 'error')
            return render_template('registo.html', lojas=lojas, fabricas=fabricas)
        
        if len(password) < 4:
            flash('❌ Password deve ter pelo menos 4 caracteres!', 'error')
            return render_template('registo.html', lojas=lojas, fabricas=fabricas)
        
        # Tenta criar na base de dados
        if criar_novo_administrador(nome, email, password, tipo_admin, loja_id, fabrica_id):
            return redirect(url_for('login', success='Registo bem-sucedido! Faça login.'))
        else:
            flash('❌ Nome já existe ou erro ao criar conta!', 'error')
            return render_template('registo.html', lojas=lojas, fabricas=fabricas)
    
    # GET request - mostra formulário
    return render_template('registo.html', lojas=lojas, fabricas=fabricas)

@app.route('/logout')
def logout():
    """Remove sessão e redireciona para login"""
    nome = session.get('admin_logado', 'Desconhecido')
    session.pop('admin_logado', None)
    session.pop('tipo_admin', None)
    session.pop('loja_id', None)
    session.pop('fabrica_id', None)
    print(f"👋 Logout: {nome}")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Página principal - só acessível após login"""
    if 'admin_logado' not in session:
        print("⚠️ Tentativa de acesso sem login")
        return redirect(url_for('login'))
    
    tipo_admin = session.get('tipo_admin', 'Geral')
    
    roadmap_status = {
        "Fase 1: Leitura (Listagem)": "✅ Concluída",
        "Fase 2: Inserção": "Produtos Done, Outros a Fazer",
        "Fase 3: Edição e Remoção": "Não Iniciada",
        "Fase 4: Relatórios": "Não Iniciada",
    }
    
    # Definir permissões por tipo
    permissoes = {
        'Geral': {
            'gestao_principal': True,
            'pessoas_clientes': True,
            'empresas': True,
            'infraestrutura': True,
            'producao': True
        },
        'Loja': {
            'gestao_principal': True,  # Produtos, Vendas, Stock, Itens
            'pessoas_clientes': True,  # Clientes, Vendedores
            'empresas': False,
            'infraestrutura': False,
            'producao': False
        },
        'Fabrica': {
            'gestao_principal': True,  # Produtos, Stock
            'pessoas_clientes': False,
            'empresas': True,  # Fornecedores
            'infraestrutura': True,  # Armazéns, Máquinas
            'producao': True  # Matérias-Primas
        }
    }
    
    return render_template('dashboard.html', 
                         roadmap=roadmap_status, 
                         usuario=session['admin_logado'],
                         tipo_admin=tipo_admin,
                         permissoes=permissoes.get(tipo_admin, permissoes['Geral']))

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
    """Lista todos os clientes com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/clientes.html', registos=[], pessoas=[])
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.Pessoa_Cc, p.Nome, p.Email, p.NumTelefone, c.Nif
            FROM Cliente c
            JOIN Pessoa p ON c.Pessoa_Cc = p.Cc
            ORDER BY p.Nome
        """)
        registos = cursor.fetchall()
        
        cursor.execute("""
            SELECT p.Cc, p.Nome, p.Email
            FROM Pessoa p
            WHERE p.Cc NOT IN (SELECT Pessoa_Cc FROM Cliente)
            ORDER BY p.Nome
        """)
        pessoas = cursor.fetchall()
        
        return render_template('tabelas/clientes.html', registos=registos, pessoas=pessoas)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/clientes.html', registos=[], pessoas=[])
    finally:
        conn.close()

@app.route('/cliente/novo', methods=['POST'])
def adicionar_cliente():
    """Insere novo cliente usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        pessoa_cc = request.form.get('pessoa_cc')
        nif = request.form.get('nif')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_clientes'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoCliente (?, ?)}", (pessoa_cc, nif))
        conn.commit()
        flash('✅ Cliente adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar cliente: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_clientes'))

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
    """Lista todos os fornecedores com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/fornecedores.html', registos=[], empresas=[])
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.Id, f.Nome, e.Nome AS Empresa, e.Nif
            FROM Fornecedor f
            JOIN Empresa e ON f.Empresa_Nif = e.Nif
            ORDER BY f.Nome
        """)
        registos = cursor.fetchall()
        
        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()
        
        return render_template('tabelas/fornecedores.html', registos=registos, empresas=empresas)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/fornecedores.html', registos=[], empresas=[])
    finally:
        conn.close()

@app.route('/fornecedor/novo', methods=['POST'])
def adicionar_fornecedor():
    """Insere novo fornecedor usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        nome = request.form.get('nome')
        empresa_nif = request.form.get('empresa_nif')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_fornecedores'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoFornecedor (?, ?)}", (nome, empresa_nif))
        conn.commit()
        flash('✅ Fornecedor adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar fornecedor: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_fornecedores'))

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
    """Lista todos os itens de venda com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/itens.html', registos=[], vendas=[], produtos=[])
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.Venda_Id, p.Nome, i.Quantidade, i.Preco, (i.Quantidade * i.Preco) AS Total
            FROM Item i
            JOIN Produto p ON i.Produto_Referencia = p.Referencia
            ORDER BY i.Venda_Id DESC
        """)
        registos = cursor.fetchall()
        
        cursor.execute("SELECT Id FROM Venda ORDER BY Id DESC")
        vendas = cursor.fetchall()
        
        cursor.execute("SELECT Referencia, Nome, Preco FROM Produto ORDER BY Nome")
        produtos = cursor.fetchall()
        
        return render_template('tabelas/itens.html', registos=registos, vendas=vendas, produtos=produtos)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/itens.html', registos=[], vendas=[], produtos=[])
    finally:
        conn.close()

@app.route('/item/novo', methods=['POST'])
def adicionar_item():
    """Insere novo item de venda usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        venda_id = request.form.get('venda_id')
        produto_ref = request.form.get('produto_referencia')
        quantidade = request.form.get('quantidade')
        preco = request.form.get('preco')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_itens'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoItem (?, ?, ?, ?)}", (venda_id, produto_ref, quantidade, preco))
        conn.commit()
        flash('✅ Item adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar item: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_itens'))

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
    """Lista todas as matérias-primas com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/materias_primas.html', registos=[], fornecedores=[])
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mp.Referencia, mp.Descricao, f.Nome AS Fornecedor
            FROM MateriaPrima mp
            JOIN Fornecedor f ON mp.Fornecedor_Id = f.Id
            ORDER BY mp.Referencia
        """)
        registos = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Fornecedor ORDER BY Nome")
        fornecedores = cursor.fetchall()
        
        return render_template('tabelas/materias_primas.html', registos=registos, fornecedores=fornecedores)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/materias_primas.html', registos=[], fornecedores=[])
    finally:
        conn.close()

@app.route('/materia_prima/nova', methods=['POST'])
def adicionar_materia_prima():
    """Insere nova matéria-prima usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        referencia = request.form.get('referencia')
        descricao = request.form.get('descricao')
        fornecedor_id = request.form.get('fornecedor_id')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_materias_primas'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovaMateriaPrima (?, ?, ?)}", (referencia, descricao, fornecedor_id))
        conn.commit()
        flash('✅ Matéria-prima adicionada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar matéria-prima: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_materias_primas'))

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
    """Lista todo o stock com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/stock.html', registos=[], produtos=[], armazens=[])
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.Produto_Referencia, p.Nome, a.Localizacao, s.Quantidade, s.UltimoMov
            FROM Stock s
            JOIN Produto p ON s.Produto_Referencia = p.Referencia
            JOIN Armazem a ON s.Armazem_Id = a.Id
            ORDER BY s.UltimoMov DESC
        """)
        registos = cursor.fetchall()
        
        cursor.execute("SELECT Referencia, Nome FROM Produto ORDER BY Nome")
        produtos = cursor.fetchall()
        
        cursor.execute("SELECT Id, Localizacao FROM Armazem ORDER BY Localizacao")
        armazens = cursor.fetchall()
        
        return render_template('tabelas/stock.html', registos=registos, produtos=produtos, armazens=armazens)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/stock.html', registos=[], produtos=[], armazens=[])
    finally:
        conn.close()

@app.route('/stock/novo', methods=['POST'])
def adicionar_stock():
    """Insere nova entrada de stock usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        produto_ref = request.form.get('produto_referencia')
        armazem_id = request.form.get('armazem_id')
        quantidade = request.form.get('quantidade')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_stock'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoStock (?, ?, ?)}", (produto_ref, armazem_id, quantidade))
        conn.commit()
        flash('✅ Stock atualizado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar stock: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_stock'))

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
    """Lista todos os vendedores com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/vendedores.html', registos=[], pessoas=[], cargos=[])
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.Pessoa_Cc, p.Nome, c.Nome AS Cargo, v.NumVendas
            FROM Vendedor v
            JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
            JOIN Cargo c ON v.Cargo_Id = c.Id
            ORDER BY v.NumVendas DESC
        """)
        registos = cursor.fetchall()
        
        cursor.execute("""
            SELECT p.Cc, p.Nome, p.Email
            FROM Pessoa p
            WHERE p.Cc NOT IN (SELECT Pessoa_Cc FROM Vendedor)
            ORDER BY p.Nome
        """)
        pessoas = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Cargo ORDER BY Nome")
        cargos = cursor.fetchall()
        
        return render_template('tabelas/vendedores.html', registos=registos, pessoas=pessoas, cargos=cargos)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/vendedores.html', registos=[], pessoas=[], cargos=[])
    finally:
        conn.close()

@app.route('/vendedor/novo', methods=['POST'])
def adicionar_vendedor():
    """Insere novo vendedor usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        pessoa_cc = request.form.get('pessoa_cc')
        cargo_id = request.form.get('cargo_id')
        num_vendas = request.form.get('num_vendas', 0)

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_vendedores'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoVendedor (?, ?, ?)}", (pessoa_cc, cargo_id, num_vendas))
        conn.commit()
        flash('✅ Vendedor adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar vendedor: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_vendedores'))


if __name__ == '__main__':
    print("🚀 A iniciar servidor Flask...")
    print("📍 Aceda a: http://127.0.0.1:5000")
    app.run(debug=True)