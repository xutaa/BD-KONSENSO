from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_db_connection
from utils import login_required, admin_tipo_required, execute_query, execute_sp, paginate

app = Flask(__name__)
app.secret_key = 'bd_konsenso_secret_key_2024'

# --- FUNÇÕES DE AUTENTICAÇÃO ---

def validar_administrador(nome, password):
    """Valida as credenciais comparando o Hash da password no SQL"""
    conn = get_db_connection()
    if not conn:
        print("❌ Erro: Sem conexão à base de dados")
        return None
    try:
        cursor = conn.cursor()
        query = """
            SELECT Nome, Tipo_Admin, Loja_Id, Fabrica_Id 
            FROM Administradores 
            WHERE Nome = ? AND Password = dbo.HashPassword(?)
        """
        cursor.execute(query, (nome, password))
        row = cursor.fetchone()
        
        if row:
            tipo_admin = str(row[1]).strip() if row[1] else 'Geral'
            print(f"✅ Login bem-sucedido: {nome} (Tipo: '{tipo_admin}', Loja: {row[2]}, Fabrica: {row[3]})")
            return {
                'nome': row[0],
                'tipo_admin': tipo_admin,
                'loja_id': row[2],
                'fabrica_id': row[3]
            }
        else:
            print(f"❌ Login falhou: {nome}")
            return None
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return None
    finally:
        conn.close()

def criar_novo_administrador(nome, email, password, tipo_admin, loja_id=None, fabrica_id=None):
    """Verifica existência e insere novo admin com password encriptada"""
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
        
        query = """
            INSERT INTO Administradores (Nome, Email, Password, Tipo_Admin, Loja_Id, Fabrica_Id)
            VALUES (?, ?, dbo.HashPassword(?), ?, ?, ?)
        """
        cursor.execute(query, (nome, email, password, tipo_admin, loja_id, fabrica_id))
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
    """Gere o acesso ao sistema"""
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
            
            print(f"✅ LOGIN - Nome: {admin_data['nome']}, Tipo: {admin_data['tipo_admin']}, Loja: {admin_data['loja_id']}, Fábrica: {admin_data['fabrica_id']}")
            
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Nome ou password incorretos!', 'error')
            
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    """Gere a criação de novas contas"""
    lojas = []
    fabricas = []
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            lojas = cursor.execute("SELECT Id, Localizacao FROM Loja ORDER BY Localizacao").fetchall()
            fabricas = cursor.execute("SELECT Id, Localizacao FROM Fabrica ORDER BY Localizacao").fetchall()
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
        
        if not nome or not email or not password:
            flash('❌ Preencha todos os campos obrigatórios!', 'error')
        elif password != confirm_password:
            flash('❌ As passwords não coincidem!', 'error')
        elif len(password) < 4:
            flash('❌ Password demasiado curta!', 'error')
        else:
            if criar_novo_administrador(nome, email, password, tipo_admin, loja_id, fabrica_id):
                return redirect(url_for('login', success='Registo bem-sucedido! Faça login.'))
            else:
                flash('❌ Erro: Nome de utilizador já existe ou falha na BD.', 'error')
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
@login_required
def dashboard():
    """Página principal - só acessível após login"""
    
    tipo_admin = session.get('tipo_admin', 'Geral')
    

    
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

    # Fetch Dashboard Stats usando View (1 query em vez de 4)
    stats = {
        'produtos': 0,
        'clientes': 0,
        'vendas': 0,
        'funcionarios': 0
    }
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Usa a View vw_DashboardStats para obter tudo numa única query
            cursor.execute("SELECT * FROM vw_DashboardStats")
            row = cursor.fetchone()
            if row:
                stats['produtos'] = row[0]
                stats['clientes'] = row[1]
                stats['vendas'] = row[2]
                stats['funcionarios'] = row[3]
        except Exception as e:
            print(f"Erro ao carregar stats do dashboard: {e}")
            # Fallback para queries individuais se a View não existir
            try:
                stats['produtos'] = cursor.execute("SELECT COUNT(*) FROM Produto").fetchone()[0]
                stats['clientes'] = cursor.execute("SELECT COUNT(*) FROM Cliente").fetchone()[0]
                stats['vendas'] = cursor.execute("SELECT COUNT(*) FROM Venda").fetchone()[0]
                stats['funcionarios'] = cursor.execute("SELECT COUNT(*) FROM Funcionario").fetchone()[0]
            except:
                pass
        finally:
            conn.close()
    
    return render_template('dashboard.html', 
                         usuario=session['admin_logado'],
                         tipo_admin=tipo_admin,
                         permissoes=permissoes.get(tipo_admin, permissoes['Geral']),
                         stats=stats)

@app.route('/armazens')
@login_required
def lista_armazens():
    """Lista todos os armazéns com informação de ocupação e paginação"""
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/armazens.html', registos=[], pagination=None, sucesso=False)
        
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            cursor.execute("""
                SELECT v.ArmazemId, v.Localizacao, v.Capacidade, v.StockAtual, v.EspacoLivre, v.PercentagemOcupada
                FROM vw_StockPorArmazem v
                INNER JOIN DistribuidoraArmazem da ON v.ArmazemId = da.Armazem_Id
                INNER JOIN Fabrica f ON da.Distribuidora_Id = f.Distribuidora_Id
                WHERE f.Id = ?
                ORDER BY v.Localizacao
            """, (fabrica_id,))
            armazens = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT ArmazemId, Localizacao, Capacidade, StockAtual, EspacoLivre, PercentagemOcupada
                FROM vw_StockPorArmazem 
                ORDER BY Localizacao
            """)
            armazens = cursor.fetchall()
        
        cursor.close()
        
        # Aplicar paginação
        pagination = paginate(armazens, page, per_page)
        
        return render_template('tabelas/armazens.html', registos=pagination['items'], pagination=pagination, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar armazéns: {e}")
        try:
            cursor.execute("SELECT Id, Localizacao, Capacidade FROM Armazem ORDER BY Localizacao")
            armazens = cursor.fetchall()
            pagination = paginate(armazens, page, per_page)
            return render_template('tabelas/armazens.html', registos=pagination['items'], pagination=pagination, sucesso=True)
        except:
            flash(f'Erro ao carregar armazéns: {str(e)}', 'error')
            return render_template('tabelas/armazens.html', registos=[], pagination=None, sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/armazem/novo', methods=['POST'])
@login_required
def adicionar_armazem():
    """Insere novo armazém usando Stored Procedure"""
    
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

@app.route('/armazem/remover/<int:id>', methods=['POST'])
@login_required
def remover_armazem(id):
    """Remove um armazém"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_armazens'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverArmazem (?)}", (id,))
        conn.commit()
        flash('✅ Armazém removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_armazens'))

