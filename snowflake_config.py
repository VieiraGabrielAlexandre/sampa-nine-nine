"""
Snowflake Configuration Module

This module provides configuration and utilities for connecting to Snowflake
as an alternative to Redis for data storage and task management.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector import SnowflakeConnection
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnowflakeConfig:
    """
    Configuration class for Snowflake connection and settings.
    """
    
    def __init__(self):
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.user = os.getenv('SNOWFLAKE_USER')
        self.password = os.getenv('SNOWFLAKE_PASSWORD')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
        self.database = os.getenv('SNOWFLAKE_DATABASE', 'AIRDROP_OPTIMIZER')
        self.schema = os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
        self.role = os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
        
    def get_connection_params(self) -> Dict[str, Any]:
        """
        Get connection parameters for Snowflake.
        
        Returns:
            Dict containing connection parameters
        """
        return {
            'account': self.account,
            'user': self.user,
            'password': self.password,
            'warehouse': self.warehouse,
            'database': self.database,
            'schema': self.schema,
            'role': self.role
        }
    
    def validate_config(self) -> bool:
        """
        Validate that all required Snowflake configuration is present.
        
        Returns:
            bool: True if configuration is valid
        """
        required_fields = ['account', 'user', 'password']
        missing_fields = [field for field in required_fields if not getattr(self, field)]
        
        if missing_fields:
            logger.error(f"Missing required Snowflake configuration: {missing_fields}")
            return False
            
        return True

class SnowflakeManager:
    """
    Manager class for Snowflake operations.
    """
    
    def __init__(self, config: Optional[SnowflakeConfig] = None):
        self.config = config or SnowflakeConfig()
        self.connection: Optional[SnowflakeConnection] = None
        
    def connect(self) -> SnowflakeConnection:
        """
        Establish connection to Snowflake.
        
        Returns:
            SnowflakeConnection: Active connection
        """
        if not self.config.validate_config():
            raise ValueError("Invalid Snowflake configuration")
            
        try:
            self.connection = snowflake.connector.connect(
                **self.config.get_connection_params()
            )
            logger.info("Successfully connected to Snowflake")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            raise
    
    def disconnect(self):
        """Close Snowflake connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Disconnected from Snowflake")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> Any:
        """
        Execute a query on Snowflake.
        
        Args:
            query (str): SQL query to execute
            params (Dict, optional): Query parameters
            
        Returns:
            Query result
        """
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def create_tables(self):
        """Create necessary tables for the airdrop optimizer."""
        tables = {
            'task_queue': """
                CREATE TABLE IF NOT EXISTS task_queue (
                    task_id VARCHAR(255) PRIMARY KEY,
                    task_name VARCHAR(255) NOT NULL,
                    task_data TEXT,
                    status VARCHAR(50) DEFAULT 'PENDING',
                    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                )
            """,
            'task_results': """
                CREATE TABLE IF NOT EXISTS task_results (
                    task_id VARCHAR(255) PRIMARY KEY,
                    result_data TEXT,
                    status VARCHAR(50) DEFAULT 'SUCCESS',
                    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                    execution_time FLOAT
                )
            """,
            'trading_metrics': """
                CREATE TABLE IF NOT EXISTS trading_metrics (
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
            """,
            'campaign_data': """
                CREATE TABLE IF NOT EXISTS campaign_data (
                    campaign_id VARCHAR(255) PRIMARY KEY,
                    token VARCHAR(50) NOT NULL,
                    volume_required FLOAT NOT NULL,
                    reward FLOAT NOT NULL,
                    period_days INTEGER DEFAULT 7,
                    viability_score FLOAT DEFAULT 0.0,
                    status VARCHAR(50) DEFAULT 'ACTIVE',
                    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                )
            """
        }
        
        for table_name, create_sql in tables.items():
            try:
                self.execute_query(create_sql)
                logger.info(f"Created table: {table_name}")
            except Exception as e:
                logger.error(f"Error creating table {table_name}: {str(e)}")

# Global instance
snowflake_manager = SnowflakeManager() 