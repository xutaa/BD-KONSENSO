"""
Utilitários e Decoradores para BD-KONSENSO
Reduz código repetido nas rotas Flask
"""

from functools import wraps
from flask import session, redirect, url_for, flash
from database import get_db_connection


def login_required(f):
    """
    Decorador que verifica se o utilizador está autenticado.
    Redireciona para login se não estiver.
    
    Uso:
        @app.route('/produtos')
        @login_required
        def lista_produtos():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logado' not in session:
            flash('⚠️ Sessão expirada. Faça login novamente.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_tipo_required(*tipos_permitidos):
    """
    Decorador que verifica se o tipo de admin tem permissão.
    
    Uso:
        @app.route('/empresas')
        @login_required
        @admin_tipo_required('Geral')
        def lista_empresas():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            tipo_admin = session.get('tipo_admin')
            if tipo_admin not in tipos_permitidos:
                flash('❌ Não tem permissão para aceder a esta página.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_db():
    """
    Obtém conexão à base de dados.
    Retorna None se falhar (para uso em rotas).
    """
    return get_db_connection()


def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Executa uma query SQL de forma segura.
    
    Args:
        query: String SQL ou chamada a SP
        params: Tuplo de parâmetros (opcional)
        fetch_one: Retornar apenas um resultado
        fetch_all: Retornar todos os resultados
        commit: Fazer commit após execução
    
    Returns:
        Resultado da query ou None em caso de erro
    
    Uso:
        produtos = execute_query("SELECT * FROM Produto ORDER BY Nome")
        produto = execute_query("SELECT * FROM Produto WHERE Referencia = ?", (ref,), fetch_one=True)
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if commit:
            conn.commit()
            return True
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na query: {e}")
        if commit:
            conn.rollback()
        return None
    finally:
        conn.close()


def execute_sp(sp_name, params=None, commit=True):
    """
    Executa um Stored Procedure.
    
    Args:
        sp_name: Nome do SP (sem "dbo.")
        params: Tuplo de parâmetros
        commit: Fazer commit após execução (default: True)
    
    Returns:
        True se sucesso, None se erro
    
    Uso:
        success = execute_sp('InserirNovoProduto', (ref, desc, nome, preco, maq_id, dist_id))
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(f"{{CALL dbo.{sp_name} ({','.join(['?' for _ in params])})}}", params)
        else:
            cursor.execute(f"{{CALL dbo.{sp_name}}}")
        
        if commit:
            conn.commit()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no SP {sp_name}: {e}")
        if commit:
            conn.rollback()
        raise  # Re-lançar para a rota tratar a mensagem
    finally:
        conn.close()


def paginate(items, page, per_page=10):
    """
    Pagina uma lista de items.
    
    Args:
        items: Lista de registos
        page: Número da página atual (1-indexed)
        per_page: Itens por página (default: 10)
    
    Returns:
        dict com:
            - items: Lista de itens da página atual
            - page: Página atual
            - per_page: Itens por página
            - total: Total de itens
            - pages: Número total de páginas
            - has_prev: Se tem página anterior
            - has_next: Se tem próxima página
            - prev_page: Número da página anterior
            - next_page: Número da próxima página
    
    Uso:
        pagination = paginate(produtos, page=1, per_page=10)
    """
    if not items:
        items = []
    
    total = len(items)
    pages = max(1, (total + per_page - 1) // per_page)  # Ceiling division
    page = max(1, min(page, pages))  # Clamp page to valid range
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': pages,
        'has_prev': page > 1,
        'has_next': page < pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < pages else None
    }