@app.route('/cargos')
@login_required
def lista_cargos():
    """Lista todos os cargos com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/cargos.html', registos=[], pagination=None, erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nome, Descricao FROM dbo.Cargo ORDER BY Id")
        cargos = cursor.fetchall()
        cursor.close()
        
        pagination = paginate(cargos, page, per_page)
        return render_template('tabelas/cargos.html', registos=pagination['items'], pagination=pagination, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar cargos: {e}")
        return render_template('tabelas/cargos.html', registos=[], pagination=None, erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/cargo/novo', methods=['POST'])
@login_required
def adicionar_cargo():
    """Insere novo cargo usando Stored Procedure"""
    
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

@app.route('/cargo/remover/<int:id>', methods=['POST'])
@login_required
def remover_cargo(id):
    """Remove um cargo"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_cargos'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverCargo (?)}", (id,))
        conn.commit()
        flash('✅ Cargo removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_cargos'))

@app.route('/clientes')
@login_required
def lista_clientes():
    """Lista todos os clientes com opção de adicionar e paginação"""
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/clientes.html', registos=[], pessoas=[], pagination=None)
    
    try:
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Loja' and session.get('loja_id'):
            loja_id = session.get('loja_id')
            cursor.execute("""
                SELECT DISTINCT c.Pessoa_Cc, p.Nome, p.Email, p.DataNascimento, p.NumTelefone, c.Nif
                FROM Cliente c
                INNER JOIN Pessoa p ON c.Pessoa_Cc = p.Cc
                INNER JOIN Venda v ON c.Nif = v.Cliente_Nif
                WHERE v.Loja_Id = ?
                ORDER BY p.Nome
            """, (loja_id,))
            registos = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM vw_Clientes ORDER BY Nome")
            registos = cursor.fetchall()
        
        cursor.execute("""
            SELECT p.Cc, p.Nome, p.Email
            FROM Pessoa p
            WHERE p.Cc NOT IN (SELECT Pessoa_Cc FROM Cliente)
            ORDER BY p.Nome
        """)
        pessoas = cursor.fetchall()
        
        # Aplicar paginação
        pagination = paginate(registos, page, per_page)
        
        return render_template('tabelas/clientes.html', registos=pagination['items'], pessoas=pessoas, pagination=pagination)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/clientes.html', registos=[], pessoas=[], pagination=None)
    finally:
        conn.close()

@app.route('/cliente/novo', methods=['POST'])
@login_required
def adicionar_cliente():
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

@app.route('/cliente/remover/<path:cc>', methods=['POST'])
@login_required
def remover_cliente(cc):
    """Remove um cliente"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_clientes'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverCliente (?)}", (cc,))
        conn.commit()
        flash('✅ Cliente removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_clientes'))

@app.route('/contratos_vendedor')
@login_required
def lista_contratos_vendedor():
    """Lista contratos de vendedor com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/contratos_vendedor.html', registos=[], vendedores=[], empresas=[], pagination=None, erro="Erro de conexão", sucesso=False)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM vw_ContratosVendedor ORDER BY Vendedor")
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
        
        pagination = paginate(contratos, page, per_page)
        return render_template('tabelas/contratos_vendedor.html', 
                             registos=pagination['items'],
                             vendedores=vendedores,
                             empresas=empresas,
                             pagination=pagination,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar contratos vendedor: {e}")
        return render_template('tabelas/contratos_vendedor.html', registos=[], vendedores=[], empresas=[], pagination=None, erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/contrato_vendedor/novo', methods=['POST'])
@login_required
def adicionar_contrato_vendedor():
    """Insere novo contrato de vendedor usando Stored Procedure"""
    
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

@app.route('/contrato_vendedor/remover/<int:vendedor_id>/<path:empresa_nif>', methods=['POST'])
@login_required
def remover_contrato_vendedor(vendedor_id, empresa_nif):
    """Remove um contrato de vendedor"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_contratos_vendedor'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverContratoVendedor (?, ?)}", (vendedor_id, empresa_nif))
        conn.commit()
        flash('✅ Contrato de vendedor removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_contratos_vendedor'))

@app.route('/distribuidoras')
@login_required
def lista_distribuidoras():
    """Lista distribuidoras com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/distribuidoras.html', registos=[], pagination=None, sucesso=False)
        
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            cursor.execute("""
                SELECT d.Id, d.Nome, d.Localizacao
                FROM Distribuidora d
                INNER JOIN Fabrica f ON f.Distribuidora_Id = d.Id
                WHERE f.Id = ?
            """, (fabrica_id,))
            distribuidoras = cursor.fetchall()
        else:
            cursor.execute("SELECT Id, Nome, Localizacao FROM dbo.Distribuidora ORDER BY Nome")
            distribuidoras = cursor.fetchall()
        
        cursor.close()
        
        pagination = paginate(distribuidoras, page, per_page)
        return render_template('tabelas/distribuidoras.html', registos=pagination['items'], pagination=pagination, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar distribuidoras: {e}")
        flash(f'Erro ao carregar distribuidoras: {str(e)}', 'error')
        return render_template('tabelas/distribuidoras.html', registos=[], pagination=None, sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/distribuidora/nova', methods=['POST'])
@login_required
def adicionar_distribuidora():
    """Insere nova distribuidora usando Stored Procedure"""
    
    try:
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_distribuidoras'))

        cursor = conn.cursor()
        cursor.execute("{CALL dbo.InserirNovaDistribuidora (?, ?)}", (nome, localizacao))
        conn.commit()
        flash('✅ Distribuidora adicionada com sucesso!', 'success')
    except Exception as e:
        flash(f'❌ Erro ao adicionar distribuidora: {str(e)}', 'error')
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('lista_distribuidoras'))

@app.route('/distribuidora/remover/<int:id>', methods=['POST'])
@login_required
def remover_distribuidora(id):
    """Remove uma distribuidora"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_distribuidoras'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverDistribuidora (?)}", (id,))
        conn.commit()
        flash('✅ Distribuidora removida com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_distribuidoras'))

@app.route('/distribuidoras_armazem')
@login_required
def lista_distribuidoras_armazem():
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
@login_required
def lista_empresas():
    """Lista todas as empresas com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/empresas.html', registos=[], pagination=None, sucesso=False)
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Nif, Nome, Localizacao, NumTelefone, Email
            FROM Empresa
            ORDER BY Nome
        """)
        empresas = cursor.fetchall()
        cursor.close()
        
        pagination = paginate(empresas, page, per_page)
        return render_template('tabelas/empresas.html', registos=pagination['items'], pagination=pagination, sucesso=True)
    except Exception as e:
        print(f"Erro ao listar empresas: {e}")
        flash(f'Erro ao carregar empresas: {str(e)}', 'error')
        return render_template('tabelas/empresas.html', registos=[], pagination=None, sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/empresa/novo', methods=['POST'])
@login_required
def adicionar_empresa():
    """Insere nova empresa usando Stored Procedure"""
    
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

@app.route('/empresa/remover/<path:nif>', methods=['POST'])
@login_required
def remover_empresa(nif):
    """Remove uma empresa"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_empresas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverEmpresa (?)}", (nif,))
        conn.commit()
        flash('✅ Empresa removida com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_empresas'))

@app.route('/fabricas')
@login_required
def lista_fabricas():
    """Lista todas as fábricas com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/fabricas.html', registos=[], empresas=[], distribuidoras=[], pagination=None, sucesso=False)
        
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            cursor.execute("""
                SELECT f.Id, f.Nome, f.Localizacao, e.Nome AS Empresa, d.Nome AS Distribuidora
                FROM Fabrica f
                JOIN Empresa e ON f.Empresa_Nif = e.Nif
                JOIN Distribuidora d ON f.Distribuidora_Id = d.Id
                WHERE f.Id = ?
            """, (fabrica_id,))
            fabricas = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM vw_Fabricas ORDER BY Nome")
            fabricas = cursor.fetchall()
        
        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Distribuidora ORDER BY Nome")
        distribuidoras = cursor.fetchall()
        
        cursor.close()
        
        pagination = paginate(fabricas, page, per_page)
        return render_template('tabelas/fabricas.html', 
                             registos=pagination['items'],
                             empresas=empresas,
                             distribuidoras=distribuidoras,
                             pagination=pagination,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar fabricas: {e}")
        flash(f'Erro ao carregar fábricas: {str(e)}', 'error')
        return render_template('tabelas/fabricas.html', registos=[], empresas=[], distribuidoras=[], pagination=None, sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/fabrica/novo', methods=['POST'])
@login_required
def adicionar_fabrica():
    """Insere nova fábrica usando Stored Procedure"""
    
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

@app.route('/fabrica/remover/<int:id>', methods=['POST'])
@login_required
def remover_fabrica(id):
    """Remove uma fábrica"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_fabricas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverFabrica (?)}", (id,))
        conn.commit()
        flash('✅ Fábrica removida com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_fabricas'))

