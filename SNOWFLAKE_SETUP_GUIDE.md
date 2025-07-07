# Guia de Configuração do Snowflake

Este guia te ajudará a configurar sua conta Snowflake e obter os dados necessários para conectar com o projeto Airdrop Optimizer.

## 1. Acessando sua Conta Snowflake

### 1.1 Login na Interface Web
1. Acesse: https://app.snowflake.com
2. Faça login com suas credenciais
3. Você será direcionado para a interface principal do Snowflake

### 1.2 Navegando pela Interface
- **Worksheets**: Para executar queries SQL
- **Databases**: Para gerenciar bancos de dados
- **Warehouses**: Para gerenciar recursos computacionais
- **Users & Roles**: Para gerenciar usuários e permissões

## 2. Obtendo os Dados de Conexão

### 2.1 Account URL
1. Na interface web, clique no seu nome de usuário (canto superior direito)
2. Selecione "Account"
3. Copie o **Account URL** (exemplo: `xy12345.snowflakecomputing.com`)
4. Este será o valor para `SNOWFLAKE_ACCOUNT`

### 2.2 Dados do Usuário
1. **Username**: Seu nome de usuário (que você criou na conta)
2. **Password**: A senha que você definiu
3. **Role**: Geralmente `ACCOUNTADMIN` para administradores

### 2.3 Warehouse
1. Vá para "Admin" → "Warehouses"
2. Clique em "Create Warehouse" se não existir
3. Nome sugerido: `COMPUTE_WH`
4. Tamanho: `X-Small` (para começar)
5. Auto-suspend: `10 minutes`
6. Auto-resume: `True`

### 2.4 Database e Schema
1. Vá para "Data" → "Databases"
2. Clique em "Create Database"
3. Nome: `AIRDROP_OPTIMIZER`
4. Schema padrão: `PUBLIC`

## 3. Configurando o Arquivo .env

Crie um arquivo `.env` na raiz do projeto com os seguintes dados:

```bash
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=seu_account.snowflakecomputing.com
SNOWFLAKE_USER=seu_username
SNOWFLAKE_PASSWORD=sua_senha
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=AIRDROP_OPTIMIZER
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN

# Groq AI Configuration
GROQ_API_KEY=sua_groq_api_key

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 4. Testando a Conexão

### 4.1 Executar o Script de Migração
```bash
# Ativar o ambiente virtual
source .venv/bin/activate

# Executar o script de migração
python migrate_to_snowflake.py
```

### 4.2 Teste Manual da Conexão
```bash
# Teste simples de conexão
python -c "
from snowflake_config import snowflake_manager
try:
    snowflake_manager.connect()
    print('✅ Conexão com Snowflake estabelecida com sucesso!')
    snowflake_manager.disconnect()
except Exception as e:
    print(f'❌ Erro na conexão: {e}')
"
```

## 5. Verificando a Configuração

### 5.1 Verificar Tabelas Criadas
Execute no Snowflake Worksheet:

```sql
-- Verificar se as tabelas foram criadas
SHOW TABLES IN AIRDROP_OPTIMIZER.PUBLIC;

-- Verificar dados de exemplo
SELECT * FROM AIRDROP_OPTIMIZER.PUBLIC.campaign_data;
```

### 5.2 Monitorar Uso de Créditos
```sql
-- Verificar uso de warehouse
SELECT 
    warehouse_name,
    credits_used,
    bytes_scanned,
    percentage_scanned_from_cache
FROM table(information_schema.warehouse_metering_history(
    date_range_start=>dateadd('hours', -24, current_timestamp()),
    date_range_end=>current_timestamp()
));
```

## 6. Solução de Problemas Comuns

### 6.1 Erro de Conexão
**Sintoma**: `Failed to connect to Snowflake`
**Solução**:
- Verificar se o Account URL está correto
- Confirmar se o usuário e senha estão corretos
- Verificar se o warehouse está ativo

### 6.2 Erro de Permissão
**Sintoma**: `Access denied`
**Solução**:
- Verificar se o role tem permissões adequadas
- Confirmar se o warehouse está disponível para o usuário
- Verificar se o database existe e está acessível

### 6.3 Erro de Warehouse
**Sintoma**: `Warehouse not found`
**Solução**:
- Criar o warehouse se não existir
- Verificar se o nome está correto no .env
- Confirmar se o warehouse está ativo

## 7. Comandos Úteis do Snowflake

### 7.1 Queries de Monitoramento
```sql
-- Verificar warehouses disponíveis
SHOW WAREHOUSES;

-- Verificar databases
SHOW DATABASES;

-- Verificar usuário atual
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();

-- Verificar uso de créditos
SELECT 
    warehouse_name,
    credits_used,
    bytes_scanned
FROM table(information_schema.warehouse_metering_history(
    date_range_start=>dateadd('hours', -1, current_timestamp()),
    date_range_end=>current_timestamp()
));
```

### 7.2 Queries de Manutenção
```sql
-- Limpar dados antigos (opcional)
DELETE FROM task_results 
WHERE created_at < DATEADD(day, -30, CURRENT_TIMESTAMP());

-- Verificar tamanho das tabelas
SELECT 
    table_name,
    bytes,
    row_count
FROM information_schema.tables 
WHERE table_schema = 'PUBLIC'
ORDER BY bytes DESC;
```

## 8. Próximos Passos

1. **Teste a aplicação**:
   ```bash
   source .venv/bin/activate
   python main.py
   ```

2. **Inicie o worker do Celery**:
   ```bash
   celery -A worker worker --loglevel=info
   ```

3. **Monitore os logs** para verificar se as tarefas estão sendo processadas

4. **Verifique os dados** no Snowflake para confirmar que estão sendo salvos

## 9. Dicas de Otimização

### 9.1 Configuração de Warehouse
- Use `X-Small` para desenvolvimento
- Use `Small` ou `Medium` para produção
- Configure auto-suspend para economizar créditos

### 9.2 Monitoramento de Custos
- Monitore o uso de créditos regularmente
- Use queries otimizadas para reduzir custos
- Configure alertas de uso excessivo

### 9.3 Segurança
- Use roles específicos para diferentes usuários
- Configure network policies se necessário
- Monitore logs de acesso

## 10. Suporte

Se encontrar problemas:
1. Verifique os logs do aplicativo
2. Teste a conexão manualmente
3. Verifique as permissões no Snowflake
4. Consulte a documentação oficial do Snowflake

**Documentação Oficial**: https://docs.snowflake.com/ 