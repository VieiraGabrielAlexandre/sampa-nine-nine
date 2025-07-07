# Checklist: Dados Necessários do Snowflake

## ✅ Dados que você precisa obter da sua conta Snowflake:

### 1. **Account URL**
- Acesse: https://app.snowflake.com
- Faça login
- Clique no seu nome de usuário (canto superior direito)
- Selecione "Account"
- Copie o **Account URL** (exemplo: `xy12345.snowflakecomputing.com`)

### 2. **Dados de Login**
- **Username**: Seu nome de usuário
- **Password**: Sua senha
- **Role**: Geralmente `ACCOUNTADMIN` (padrão)

### 3. **Warehouse**
- Nome: `COMPUTE_WH` (ou criar um com este nome)
- Tamanho: `X-Small` (para começar)
- Auto-suspend: `10 minutes`

### 4. **Database**
- Nome: `AIRDROP_OPTIMIZER`
- Schema: `PUBLIC` (padrão)

## 📝 Arquivo .env

Crie um arquivo `.env` na raiz do projeto com:

```bash
SNOWFLAKE_ACCOUNT=seu_account.snowflakecomputing.com
SNOWFLAKE_USER=seu_username
SNOWFLAKE_PASSWORD=sua_senha
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=AIRDROP_OPTIMIZER
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

## 🧪 Teste Rápido

Após configurar o `.env`, execute:

```bash
source .venv/bin/activate
python test_snowflake_connection.py
```

## 🔧 Se algo der errado:

1. **Verifique se o warehouse está ativo** no Snowflake
2. **Confirme se o database existe**
3. **Teste a conexão manualmente** no Snowflake Worksheet
4. **Verifique as permissões** do seu usuário

## 📞 Suporte

- **Documentação**: https://docs.snowflake.com/
- **Interface Web**: https://app.snowflake.com
- **Comunidade**: https://community.snowflake.com/ 