@app.route('/fornecedores')
@login_required
def lista_fornecedores():
    """Lista todos os fornecedores com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/fornecedores.html', registos=[], empresas=[], pagination=None)
    
    try:
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica':
            cursor.execute("""
                SELECT DISTINCT f.Id, f.Nome, e.Nome AS Empresa
                FROM Fornecedor f
                LEFT JOIN Empresa e ON f.Empresa_Nif = e.Nif
                WHERE EXISTS (
                    SELECT 1 FROM MateriaPrima mp WHERE mp.Fornecedor_Id = f.Id
                )
                ORDER BY f.Nome
            """)
            registos = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM vw_Fornecedores ORDER BY Nome")
            registos = cursor.fetchall()
        
        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()
        
        pagination = paginate(registos, page, per_page)
        return render_template('tabelas/fornecedores.html', registos=pagination['items'], empresas=empresas, pagination=pagination)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/fornecedores.html', registos=[], empresas=[], pagination=None)
    finally:
        conn.close()

@app.route('/fornecedor/novo', methods=['POST'])
@login_required
def adicionar_fornecedor():
    """Insere novo fornecedor usando Stored Procedure"""
    
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

@app.route('/fornecedor/remover/<int:id>', methods=['POST'])
@login_required
def remover_fornecedor(id):
    """Remove um fornecedor"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_fornecedores'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverFornecedor (?)}", (id,))
        conn.commit()
        flash('✅ Fornecedor removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_fornecedores'))

@app.route('/funcionarios')
@login_required
def lista_funcionarios():
    """Lista todos os funcionários com paginação"""
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            return render_template('tabelas/funcionarios.html', registos=[], pessoas=[], cargos=[], empresas=[], fabricas=[], pagination=None, erro="Erro de conexão", sucesso=False)
        
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            cursor.execute("""
                SELECT f.Pessoa_Cc, p.Nome, c.Nome AS Cargo, e.Nome AS Empresa, fab.Nome AS Fabrica
                FROM Funcionario f
                INNER JOIN Pessoa p ON f.Pessoa_Cc = p.Cc
                LEFT JOIN Cargo c ON f.Cargo_Id = c.Id
                LEFT JOIN Empresa e ON f.Empresa_Nif = e.Nif
                LEFT JOIN Fabrica fab ON f.Fabrica_Id = fab.Id
                WHERE f.Fabrica_Id = ?
                ORDER BY p.Nome
            """, (fabrica_id,))
            funcionarios = cursor.fetchall()
            
            cursor.execute("SELECT Id, Nome FROM Fabrica WHERE Id = ?", (fabrica_id,))
            fabricas = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM vw_Funcionarios ORDER BY Nome")
            funcionarios = cursor.fetchall()
            
            print(f"📊 TODOS os funcionários (sem filtro): {len(funcionarios)} registos")
            
            cursor.execute("SELECT Id, Nome FROM Fabrica ORDER BY Nome")
            fabricas = cursor.fetchall()
        
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
        
        cursor.close()
        
        # Aplicar paginação
        pagination = paginate(funcionarios, page, per_page)
        
        return render_template('tabelas/funcionarios.html', 
                             registos=pagination['items'], 
                             pessoas=pessoas,
                             cargos=cargos,
                             empresas=empresas,
                             fabricas=fabricas,
                             pagination=pagination,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar funcionarios: {e}")
        return render_template('tabelas/funcionarios.html', registos=[], pessoas=[], cargos=[], empresas=[], fabricas=[], pagination=None, erro=str(e), sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/funcionario/novo', methods=['POST'])
@login_required
def adicionar_funcionario():
    """Insere novo funcionário e dados pessoais usando Stored Procedure"""
    
    conn = None
    try:
        cc = request.form.get('pessoa_cc')
        nome = request.form.get('nome')
        email = request.form.get('email')
        data_nasc = request.form.get('data_nasc')
        morada = request.form.get('morada')
        telemovel = request.form.get('telemovel')
        cargo_id = request.form.get('cargo_id')
        empresa_nif = request.form.get('empresa_nif')
        fabrica_id = request.form.get('fabrica_id') if request.form.get('fabrica_id') else None

        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_funcionarios'))

        cursor = conn.cursor()

        sql = "{CALL dbo.InserirNovoFuncionario (?, ?, ?, ?, ?, ?, ?, ?, ?)}"
        params = (cc, nome, email, data_nasc, morada, telemovel, cargo_id, empresa_nif, fabrica_id)
        
        cursor.execute(sql, params)
        conn.commit()
        
        flash('✅ Funcionário registado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao adicionar funcionário: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_funcionarios'))

@app.route('/funcionario/remover/<path:cc>', methods=['POST'])
@login_required
def remover_funcionario(cc):
    """Remove um funcionário"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_funcionarios'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverFuncionario (?)}", (cc,))
        conn.commit()
        flash('✅ Funcionário removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_funcionarios'))

@app.route('/itens')
@login_required
def lista_itens():
    """Lista todos os itens de venda com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/itens.html', registos=[], vendas=[], produtos=[], pagination=None)
    
    try:
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Loja' and session.get('loja_id'):
            loja_id = session.get('loja_id')
            cursor.execute("""
                SELECT i.Venda_Id, p.Nome AS Produto, i.Produto_Referencia,
                i.Quantidade, i.Preco, (i.Quantidade * i.Preco) AS Total
                FROM Item i
                INNER JOIN Produto p ON i.Produto_Referencia = p.Referencia
                INNER JOIN Venda v ON i.Venda_Id = v.Id
                WHERE v.Loja_Id = ?
                ORDER BY i.Venda_Id DESC
            """, (loja_id,))
            registos = cursor.fetchall()
            
            cursor.execute("SELECT Id FROM Venda WHERE Loja_Id = ? ORDER BY Id DESC", (loja_id,))
            vendas = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM vw_Itens ORDER BY Venda_Id DESC")
            registos = cursor.fetchall()
            
            cursor.execute("SELECT Id FROM Venda ORDER BY Id DESC")
            vendas = cursor.fetchall()
        
        cursor.execute("SELECT Referencia, Nome, Preco FROM Produto ORDER BY Nome")
        produtos = cursor.fetchall()
        
        pagination = paginate(registos, page, per_page)
        return render_template('tabelas/itens.html', registos=pagination['items'], vendas=vendas, produtos=produtos, pagination=pagination)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/itens.html', registos=[], vendas=[], produtos=[], pagination=None)
    finally:
        conn.close()

@app.route('/lojas')
@login_required
def lista_lojas():
    """Lista lojas com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/lojas.html', registos=[], armazens=[], pagination=None, sucesso=False)
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_Lojas ORDER BY Nome")
        lojas = cursor.fetchall()
        
        cursor.execute("SELECT Id, Localizacao FROM dbo.Armazem ORDER BY Localizacao")
        armazens = cursor.fetchall()
        
        cursor.close()
        
        pagination = paginate(lojas, page, per_page)
        return render_template('tabelas/lojas.html', registos=pagination['items'], armazens=armazens, pagination=pagination, sucesso=True)
        
    except Exception as e:
        print(f"Erro ao listar lojas: {e}")
        flash(f'Erro ao carregar lojas: {str(e)}', 'error')
        return render_template('tabelas/lojas.html', registos=[], armazens=[], pagination=None, sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/loja/nova', methods=['POST'])
@login_required
def adicionar_loja():
    
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

@app.route('/loja/remover/<int:id>', methods=['POST'])
@login_required
def remover_loja(id):
    """Remove uma loja"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_lojas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverLoja (?)}", (id,))
        conn.commit()
        flash('✅ Loja removida com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_lojas'))

