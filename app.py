from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
    
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    """Página de registo - cria novo administrador na BD"""
    lojas = []
    fabricas = []
    
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
        
        if criar_novo_administrador(nome, email, password, tipo_admin, loja_id, fabrica_id):
            return redirect(url_for('login', success='Registo bem-sucedido! Faça login.'))
        else:
            flash('❌ Nome já existe ou erro ao criar conta!', 'error')
            return render_template('registo.html', lojas=lojas, fabricas=fabricas)
    
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

@app.route('/armazens')
def lista_armazens():
    """Lista todos os armazéns"""
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/armazens.html', registos=[], sucesso=False)
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id, Localizacao, Capacidade 
            FROM Armazem 
            ORDER BY Localizacao
        """)
        armazens = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/armazens.html', registos=armazens, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar armazéns: {e}")
        flash(f'Erro ao carregar armazéns: {str(e)}', 'error')
        return render_template('tabelas/armazens.html', registos=[], sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/armazem/novo', methods=['POST'])
def adicionar_armazem():
    """Insere novo armazém usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        localizacao = request.form.get('localizacao')
        capacidade = request.form.get('capacidade')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_armazens'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoArmazem (?, ?)}", 
                       (localizacao, capacidade))
        conn.commit()
        flash('✅ Armazém adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar armazém: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_armazens'))   

