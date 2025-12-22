# =============================================
# ROTAS DE EDIÇÃO - BD-KONSENSO
# Adiciona estas rotas ao app.py após cada rota de remover correspondente
# =============================================

# --- EDITAR CLIENTE ---
@app.route('/cliente/editar', methods=['POST'])
@login_required
def editar_cliente():
    """Edita um cliente existente"""
    try:
        cc = request.form.get('pessoa_cc')
        nome = request.form.get('nome')
        email = request.form.get('email')
        data_nasc = request.form.get('data_nasc')
        morada = request.form.get('morada')
        telemovel = request.form.get('telemovel')
        nif = request.form.get('nif')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_clientes'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarCliente (?, ?, ?, ?, ?, ?, ?)}", 
                      (cc, nome, email, data_nasc, morada, telemovel, nif))
        conn.commit()
        flash('✅ Cliente atualizado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_clientes'))


# --- EDITAR FUNCIONÁRIO ---
@app.route('/funcionario/editar', methods=['POST'])
@login_required
def editar_funcionario():
    """Edita um funcionário existente"""
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
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_funcionarios'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarFuncionario (?, ?, ?, ?, ?, ?, ?, ?, ?)}", 
                      (cc, nome, email, data_nasc, morada, telemovel, cargo_id, empresa_nif, fabrica_id))
        conn.commit()
        flash('✅ Funcionário atualizado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_funcionarios'))


# --- EDITAR VENDEDOR ---
@app.route('/vendedor/editar', methods=['POST'])
@login_required
def editar_vendedor():
    """Edita um vendedor existente"""
    try:
        cc = request.form.get('pessoa_cc')
        nome = request.form.get('nome')
        email = request.form.get('email')
        data_nasc = request.form.get('data_nasc')
        morada = request.form.get('morada')
        telemovel = request.form.get('telemovel')
        cargo_id = request.form.get('cargo_id')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_vendedores'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarVendedor (?, ?, ?, ?, ?, ?, ?)}", 
                      (cc, nome, email, data_nasc, morada, telemovel, cargo_id))
        conn.commit()
        flash('✅ Vendedor atualizado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_vendedores'))


# --- EDITAR EMPRESA ---
@app.route('/empresa/editar', methods=['POST'])
@login_required
def editar_empresa():
    """Edita uma empresa existente"""
    try:
        nif = request.form.get('nif')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        num_telefone = request.form.get('num_telefone')
        email = request.form.get('email')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_empresas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarEmpresa (?, ?, ?, ?, ?)}", 
                      (nif, nome, localizacao, num_telefone, email))
        conn.commit()
        flash('✅ Empresa atualizada com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_empresas'))


# --- EDITAR FORNECEDOR ---
@app.route('/fornecedor/editar', methods=['POST'])
@login_required
def editar_fornecedor():
    """Edita um fornecedor existente"""
    try:
        id = request.form.get('id')
        nome = request.form.get('nome')
        empresa_nif = request.form.get('empresa_nif')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_fornecedores'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarFornecedor (?, ?, ?)}", (id, nome, empresa_nif))
        conn.commit()
        flash('✅ Fornecedor atualizado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_fornecedores'))


# --- EDITAR DISTRIBUIDORA ---
@app.route('/distribuidora/editar', methods=['POST'])
@login_required
def editar_distribuidora():
    """Edita uma distribuidora existente"""
    try:
        id = request.form.get('id')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_distribuidoras'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarDistribuidora (?, ?, ?)}", (id, nome, localizacao))
        conn.commit()
        flash('✅ Distribuidora atualizada com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_distribuidoras'))


# --- EDITAR LOJA ---
@app.route('/loja/editar', methods=['POST'])
@login_required
def editar_loja():
    """Edita uma loja existente"""
    try:
        id = request.form.get('id')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        armazem_id = request.form.get('armazem_id')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_lojas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarLoja (?, ?, ?, ?)}", (id, nome, localizacao, armazem_id))
        conn.commit()
        flash('✅ Loja atualizada com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_lojas'))


# --- EDITAR FÁBRICA ---
@app.route('/fabrica/editar', methods=['POST'])
@login_required
def editar_fabrica():
    """Edita uma fábrica existente"""
    try:
        id = request.form.get('id')
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        empresa_nif = request.form.get('empresa_nif')
        distribuidora_id = request.form.get('distribuidora_id')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_fabricas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarFabrica (?, ?, ?, ?, ?)}", 
                      (id, nome, localizacao, empresa_nif, distribuidora_id))
        conn.commit()
        flash('✅ Fábrica atualizada com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_fabricas'))


# --- EDITAR MÁQUINA ---
@app.route('/maquina/editar', methods=['POST'])
@login_required
def editar_maquina():
    """Edita uma máquina existente"""
    try:
        id = request.form.get('id')
        descricao = request.form.get('descricao')
        tipo = request.form.get('tipo')
        fabrica_id = request.form.get('fabrica_id')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_maquinas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarMaquina (?, ?, ?, ?)}", (id, descricao, tipo, fabrica_id))
        conn.commit()
        flash('✅ Máquina atualizada com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_maquinas'))


# --- EDITAR MATÉRIA-PRIMA ---
@app.route('/materia_prima/editar', methods=['POST'])
@login_required
def editar_materia_prima():
    """Edita uma matéria-prima existente"""
    try:
        referencia = request.form.get('referencia')
        descricao = request.form.get('descricao')
        fornecedor_id = request.form.get('fornecedor_id')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_materias_primas'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarMateriaPrima (?, ?, ?)}", (referencia, descricao, fornecedor_id))
        conn.commit()
        flash('✅ Matéria-prima atualizada com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_materias_primas'))


# --- EDITAR STOCK ---
@app.route('/stock/editar', methods=['POST'])
@login_required
def editar_stock():
    """Edita uma entrada de stock existente"""
    try:
        produto_ref = request.form.get('produto_referencia')
        armazem_id = request.form.get('armazem_id')
        quantidade = request.form.get('quantidade')
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_stock'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarStock (?, ?, ?)}", (produto_ref, armazem_id, quantidade))
        conn.commit()
        flash('✅ Stock atualizado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_stock'))


# --- EDITAR CONTRATO VENDEDOR ---
@app.route('/contrato_vendedor/editar', methods=['POST'])
@login_required
def editar_contrato_vendedor():
    """Edita um contrato de vendedor existente"""
    try:
        vendedor_id = request.form.get('vendedor_id')
        empresa_nif = request.form.get('empresa_nif')
        data_in = request.form.get('data_in')
        data_fim = request.form.get('data_fim') if request.form.get('data_fim') else None
        
        conn = get_db_connection()
        if not conn:
            flash('Erro de conexão', 'error')
            return redirect(url_for('lista_contratos_vendedor'))
        cursor = conn.cursor()
        cursor.execute("{CALL dbo.AtualizarContratoVendedor (?, ?, ?, ?)}", 
                      (vendedor_id, empresa_nif, data_in, data_fim))
        conn.commit()
        flash('✅ Contrato atualizado com sucesso!', 'success')
    except Exception as e:
        error_msg = str(e).split(']')[-1] if ']' in str(e) else str(e)
        flash(f'❌ Erro ao atualizar: {error_msg}', 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('lista_contratos_vendedor'))