@app.route('/maquinas')
@login_required
def lista_maquinas():
    """Lista todas as máquinas com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None: 
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/maquinas.html', registos=[], fabricas=[], pagination=None, sucesso=False)
        
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            cursor.execute("""
                SELECT m.Id, m.Descricao, m.Tipo, f.Nome AS Fabrica
                FROM Maquina m
                INNER JOIN Fabrica f ON m.Fabrica_Id = f.Id
                WHERE m.Fabrica_Id = ?
                ORDER BY m.Descricao
            """, (fabrica_id,))
            maquinas = cursor.fetchall()
            
            cursor.execute("SELECT Id, Nome FROM Fabrica WHERE Id = ?", (fabrica_id,))
            fabricas = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM vw_Maquinas ORDER BY Descricao")
            maquinas = cursor.fetchall()
            
            cursor.execute("SELECT Id, Nome FROM Fabrica ORDER BY Nome")
            fabricas = cursor.fetchall()
        
        cursor.close()
        
        pagination = paginate(maquinas, page, per_page)
        return render_template('tabelas/maquinas.html', 
                             registos=pagination['items'],
                             fabricas=fabricas,
                             pagination=pagination,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar maquinas: {e}")
        flash(f'Erro ao carregar máquinas: {str(e)}', 'error')
        return render_template('tabelas/maquinas.html', registos=[], fabricas=[], pagination=None, sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/maquina/novo', methods=['POST'])
@login_required
def adicionar_maquina():
    """Insere nova máquina usando Stored Procedure"""
    
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

@app.route('/maquina/remover/<int:id>', methods=['POST'])
@login_required
def remover_maquina(id):
    """Remove uma máquina"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_maquinas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverMaquina (?)}", (id,))
        conn.commit()
        flash('✅ Máquina removida com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_maquinas'))

@app.route('/materias_primas')
@login_required
def lista_materias_primas():
    """Lista todas as matérias-primas com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/materias_primas.html', registos=[], fornecedores=[], pagination=None)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_MateriasPrimas ORDER BY Referencia")
        registos = cursor.fetchall()
        
        cursor.execute("SELECT Id, Nome FROM Fornecedor ORDER BY Nome")
        fornecedores = cursor.fetchall()
        
        pagination = paginate(registos, page, per_page)
        return render_template('tabelas/materias_primas.html', registos=pagination['items'], fornecedores=fornecedores, pagination=pagination)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/materias_primas.html', registos=[], fornecedores=[], pagination=None)
    finally:
        conn.close()

@app.route('/materia_prima/nova', methods=['POST'])
@login_required
def adicionar_materia_prima():
    """Insere nova matéria-prima usando Stored Procedure"""
    
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

@app.route('/materia_prima/remover/<path:referencia>', methods=['POST'])
@login_required
def remover_materia_prima(referencia):
    """Remove uma matéria-prima"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_materias_primas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverMateriaPrima (?)}", (referencia,))
        conn.commit()
        flash('✅ Matéria-prima removida com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_materias_primas'))