@app.route('/cargos')
def lista_cargos():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/cargos.html', registos=[], erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Descricao FROM dbo.Cargo ORDER BY Id")
        cargos = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/cargos.html', registos=cargos, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar cargos: {e}")
        return render_template('tabelas/cargos.html', registos=[], erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/cargo/novo', methods=['POST'])
def adicionar_cargo():
    """Insere novo cargo usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_cargos'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoCargo (?, ?)}", (nome, descricao))
        conn.commit()
        flash('✅ Cargo adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar cargo: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_cargos'))

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
            SELECT c.Pessoa_Cc, p.Nome, p.Email, p.DataNascimento , p.NumTelefone, c.Nif
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
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
        
    try:
        dados = {
            'cc': request.form.get('pessoa_cc'),
            'nome': request.form.get('nome'),
            'email': request.form.get('email'),
            'data_nasc': request.form.get('data_nasc'),
            'morada': request.form.get('morada'),
            'telemovel': request.form.get('telemovel'),
            'nif': request.form.get('nif')
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("{CALL dbo.InserirNovoCliente (?, ?, ?, ?, ?, ?, ?)}", 
                       (dados['cc'], dados['nome'], dados['email'], 
                        dados['data_nasc'], dados['morada'], dados['telemovel'], dados['nif']))
        conn.commit()
        flash('✅ Cliente e dados pessoais criados com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] 
        flash(f'❌ Erro: {error_msg}', 'error')
    finally:
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
            return render_template('tabelas/contratos_vendedor.html', registos=[], vendedores=[], empresas=[], erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cv.Vendedor_Id, p.Nome AS Vendedor, e.Nome AS Empresa, cv.DataIn, cv.DataOut
            FROM ContratoVendedor cv
            JOIN Vendedor v ON cv.Vendedor_Id = v.Id
            JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
            JOIN Empresa e ON cv.Empresa_Nif = e.Nif
            ORDER BY p.Nome
        """)
        contratos = cursor.fetchall()
        
        cursor.execute("""
            SELECT v.Id, p.Nome
            FROM Vendedor v
            JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
            ORDER BY p.Nome
        """)
        vendedores = cursor.fetchall()
        
        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()
        
        cursor.close()
        return render_template('tabelas/contratos_vendedor.html', 
                             registos=contratos,
                             vendedores=vendedores,
                             empresas=empresas,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar contratos vendedor: {e}")
        return render_template('tabelas/contratos_vendedor.html', registos=[], vendedores=[], empresas=[], erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/contrato_vendedor/novo', methods=['POST'])
def adicionar_contrato_vendedor():
    """Insere novo contrato de vendedor usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        vendedor_id = request.form.get('vendedor_id')
        empresa_nif = request.form.get('empresa_nif')
        data_in = request.form.get('data_in')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_contratos_vendedor'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoContratoVendedor (?, ?, ?)}", 
                       (vendedor_id, empresa_nif, data_in))
        conn.commit()
        flash('✅ Contrato de vendedor criado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao criar contrato: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_contratos_vendedor'))

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
    """Lista todas as empresas"""
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/empresas.html', registos=[], sucesso=False)
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Nif, Nome, Localizacao, NumTelefone, Email
            FROM Empresa
            ORDER BY Nome
        """)
        empresas = cursor.fetchall()
        cursor.close()
        return render_template('tabelas/empresas.html', registos=empresas, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar empresas: {e}")
        flash(f'Erro ao carregar empresas: {str(e)}', 'error')
        return render_template('tabelas/empresas.html', registos=[], sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/empresa/novo', methods=['POST'])
def adicionar_empresa():
    """Insere nova empresa usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        nif = request.form.get('nif')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        num_telefone = request.form.get('num_telefone')
        email = request.form.get('email')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_empresas'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovaEmpresa (?, ?, ?, ?, ?)}", 
                       (nif, nome, localizacao, num_telefone, email))
        conn.commit()
        flash('✅ Empresa adicionada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar empresa: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_empresas'))

@app.route('/fabricas')
def lista_fabricas():
    """Lista todas as fábricas"""
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/fabricas.html', registos=[], empresas=[], distribuidoras=[], sucesso=False)
        
        cursor = conn.cursor()
        
        # Buscar fábricas
        cursor.execute("""
            SELECT f.Id, f.Nome, f.Localizacao, e.Nome AS Empresa, d.Nome AS Distribuidora
            FROM Fabrica f
            JOIN Empresa e ON f.Empresa_Nif = e.Nif
            JOIN Distribuidora d ON f.Distribuidora_Id = d.Id
            ORDER BY f.Nome
        """)
        fabricas = cursor.fetchall()
        
        # Buscar empresas para o modal
        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()
        
        # Buscar distribuidoras para o modal
        cursor.execute("SELECT Id, Nome FROM Distribuidora ORDER BY Nome")
        distribuidoras = cursor.fetchall()
        
        cursor.close()
        return render_template('tabelas/fabricas.html', 
                             registos=fabricas,
                             empresas=empresas,
                             distribuidoras=distribuidoras,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar fabricas: {e}")
        flash(f'Erro ao carregar fábricas: {str(e)}', 'error')
        return render_template('tabelas/fabricas.html', registos=[], empresas=[], distribuidoras=[], sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/fabrica/novo', methods=['POST'])
def adicionar_fabrica():
    """Insere nova fábrica usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        empresa_nif = request.form.get('empresa_nif')
        distribuidora_id = request.form.get('distribuidora_id')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_fabricas'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovaFabrica (?, ?, ?, ?)}", 
                       (nome, localizacao, empresa_nif, distribuidora_id))
        conn.commit()
        flash('✅ Fábrica adicionada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar fábrica: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_fabricas'))

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
            return render_template('tabelas/funcionarios.html', registos=[], pessoas=[], cargos=[], empresas=[], fabricas=[], erro="Erro de conexão", sucesso=False)
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT f.Pessoa_Cc, p.Nome, c.Nome AS Cargo, 
                   e.Nome AS Empresa,
                   COALESCE(fab.Nome, 'N/A') AS Fabrica
            FROM Funcionario f
            JOIN Pessoa p ON f.Pessoa_Cc = p.Cc
            JOIN Cargo c ON f.Cargo_Id = c.Id
            JOIN Empresa e ON f.Empresa_Nif = e.Nif
            LEFT JOIN Fabrica fab ON f.Fabrica_Id = fab.Id
            ORDER BY p.Nome
        """)
        funcionarios = cursor.fetchall()
        
        cursor.execute("""
            SELECT p.Cc, p.Nome, p.Email
            FROM Pessoa p
            WHERE p.Cc NOT IN (SELECT Pessoa_Cc FROM Funcionario)
            ORDER BY p.Nome
        """)
        pessoas = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Cargo ORDER BY Nome")
        cargos = cursor.fetchall()
        
        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Fabrica ORDER BY Nome")
        fabricas = cursor.fetchall()
        
        cursor.close()
        return render_template('tabelas/funcionarios.html', 
                             registos=funcionarios, 
                             pessoas=pessoas,
                             cargos=cargos,
                             empresas=empresas,
                             fabricas=fabricas,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar funcionarios: {e}")
        return render_template('tabelas/funcionarios.html', registos=[], pessoas=[], cargos=[], empresas=[], fabricas=[], erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/funcionario/novo', methods=['POST'])
def adicionar_funcionario():
    """Insere novo funcionário usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        pessoa_cc = request.form.get('pessoa_cc')
        cargo_id = request.form.get('cargo_id')
        empresa_nif = request.form.get('empresa_nif')
        fabrica_id = request.form.get('fabrica_id') if request.form.get('fabrica_id') else None

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_funcionarios'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovoFuncionario (?, ?, ?, ?)}", 
                       (pessoa_cc, cargo_id, empresa_nif, fabrica_id))
        conn.commit()
        flash('✅ Funcionário adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar funcionário: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_funcionarios'))

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

