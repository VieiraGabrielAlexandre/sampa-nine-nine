# Redis to Snowflake Migration Guide

This guide explains how to migrate your Airdrop Optimizer project from Redis to Snowflake for data storage and task management.

## Overview

The migration involves replacing Redis (used for Celery message broker and result backend) with Snowflake for:
- **Task Results Storage**: Store Celery task results in Snowflake tables
- **Data Persistence**: Store trading metrics, campaign data, and other application data
- **Scalability**: Leverage Snowflake's cloud data warehouse capabilities

## Prerequisites

1. **Snowflake Account**: You need a Snowflake account with appropriate permissions
2. **Python Dependencies**: Install the required Snowflake packages
3. **Environment Variables**: Configure Snowflake connection parameters

## Migration Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The updated requirements.txt includes:
- `snowflake-connector-python==3.6.0`
- `snowflake-sqlalchemy==1.5.1`
- `sqlalchemy==2.0.23`

### 2. Configure Environment Variables

Create a `.env` file with your Snowflake credentials:

```bash
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=AIRDROP_OPTIMIZER
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN

# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 3. Run Migration Script

Execute the migration script to set up Snowflake:

```bash
python migrate_to_snowflake.py
```

This script will:
- Validate your environment configuration
- Test Snowflake connectivity
- Create the necessary database and tables
- Migrate sample data
- Verify the migration

### 4. Update Celery Configuration

The `celeryconfig.py` has been updated to use Snowflake as the result backend:

```python
# Result backend using Snowflake
result_backend = 'snowflake_backend.SnowflakeBackend'

# Broker configuration (still using Redis for now)
broker_url = 'redis://localhost:6380/0'
```

### 5. Test the Migration

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Start the Celery worker**:
   ```bash
   celery -A worker worker --loglevel=info
   ```

3. **Monitor logs** for any Snowflake-related errors

## Architecture Changes

### Before (Redis)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Celery    │    │    Redis    │    │ Application │
│   Worker    │◄──►│   Broker    │◄──►│    Tasks    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Redis     │
                   │   Results   │
                   └─────────────┘
```

### After (Snowflake)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Celery    │    │    Redis    │    │ Application │
│   Worker    │◄──►│   Broker    │◄──►│    Tasks    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Snowflake  │
                   │   Results   │
                   └─────────────┘
```

## Snowflake Tables

The migration creates the following tables:

### 1. `task_queue`
Stores pending and processing tasks
```sql
CREATE TABLE task_queue (
    task_id VARCHAR(255) PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    task_data TEXT,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
```

### 2. `task_results`
Stores completed task results
```sql
CREATE TABLE task_results (
    task_id VARCHAR(255) PRIMARY KEY,
    result_data TEXT,
    status VARCHAR(50) DEFAULT 'SUCCESS',
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    execution_time FLOAT
)
```

### 3. `trading_metrics`
Stores trading performance data
```sql
CREATE TABLE trading_metrics (
    agent_id VARCHAR(255) PRIMARY KEY,
    token VARCHAR(50) NOT NULL,
    total_trades INTEGER DEFAULT 0,
    successful_trades INTEGER DEFAULT 0,
    failed_trades INTEGER DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0,
    profit_loss FLOAT DEFAULT 0.0,
    duration_seconds FLOAT DEFAULT 0.0,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
```

### 4. `campaign_data`
Stores airdrop campaign information
```sql
CREATE TABLE campaign_data (
    campaign_id VARCHAR(255) PRIMARY KEY,
    token VARCHAR(50) NOT NULL,
    volume_required FLOAT NOT NULL,
    reward FLOAT NOT NULL,
    period_days INTEGER DEFAULT 7,
    viability_score FLOAT DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
```

## Key Components

### 1. SnowflakeConfig (`snowflake_config.py`)
- Manages Snowflake connection parameters
- Validates configuration
- Provides connection utilities

### 2. SnowflakeBackend (`snowflake_backend.py`)
- Custom Celery result backend
- Stores and retrieves task results
- Handles serialization/deserialization

### 3. SnowflakeManager (`snowflake_config.py`)
- Database operations
- Table creation and management
- Query execution utilities

## Benefits of Snowflake Migration

### 1. **Scalability**
- Cloud-native data warehouse
- Automatic scaling based on workload
- No infrastructure management

### 2. **Data Analytics**
- SQL-based analytics on task results
- Historical data analysis
- Performance monitoring

### 3. **Cost Efficiency**
- Pay-per-use pricing
- No upfront infrastructure costs
- Automatic resource optimization

### 4. **Reliability**
- Built-in fault tolerance
- Automatic backups
- High availability

## Monitoring and Maintenance

### 1. **Query Performance**
Monitor slow queries in Snowflake:
```sql
SELECT query_text, execution_time, bytes_scanned
FROM table(information_schema.query_history())
WHERE execution_time > 10000
ORDER BY execution_time DESC;
```

### 2. **Storage Usage**
Check table sizes:
```sql
SELECT table_name, bytes, row_count
FROM information_schema.tables
WHERE table_schema = 'PUBLIC'
ORDER BY bytes DESC;
```

### 3. **Task Monitoring**
Monitor task execution:
```sql
SELECT status, COUNT(*) as count
FROM task_results
WHERE created_at >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
GROUP BY status;
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify Snowflake credentials
   - Check network connectivity
   - Ensure account URL is correct

2. **Permission Errors**
   - Verify user has appropriate roles
   - Check warehouse access
   - Ensure database/schema permissions

3. **Performance Issues**
   - Monitor warehouse size
   - Check query optimization
   - Review indexing strategy

### Debug Commands

```bash
# Test Snowflake connection
python -c "from snowflake_config import snowflake_manager; snowflake_manager.connect()"

# Check table structure
python -c "from snowflake_config import snowflake_manager; snowflake_manager.execute_query('DESCRIBE TABLE task_results')"

# Verify data migration
python -c "from snowflake_config import snowflake_manager; cursor = snowflake_manager.execute_query('SELECT COUNT(*) FROM task_results'); print(cursor.fetchone())"
```

## Rollback Plan

If you need to rollback to Redis:

1. **Update Celery Configuration**:
   ```python
   # In celeryconfig.py
   broker_url = 'redis://localhost:6380/0'
   result_backend = 'redis://localhost:6380/0'
   ```

2. **Remove Snowflake Dependencies**:
   ```bash
   pip uninstall snowflake-connector-python snowflake-sqlalchemy
   ```

3. **Restart Services**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Next Steps

1. **Complete Migration**: Run the migration script
2. **Test Thoroughly**: Verify all functionality works
3. **Monitor Performance**: Track Snowflake usage and costs
4. **Optimize Queries**: Review and optimize database queries
5. **Scale as Needed**: Adjust warehouse size based on usage

## Support

For issues with the migration:
1. Check the logs for detailed error messages
2. Verify Snowflake connectivity
3. Review environment variable configuration
4. Test with the provided migration script 

```python
backend = SnowflakeBackend(app=None)
``` 