@app.route('/produtos')
@login_required
def lista_produtos():
    """Lista todos os produtos com dados para o modal e paginação"""
    
    # Obter página atual do query string
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Produtos por página
    
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            flash('Erro de conexão com a base de dados', 'error')
            return render_template('tabelas/produtos.html', 
                                 registos=[], 
                                 maquinas=[], 
                                 distribuidoras=[],
                                 pagination=None,
                                 sucesso=False)
        cursor = conn.cursor()
        
        if session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            cursor.execute("""
                SELECT p.Nome, p.Referencia, p.Descricao, p.Preco, p.Maquina_Id, p.Distribuidora_Id 
                FROM Produto p
                INNER JOIN Maquina m ON p.Maquina_Id = m.Id
                WHERE m.Fabrica_Id = ?
                ORDER BY p.Nome
            """, (fabrica_id,))
            produtos = cursor.fetchall()
            
            cursor.execute("SELECT Id, Descricao FROM Maquina WHERE Fabrica_Id = ? ORDER BY Descricao", (fabrica_id,))
            maquinas = cursor.fetchall()
            
            cursor.execute("""
                SELECT d.Id, d.Nome 
                FROM Distribuidora d
                INNER JOIN Fabrica f ON f.Distribuidora_Id = d.Id
                WHERE f.Id = ?
            """, (fabrica_id,))
            distribuidoras = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT Nome, Referencia, Descricao, Preco, Maquina_Id, Distribuidora_Id 
                FROM Produto
                ORDER BY Nome
            """) 
            produtos = cursor.fetchall()
            
            print(f"📊 TODOS os produtos (sem filtro): {len(produtos)} registos")
            
            cursor.execute("SELECT Id, Descricao FROM Maquina ORDER BY Descricao") 
            maquinas = cursor.fetchall()

            cursor.execute("SELECT Id, Nome FROM Distribuidora ORDER BY Nome")
            distribuidoras = cursor.fetchall()
        
        cursor.close()
        
        # Aplicar paginação
        pagination = paginate(produtos, page, per_page)
        
        return render_template('tabelas/produtos.html', 
                             registos=pagination['items'],
                             maquinas=maquinas,            
                             distribuidoras=distribuidoras,
                             pagination=pagination,
                             sucesso=True)
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        flash(f'Erro ao carregar produtos: {str(e)}', 'error')
        return render_template('tabelas/produtos.html', 
                             registos=[], 
                             maquinas=[], 
                             distribuidoras=[],
                             pagination=None,
                             sucesso=False)
    finally:
        if conn:
            conn.close()

@app.route('/produto/novo', methods=['POST'])
@login_required
def adicionar_produto():
    """
    Processa a submissão do Modal e insere um novo produto no BD através de uma SP.
    """
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


@app.route('/produto/editar', methods=['POST'])
@login_required
def editar_produto():
    """Edita um produto existente"""
    try:
        # Dados do formulário
        referencia_atual = request.form.get('referencia_atual')
        nova_referencia = request.form.get('referencia')
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco').replace(',', '.'))
        maquina_id = int(request.form.get('maquina_id'))
        distribuidora_id = int(request.form.get('distribuidora_id'))
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão com a base de dados', 'error')
            return redirect(url_for('lista_produtos'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarProduto (?, ?, ?, ?, ?, ?, ?)}",
                       (referencia_atual, nova_referencia, nome, descricao, preco, maquina_id, distribuidora_id))
        conn.commit()
        flash('✅ Produto atualizado com sucesso!', 'success')
    except ValueError:
         flash('❌ Erro: Verifique se os valores numéricos estão corretos.', 'error')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_produtos'))


@app.route('/produto/remover/<path:referencia>', methods=['POST'])
@login_required
def remover_produto(referencia):
    """Remove um produto"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_produtos'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverProduto (?)}", (referencia,))
        conn.commit()
        flash('✅ Produto removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_produtos'))


@app.route('/stock')
@login_required
def lista_stock():
    """Lista todo o stock com opção de adicionar e paginação"""
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/stock.html', registos=[], produtos=[], armazens=[], pagination=None)
    
    try:
        cursor = conn.cursor()
        
        # Admin de Loja - vê apenas stock do armazém da sua loja
        if session.get('tipo_admin') == 'Loja' and session.get('loja_id'):
            loja_id = session.get('loja_id')
            cursor.execute("SELECT Armazem_Id FROM Loja WHERE Id = ?", (loja_id,))
            armazem_row = cursor.fetchone()
            
            if armazem_row and armazem_row[0]:
                armazem_id = armazem_row[0]
                cursor.execute("SELECT * FROM vw_Stock WHERE Armazem_Id = ? ORDER BY UltimoMov DESC", (armazem_id,))
                registos = cursor.fetchall()
                
                cursor.execute("SELECT Referencia, Nome FROM Produto ORDER BY Nome")
                produtos = cursor.fetchall()
                
                cursor.execute("SELECT Id, Localizacao FROM Armazem WHERE Id = ?", (armazem_id,))
                armazens = cursor.fetchall()
            else:
                flash('Sua loja não possui armazém associado.', 'warning')
                return render_template('tabelas/stock.html', registos=[], produtos=[], armazens=[], pagination=None)
        
        elif session.get('tipo_admin') == 'Fabrica' and session.get('fabrica_id'):
            fabrica_id = session.get('fabrica_id')
            
            cursor.execute("""
                SELECT s.*
                FROM vw_Stock s
                INNER JOIN DistribuidoraArmazem da ON s.Armazem_Id = da.Armazem_Id
                INNER JOIN Fabrica f ON da.Distribuidora_Id = f.Distribuidora_Id
                WHERE f.Id = ?
                ORDER BY s.UltimoMov DESC
            """, (fabrica_id,))
            registos = cursor.fetchall()
            
            cursor.execute("""
                SELECT p.Referencia, p.Nome 
                FROM Produto p
                INNER JOIN Maquina m ON p.Maquina_Id = m.Id
                WHERE m.Fabrica_Id = ?
                ORDER BY p.Nome
            """, (fabrica_id,))
            produtos = cursor.fetchall()
            
            cursor.execute("""
                SELECT a.Id, a.Localizacao
                FROM Armazem a
                INNER JOIN DistribuidoraArmazem da ON a.Id = da.Armazem_Id
                INNER JOIN Fabrica f ON da.Distribuidora_Id = f.Distribuidora_Id
                WHERE f.Id = ?
                ORDER BY a.Localizacao
            """, (fabrica_id,))
            armazens = cursor.fetchall()
        
        else:
            cursor.execute("SELECT * FROM vw_Stock ORDER BY UltimoMov DESC")
            registos = cursor.fetchall()
            
            cursor.execute("SELECT Referencia, Nome FROM Produto ORDER BY Nome")
            produtos = cursor.fetchall()
            
            cursor.execute("SELECT Id, Localizacao FROM Armazem ORDER BY Localizacao")
            armazens = cursor.fetchall()
        
        # Aplicar paginação
        pagination = paginate(registos, page, per_page)
        
        return render_template('tabelas/stock.html', registos=pagination['items'], produtos=produtos, armazens=armazens, pagination=pagination)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/stock.html', registos=[], produtos=[], armazens=[], pagination=None)
    finally:
        conn.close()

@app.route('/stock/novo', methods=['POST'])
@login_required
def adicionar_stock():
    """Insere nova entrada de stock usando Stored Procedure"""
    
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