@app.route('/lojas')
def lista_lojas():
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/lojas.html', registos=[], armazens=[], sucesso=False)
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.Id, l.Nome, l.Localizacao, a.Localizacao AS Armazem
            FROM dbo.Loja l
            LEFT JOIN dbo.Armazem a ON l.Armazem_Id = a.Id
            ORDER BY l.Nome
        """)
        lojas = cursor.fetchall()
        
        cursor.execute("SELECT Id, Localizacao FROM dbo.Armazem ORDER BY Localizacao")
        armazens = cursor.fetchall()
        
        cursor.close()
        return render_template('tabelas/lojas.html', registos=lojas, armazens=armazens, sucesso=True)
        
    except Exception as e:
        print(f"Erro ao listar lojas: {e}")
        flash(f'Erro ao carregar lojas: {str(e)}', 'error')
        return render_template('tabelas/lojas.html', registos=[], armazens=[], sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/loja/nova', methods=['POST'])
def adicionar_loja():
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        armazem_id = request.form.get('armazem_id')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_lojas'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovaLoja (?, ?, ?)}", (nome, localizacao, armazem_id))
        conn.commit()
        cursor.close()
        flash('✅ Loja adicionada com sucesso!', 'success')
        
    except Exception as e:
        print(f"Erro ao adicionar loja: {e}")
        flash(f'❌ Erro ao adicionar loja: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_lojas'))

@app.route('/maquinas')
def lista_maquinas():
    """Lista todas as máquinas"""
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/maquinas.html', registos=[], fabricas=[], sucesso=False)
        
        cursor = conn.cursor()
        
        # Buscar máquinas
        cursor.execute("""
            SELECT m.Id, m.Descricao, m.Tipo, f.Nome AS Fabrica
            FROM Maquina m
            JOIN Fabrica f ON m.Fabrica_Id = f.Id
            ORDER BY m.Descricao
        """)
        maquinas = cursor.fetchall()
        
        # Buscar fábricas para o modal
        cursor.execute("SELECT Id, Nome FROM Fabrica ORDER BY Nome")
        fabricas = cursor.fetchall()
        
        cursor.close()
        return render_template('tabelas/maquinas.html', 
                             registos=maquinas,
                             fabricas=fabricas,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar maquinas: {e}")
        flash(f'Erro ao carregar máquinas: {str(e)}', 'error')
        return render_template('tabelas/maquinas.html', registos=[], fabricas=[], sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/maquina/novo', methods=['POST'])
def adicionar_maquina():
    """Insere nova máquina usando Stored Procedure"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    try:
        descricao = request.form.get('descricao')
        tipo = request.form.get('tipo')
        fabrica_id = request.form.get('fabrica_id')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_maquinas'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovaMaquina (?, ?, ?)}", 
                       (descricao, tipo, fabrica_id))
        conn.commit()
        flash('✅ Máquina adicionada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'❌ Erro ao adicionar máquina: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_maquinas'))

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

@app.route('/produtos')
def lista_produtos():
    """Lista todos os produtos com dados para o modal"""
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/produtos.html', 
                                 registos=[], 
                                 maquinas=[], 
                                 distribuidoras=[], 
                                 sucesso=False)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Nome, Referencia, Descricao, Preco, Maquina_Id, Distribuidora_Id 
            FROM Produto
            ORDER BY Nome
        """) 
        
        produtos = cursor.fetchall()
        
        cursor.execute("SELECT Id, Descricao FROM Maquina ORDER BY Descricao") 
        maquinas = cursor.fetchall()

        cursor.execute("SELECT Id, Nome FROM Distribuidora ORDER BY Nome")
        distribuidoras = cursor.fetchall()
        
        cursor.close()
        return render_template('tabelas/produtos.html', 
                             registos=produtos,
                             maquinas=maquinas,            
                             distribuidoras=distribuidoras,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        flash(f'Erro ao carregar produtos: {str(e)}', 'error')
        return render_template('tabelas/produtos.html', 
                             registos=[], 
                             maquinas=[], 
                             distribuidoras=[], 
                             sucesso=False)
    finally:
        if conn:
            conn.close()

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
    """
    Lista as vendas. Filtra automaticamente por Loja_Id se o admin for 'Loja'.
    Se for 'Geral', lista todas as vendas.
    """
    if 'admin_logado' not in session: 
        return redirect(url_for('login'))
    
    tipo_admin = session.get('tipo_admin')
    loja_id_sessao = session.get('loja_id') 

    if tipo_admin == 'Loja' and loja_id_sessao is not None:
        parametro_loja_id = loja_id_sessao
    else:
        parametro_loja_id = None 

    conn = None
    sucesso = False
    erro = None
    
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/vendas.html', erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.ObterVendasPorLoja (?)}", parametro_loja_id)
        vendas = cursor.fetchall()

        cursor.execute("SELECT Referencia, Nome FROM Produto ORDER BY Nome")
        produtos = cursor.fetchall()

        lojas = []
        if session.get('tipo_admin') == 'Geral':
            cursor.execute("SELECT Id, Nome FROM Loja")
        lojas = cursor.fetchall()
        
        sucesso = True
    except Exception as e:
        erro = f"Erro ao listar vendas: {e}"
        print(f"❌ {erro}")
        vendas = []
    finally:
        if conn:
            conn.close()
    return render_template('tabelas/vendas.html', 
                            dados_vendas=vendas, 
                            dados_produtos=produtos,
                            dados_lojas=lojas,
                            sucesso=sucesso, 
                            erro=erro,
                            filtro_ativo=True if parametro_loja_id is not None else False)

@app.route('/venda/nova', methods=['POST'])
def adicionar_venda():
    data = request.get_json()
    
    itens_para_sql = [(item['ref'], int(item['qtd'])) for item in data['itens']]
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        sql = "{CALL dbo.RegistarVendaCompleta (?, ?, ?, ?)}"
        params = (
            data['loja_id'],
            data['nif'] if data['nif'] else None,
            data['pagamento'],
            itens_para_sql
        )
        
        cursor.execute(sql, params)
        conn.commit()
        
        return jsonify({'sucesso': True, 'mensagem': 'Venda registada com sucesso!'})
    except Exception as e:
        error_msg = str(e).split(']')[-1]
        return jsonify({'sucesso': False, 'erro': error_msg})
    finally:
        conn.close()

@app.route('/api/venda/<int:venda_id>/itens')
def obter_itens_venda(venda_id):
    """API que retorna os itens de uma venda específica em formato JSON"""
    if 'admin_logado' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401

    conn = get_db_connection()
    itens = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT P.Nome, I.Quantidade, I.Preco, (I.Quantidade * I.Preco) as Total
            FROM Item I
            JOIN Produto P ON I.Produto_Referencia = P.Referencia
            WHERE I.Venda_Id = ?
        """, (venda_id,))

        #TODO: Mudar isto para uma SP

        for row in cursor.fetchall():
            itens.append({
                'produto': row[0],
                'quantidade': row[1],
                'preco_unit': row[2],
                'subtotal': row[3]
            })
            
        return jsonify(itens)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()