@app.route('/stock/remover/<path:produto_ref>/<int:armazem_id>', methods=['POST'])
@login_required
def remover_stock(produto_ref, armazem_id):
    """Remove um registo de stock"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_stock'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverStock (?, ?)}", (produto_ref, armazem_id))
        conn.commit()
        flash('✅ Registo de stock removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_stock'))

@app.route('/vendas')
@login_required
def lista_vendas():
    """
    Lista as vendas. Filtra automaticamente por Loja_Id se o admin for 'Loja'.
    Se for 'Geral', lista todas as vendas. Com paginação.
    """
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
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
            return render_template('tabelas/vendas.html', erro="Erro de conexão", sucesso=False, pagination=None)
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.ObterVendasPorLoja (?)}", parametro_loja_id)
        vendas = cursor.fetchall()

        cursor.execute("SELECT Referencia, Nome FROM Produto ORDER BY Nome")
        produtos = cursor.fetchall()

        lojas = []
        if session.get('tipo_admin') == 'Geral':
            cursor.execute("SELECT Id, Nome FROM Loja")
        lojas = cursor.fetchall()
        
        # Aplicar paginação
        pagination = paginate(vendas, page, per_page)
        
        sucesso = True
    except Exception as e:
        erro = f"Erro ao listar vendas: {e}"
        print(f"❌ {erro}")
        vendas = []
        pagination = None
    finally:
        if conn:
            conn.close()
    return render_template('tabelas/vendas.html', 
                            dados_vendas=pagination['items'] if pagination else vendas, 
                            dados_produtos=produtos,
                            dados_lojas=lojas,
                            pagination=pagination,
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

        flash('✅ Venda registada com sucesso!', 'success')
        return jsonify({'sucesso': True, 'mensagem': 'Venda registada com sucesso!'})
    except Exception as e:
        error_msg = str(e).split(']')[-1]
        flash(f'❌ Erro ao adicionar venda: {error_msg}', 'error')
        return jsonify({'sucesso': False, 'erro': error_msg})
    finally:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        conn.close()
@app.route('/api/venda/<int:venda_id>/itens')
@login_required
def obter_itens_venda(venda_id):
    """API que retorna os itens de uma venda específica em formato JSON"""
    
    conn = get_db_connection()
    itens = []
    try:
        cursor = conn.cursor()
        # Usar query direta em vez da SP
        cursor.execute("""
            SELECT P.Nome, I.Quantidade, I.Preco, (I.Quantidade * I.Preco) as Total
            FROM Item I
            JOIN Produto P ON I.Produto_Referencia = P.Referencia
            WHERE I.Venda_Id = ?
        """, (venda_id,))

        for row in cursor.fetchall():
            itens.append({
                'produto': row[0],  # Nome do produto
                'quantidade': row[1],
                'preco_unit': row[2],
                'subtotal': float(row[3])  # Total já calculado
            })
        return jsonify(itens)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/venda/<int:venda_id>/detalhes')
@login_required
def obter_detalhes_venda(venda_id):
    """API que retorna todos os detalhes de uma venda para edição"""
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Buscar dados da venda
        cursor.execute("""
            SELECT v.Id, v.DataHora, v.ValorTotal, v.MetodoPagamento, 
                   v.Cliente_Nif, v.Loja_Id, l.Nome as Loja_Nome
            FROM Venda v
            LEFT JOIN Loja l ON v.Loja_Id = l.Id
            WHERE v.Id = ?
        """, (venda_id,))
        
        venda_row = cursor.fetchone()
        if not venda_row:
            return jsonify({'erro': 'Venda não encontrada'}), 404
        
        # Buscar itens da venda
        # Primeiro precisamos buscar com JOIN para pegar a Referencia
        cursor.execute("""
            SELECT P.Referencia, P.Nome, I.Quantidade, I.Preco, (I.Quantidade * I.Preco) as Total
            FROM Item I
            JOIN Produto P ON I.Produto_Referencia = P.Referencia
            WHERE I.Venda_Id = ?
        """, (venda_id,))
        
        itens = []
        for row in cursor.fetchall():
            itens.append({
                'produto_ref': row[0],  # Referencia
                'produto_nome': row[1],  # Nome
                'quantidade': row[2],
                'preco_unit': float(row[3]),
                'subtotal': float(row[4])
            })
        
        venda = {
            'id': venda_row[0],
            'data': venda_row[1].strftime('%Y-%m-%d') if venda_row[1] else '',
            'valor_total': float(venda_row[2]) if venda_row[2] else 0,
            'metodo_pagamento': venda_row[3],
            'cliente_nif': venda_row[4],
            'loja_id': venda_row[5],
            'loja_nome': venda_row[6],
            'itens': itens
        }
        
        return jsonify(venda)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        conn.close()

@app.route('/venda/editar/<int:venda_id>', methods=['POST'])
@login_required
def editar_venda(venda_id):
    """Edita uma venda existente"""
    
    data = request.get_json()
    
    if not data or 'itens' not in data or len(data['itens']) == 0:
        return jsonify({'sucesso': False, 'erro': 'Venda deve ter pelo menos 1 item'}), 400
    
    # Converter quantidade de float/string para int
    itens_para_sql = [(item['ref'], int(float(item['qtd']))) for item in data['itens']]
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        nif = data.get('nif') if data.get('nif') else None
        
        sql = "{CALL dbo.EditarVenda (?, ?, ?, ?)}"
        params = (
            venda_id,
            nif,
            data['pagamento'],
            itens_para_sql
        )
        
        cursor.execute(sql, params)
        conn.commit()

        flash('✅ Venda editada com sucesso!', 'success')
        return jsonify({'sucesso': True, 'mensagem': 'Venda editada com sucesso!'})
        
    except Exception as e:
        conn.rollback()
        error_msg = str(e)
        flash(f'❌ Erro ao editar venda: {error_msg}', 'error')
        return jsonify({'sucesso': False, 'erro': error_msg}), 500
    finally:
        conn.close()

@app.route('/vendedores')
@login_required
def lista_vendedores():
    """Lista todos os vendedores com paginação"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    if session.get('tipo_admin') == 'Loja':
        flash('Acesso negado. Admins de Loja não têm permissão para visualizar vendedores.', 'error')
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    if not conn:
        return render_template('tabelas/vendedores.html', registos=[], cargos=[], empresas=[], pagination=None)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_Vendedores ORDER BY Nome")
        registos = cursor.fetchall()

        cursor.execute("SELECT Id, Nome FROM Cargo ORDER BY Nome")
        cargos = cursor.fetchall()

        cursor.execute("SELECT Nif, Nome FROM Empresa ORDER BY Nome")
        empresas = cursor.fetchall()

        pagination = paginate(registos, page, per_page)
        return render_template('tabelas/vendedores.html', registos=pagination['items'], cargos=cargos, empresas=empresas, pagination=pagination)
    except Exception as e:
        print(f"Erro: {e}")
        return render_template('tabelas/vendedores.html', registos=[], cargos=[], empresas=[], pagination=None)
    finally:
        conn.close()

@app.route('/vendedor/novo', methods=['POST'])
@login_required
def adicionar_vendedor():
    """Insere novo vendedor e contrato usando Stored Procedure completa"""
    
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

@app.route('/vendedor/remover/<path:cc>', methods=['POST'])
@login_required
def remover_vendedor(cc):
    """Remove um vendedor"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_vendedores'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.RemoverVendedor (?)}", (cc,))
        conn.commit()
        flash('✅ Vendedor removido com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao remover: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_vendedores'))

# --- ROTA DE DIAGNÓSTICO (Apenas para admins Geral) ---
@app.route('/admin/diagnostico')
@login_required
@admin_tipo_required('Geral')
def diagnostico_bd():
    """Página de diagnóstico da base de dados - verifica triggers, indexes, etc."""
    
    diagnostico = {
        'triggers': [],
        'indexes': [],
        'stats': {},
        'erros': []
    }
    
    conn = get_db_connection()
    if not conn:
        flash('Erro de conexão com a base de dados', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor()
        
        # Verificar Triggers
        cursor.execute("""
            SELECT 
                t.name AS NomeTrigger,
                OBJECT_NAME(t.parent_id) AS Tabela,
                CASE WHEN t.is_disabled = 0 THEN 'Ativo' ELSE 'Desativado' END AS Estado,
                t.create_date AS DataCriacao
            FROM sys.triggers t
            WHERE OBJECT_SCHEMA_NAME(t.parent_id) = 'dbo'
            ORDER BY t.name
        """)

        for row in cursor.fetchall():
            diagnostico['triggers'].append({
                'nome': row[0],
                'tabela': row[1],
                'estado': row[2],
                'data': row[3].strftime('%Y-%m-%d %H:%M') if row[3] else 'N/A'
            })
        
        # Verificar Indexes
        cursor.execute("""
            SELECT TOP 10
                i.name AS NomeIndex,
                t.name AS Tabela,
                i.type_desc AS Tipo
            FROM sys.indexes i
            INNER JOIN sys.tables t ON i.object_id = t.object_id
            WHERE i.name IS NOT NULL 
              AND t.is_ms_shipped = 0
              AND SCHEMA_NAME(t.schema_id) = 'dbo'
            ORDER BY t.name, i.name
        """)
        for row in cursor.fetchall():
            diagnostico['indexes'].append({
                'nome': row[0],
                'tabela': row[1],
                'tipo': row[2]
            })
        
        # Estatísticas gerais
        diagnostico['stats'] = {
            'produtos': cursor.execute("SELECT COUNT(*) FROM Produto").fetchone()[0],
            'clientes': cursor.execute("SELECT COUNT(*) FROM Cliente").fetchone()[0],
            'vendas': cursor.execute("SELECT COUNT(*) FROM Venda").fetchone()[0],
            'funcionarios': cursor.execute("SELECT COUNT(*) FROM Funcionario").fetchone()[0],
            'armazens': cursor.execute("SELECT COUNT(*) FROM Armazem").fetchone()[0],
        }
        
    except Exception as e:
        diagnostico['erros'].append(str(e))
    finally:
        conn.close()
    
    # Renderizar página simples de diagnóstico
    html = f"""
    {{% extends 'base.html' %}}
    {{% block title %}}Diagnóstico BD{{% endblock %}}
    {{% block header_title %}}🔧 Diagnóstico da Base de Dados{{% endblock %}}
    {{% block content %}}
    <div class="row g-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header"><h5 class="card-title mb-0">🔥 Triggers Ativos</h5></div>
                <div class="card-body">
                    <table class="table table-sm">
                        <thead><tr><th>Nome</th><th>Tabela</th><th>Estado</th></tr></thead>
                        <tbody>
                        {{% for t in triggers %}}
                            <tr>
                                <td>{{{{ t.nome }}}}</td>
                                <td><code>{{{{ t.tabela }}}}</code></td>
                                <td>{{% if t.estado == 'Ativo' %}}<span class="badge bg-success">✅ Ativo</span>{{% else %}}<span class="badge bg-danger">❌ Desativado</span>{{% endif %}}</td>
                            </tr>
                        {{% else %}}
                            <tr><td colspan="3" class="text-muted">Nenhum trigger encontrado</td></tr>
                        {{% endfor %}}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-header"><h5 class="card-title mb-0">📊 Estatísticas</h5></div>
                <div class="card-body">
                    <ul class="list-group">
                        <li class="list-group-item d-flex justify-content-between">Produtos <span class="badge bg-primary">{{{{ stats.produtos }}}}</span></li>
                        <li class="list-group-item d-flex justify-content-between">Clientes <span class="badge bg-primary">{{{{ stats.clientes }}}}</span></li>
                        <li class="list-group-item d-flex justify-content-between">Vendas <span class="badge bg-primary">{{{{ stats.vendas }}}}</span></li>
                        <li class="list-group-item d-flex justify-content-between">Funcionários <span class="badge bg-primary">{{{{ stats.funcionarios }}}}</span></li>
                        <li class="list-group-item d-flex justify-content-between">Armazéns <span class="badge bg-primary">{{{{ stats.armazens }}}}</span></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="mt-4">
        <a href="{{{{ url_for('dashboard') }}}}" class="btn btn-secondary">← Voltar</a>
    </div>
    {{% endblock %}}
    """
    
    from flask import render_template_string
    return render_template_string(html, triggers=diagnostico['triggers'], indexes=diagnostico['indexes'], stats=diagnostico['stats'])

# --- PÁGINA DE TESTE DE TRIGGERS ---
@app.route('/admin/testar-triggers')
@login_required
@admin_tipo_required('Geral')
def testar_triggers_page():
    """Página para testar triggers interativamente"""
    
    conn = get_db_connection()
    armazens = []
    produtos = []
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Id, Localizacao, Capacidade FROM Armazem ORDER BY Localizacao")
            armazens = cursor.fetchall()
            cursor.execute("SELECT Referencia, Nome FROM Produto ORDER BY Nome")
            produtos = cursor.fetchall()
        except:
            pass
        finally:
            conn.close()
    
    html = """
    {% extends 'base.html' %}
    {% block title %}Testar Triggers{% endblock %}
    {% block header_title %}🧪 Testar Triggers{% endblock %}
    {% block content %}
    
    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    {% for category, message in messages %}
    <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} alert-dismissible fade show" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    {% endfor %}
    {% endif %}
    {% endwith %}
    
    <div class="row g-4">
        <!-- TESTE 1: Capacidade Armazém -->
        <div class="col-md-6">
            <div class="card h-100">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">🏭 Teste: Capacidade do Armazém</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted">Tenta adicionar stock que excede a capacidade do armazém.</p>
                    <p><strong>Trigger:</strong> <code>TR_ValidarCapacidadeArmazem</code></p>
                    <p><strong>Resultado esperado:</strong> <span class="text-danger">Erro - "Capacidade excedida"</span></p>
                    
                    <form method="POST" action="{{ url_for('testar_trigger_capacidade') }}">
                        <div class="mb-3">
                            <label class="form-label">Armazém</label>
                            <select name="armazem_id" class="form-select" required>
                                {% for a in armazens %}
                                <option value="{{ a[0] }}">{{ a[1] }} (Cap: {{ a[2] }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Produto</label>
                            <select name="produto_ref" class="form-select" required>
                                {% for p in produtos %}
                                <option value="{{ p[0] }}">{{ p[1] }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Quantidade (coloca valor ALTO)</label>
                            <input type="number" name="quantidade" class="form-control" value="999999999" required>
                        </div>
                        <button type="submit" class="btn btn-warning">⚡ Testar Trigger</button>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- TESTE 2: Stock Negativo -->
        <div class="col-md-6">
            <div class="card h-100">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">📦 Teste: Stock Negativo</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted">Tenta colocar um valor de stock negativo.</p>
                    <p><strong>Trigger:</strong> <code>GarantirStockPositivo</code></p>
                    <p><strong>Resultado esperado:</strong> <span class="text-danger">Erro - "Stock insuficiente"</span></p>
                    
                    <form method="POST" action="{{ url_for('testar_trigger_stock_negativo') }}">
                        <div class="mb-3">
                            <label class="form-label">Armazém</label>
                            <select name="armazem_id" class="form-select" required>
                                {% for a in armazens %}
                                <option value="{{ a[0] }}">{{ a[1] }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Produto</label>
                            <select name="produto_ref" class="form-select" required>
                                {% for p in produtos %}
                                <option value="{{ p[0] }}">{{ p[1] }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <button type="submit" class="btn btn-danger">⚡ Testar Trigger</button>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- INFO -->
        <div class="col-12">
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">ℹ️ Como Funcionam os Triggers</h5>
                </div>
                <div class="card-body">
                    <p>Os triggers são executados <strong>automaticamente</strong> pelo SQL Server quando tentas fazer operações inválidas:</p>
                    <ul>
                        <li><strong>TR_ValidarCapacidadeArmazem</strong> - Bloqueia INSERT/UPDATE em Stock se exceder capacidade</li>
                        <li><strong>GarantirStockPositivo</strong> - Bloqueia UPDATE em Stock se quantidade ficar negativa</li>
                        <li><strong>AtualizarTotalVenda</strong> - Recalcula automaticamente o ValorTotal quando adicionas itens</li>
                        <li><strong>TR_BloquearExclusaoClienteComVendas</strong> - Impede DELETE de clientes com histórico</li>
                    </ul>
                    <p class="mb-0">Se vires uma <span class="badge bg-danger">mensagem de erro vermelha</span> após clicar nos botões, significa que o <strong>trigger está a funcionar corretamente!</strong></p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="mt-4">
        <a href="{{ url_for('diagnostico_bd') }}" class="btn btn-secondary">← Ver Diagnóstico</a>
        <a href="{{ url_for('dashboard') }}" class="btn btn-outline-secondary">← Dashboard</a>
    </div>
    {% endblock %}
    """
    
    from flask import render_template_string
    return render_template_string(html, armazens=armazens, produtos=produtos)


@app.route('/admin/testar-triggers/capacidade', methods=['POST'])
@login_required
@admin_tipo_required('Geral')
def testar_trigger_capacidade():
    """Testa o trigger de capacidade do armazém"""
    
    armazem_id = request.form.get('armazem_id')
    produto_ref = request.form.get('produto_ref')
    quantidade = request.form.get('quantidade', 999999999)
    
    conn = get_db_connection()
    if not conn:
        flash('❌ Erro de conexão com a BD', 'error')
        return redirect(url_for('testar_triggers_page'))
    
    try:
        cursor = conn.cursor()
        
        # Tentar inserir stock enorme
        cursor.execute("""
            INSERT INTO Stock (Produto_Referencia, Armazem_Id, Quantidade, UltimoMov)
            VALUES (?, ?, ?, GETDATE())
        """, (produto_ref, armazem_id, quantidade))
        conn.commit()
        
        # Se chegou aqui, o trigger NÃO bloqueou
        flash('⚠️ ATENÇÃO: A operação foi permitida! O trigger pode não estar ativo ou a capacidade é muito alta.', 'error')
        
        # Reverter a inserção de teste
        cursor.execute("""
            DELETE FROM Stock 
            WHERE Produto_Referencia = ? AND Armazem_Id = ? AND Quantidade = ?
        """, (produto_ref, armazem_id, quantidade))
        conn.commit()
        
    except Exception as e:
        error_msg = str(e)
        if 'Capacidade' in error_msg or 'excedida' in error_msg.lower():
            flash(f'✅ TRIGGER FUNCIONOU! Erro capturado: {error_msg.split("]")[-1]}', 'success')
        else:
            flash(f'❌ Erro (pode ser do trigger): {error_msg.split("]")[-1]}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('testar_triggers_page'))


@app.route('/admin/testar-triggers/stock-negativo', methods=['POST'])
@login_required
@admin_tipo_required('Geral')
def testar_trigger_stock_negativo():
    """Testa o trigger de stock negativo"""
    
    armazem_id = request.form.get('armazem_id')
    produto_ref = request.form.get('produto_ref')
    
    conn = get_db_connection()
    if not conn:
        flash('❌ Erro de conexão com a BD', 'error')
        return redirect(url_for('testar_triggers_page'))
    
    try:
        cursor = conn.cursor()
        
        # Verificar se existe stock para este produto/armazém
        cursor.execute("""
            SELECT Quantidade FROM Stock 
            WHERE Produto_Referencia = ? AND Armazem_Id = ?
        """, (produto_ref, armazem_id))
        row = cursor.fetchone()
        
        if row:
            # Tentar colocar stock negativo
            cursor.execute("""
                UPDATE Stock SET Quantidade = -100 
                WHERE Produto_Referencia = ? AND Armazem_Id = ?
            """, (produto_ref, armazem_id))
            conn.commit()
            
            # Se chegou aqui, o trigger NÃO bloqueou - reverter
            cursor.execute("""
                UPDATE Stock SET Quantidade = ? 
                WHERE Produto_Referencia = ? AND Armazem_Id = ?
            """, (row[0], produto_ref, armazem_id))
            conn.commit()
            
            flash('⚠️ ATENÇÃO: A operação foi permitida! O trigger GarantirStockPositivo pode não estar ativo.', 'error')
        else:
            flash('⚠️ Não existe stock para este produto/armazém. Adiciona stock primeiro.', 'error')
        
    except Exception as e:
        error_msg = str(e)
        if 'Stock insuficiente' in error_msg or 'negativ' in error_msg.lower():
            flash(f'✅ TRIGGER FUNCIONOU! Erro capturado: {error_msg.split("]")[-1]}', 'success')
        else:
            flash(f'❌ Erro (pode ser do trigger): {error_msg.split("]")[-1]}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('testar_triggers_page'))


if __name__ == '__main__':
    print("🚀 A iniciar servidor Flask...")
    print("📍 Aceda a: http://127.0.0.1:5000")
    app.run(debug=True)