@app.route('/vendedores')
def lista_vendedores():
    """Lista todos os vendedores com opção de adicionar"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/vendedores.html', registos=[], cargos=[], empresas=[])
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.Pessoa_Cc, p.Nome, c.Nome AS Cargo, v.NumVendas, p.NumTelefone
            FROM Vendedor v
            JOIN Pessoa p ON v.Pessoa_Cc = p.Cc
            JOIN Cargo c ON v.Cargo_Id = c.Id
            ORDER BY p.Nome
        """)
        registos = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Cargo ORDER BY Nome")
        cargos = cursor.fetchall()

        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()

        return render_template('tabelas/vendedores.html', registos=registos, cargos=cargos, empresas=empresas)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/vendedores.html', registos=[], cargos=[], empresas=[])
    finally:
        conn.close()

@app.route('/vendedor/novo', methods=['POST'])
def adicionar_vendedor():
    """Insere novo vendedor e contrato usando Stored Procedure completa"""
    if 'admin_logado' not in session:
        return redirect(url_for('login'))
    
    conn = None
    try:
        cc = request.form.get('pessoa_cc')
        nome = request.form.get('nome')
        email = request.form.get('email') or None
        data_nasc = request.form.get('data_nasc') or None
        morada = request.form.get('morada') or None
        telemovel = request.form.get('telemovel') or None

        cargo_id = request.form.get('cargo_id')
        empresa_nif = request.form.get('empresa_nif')
        data_fim = request.form.get('data_fim') or None

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_vendedores'))

        cursor = conn.cursor()

        sql = "{CALL dbo.InserirNovoVendedor (?, ?, ?, ?, ?, ?, ?, ?, ?)}"
        params = (cc, nome, email, data_nasc, morada, telemovel, cargo_id, empresa_nif, data_fim)
        
        cursor.execute(sql, params)
        conn.commit()
        
        flash('✅ Vendedor e Contrato registados com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao adicionar vendedor: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_vendedores'))

if __name__ == '__main__':
    print("🚀 A iniciar servidor Flask...")
    print("📍 Aceda a: http://127.0.0.1:5000")
    app.run(debug=True)