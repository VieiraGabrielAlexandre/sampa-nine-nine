#!/usr/bin/env python3
"""
Migration Script: Redis to Snowflake

This script helps migrate from Redis to Snowflake for the Airdrop Optimizer project.
It sets up the necessary Snowflake tables and provides utilities for data migration.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from snowflake_config import snowflake_manager, SnowflakeConfig
# from snowflake_backend import snowflake_backend  # Removido pois não é necessário

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RedisToSnowflakeMigrator:
    """
    Handles migration from Redis to Snowflake.
    """
    
    def __init__(self):
        self.snowflake = snowflake_manager
        self.config = SnowflakeConfig()
        
    def validate_environment(self) -> bool:
        """
        Validate that all required environment variables are set.
        
        Returns:
            bool: True if environment is properly configured
        """
        logger.info("Validating environment configuration...")
        
        required_vars = [
            'SNOWFLAKE_ACCOUNT',
            'SNOWFLAKE_USER', 
            'SNOWFLAKE_PASSWORD'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            logger.error("Please set these variables in your .env file")
            return False
        
        logger.info("Environment validation passed")
        return True
    
    def setup_snowflake_database(self) -> bool:
        """
        Set up Snowflake database and tables.
        
        Returns:
            bool: True if setup was successful
        """
        try:
            logger.info("Setting up Snowflake database...")
            
            # Connect to Snowflake
            self.snowflake.connect()
            
            # Create database if it doesn't exist
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {self.config.database}"
            self.snowflake.execute_query(create_db_query)
            logger.info(f"Database {self.config.database} created/verified")
            
            # Use the database
            use_db_query = f"USE DATABASE {self.config.database}"
            self.snowflake.execute_query(use_db_query)
            
            # Create schema if it doesn't exist
            create_schema_query = f"CREATE SCHEMA IF NOT EXISTS {self.config.schema}"
            self.snowflake.execute_query(create_schema_query)
            logger.info(f"Schema {self.config.schema} created/verified")
            
            # Use the schema
            use_schema_query = f"USE SCHEMA {self.config.schema}"
            self.snowflake.execute_query(use_schema_query)
            
            # Create tables
            self.snowflake.create_tables()
            
            logger.info("Snowflake database setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up Snowflake database: {str(e)}")
            return False
    
    def test_snowflake_connection(self) -> bool:
        """
        Test the Snowflake connection and basic operations.
        
        Returns:
            bool: True if connection test passed
        """
        try:
            logger.info("Testing Snowflake connection...")
            
            # Test basic query
            test_query = "SELECT CURRENT_TIMESTAMP() as current_time, CURRENT_USER() as current_user"
            cursor = self.snowflake.execute_query(test_query)
            result = cursor.fetchone()
            
            if result:
                logger.info(f"Connection test passed. Current time: {result[0]}, User: {result[1]}")
                return True
            else:
                logger.error("Connection test failed - no result returned")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def migrate_sample_data(self) -> bool:
        """
        Migrate sample data to Snowflake for testing.
        
        Returns:
            bool: True if migration was successful
        """
        try:
            logger.info("Migrating sample data to Snowflake...")
            
            # Sample campaign data
            sample_campaigns = [
                {
                    'campaign_id': 'camp_001',
                    'token': 'BTC',
                    'volume_required': 1000.0,
                    'reward': 50.0,
                    'period_days': 7,
                    'viability_score': 8.5,
                    'status': 'ACTIVE'
                },
                {
                    'campaign_id': 'camp_002', 
                    'token': 'ETH',
                    'volume_required': 500.0,
                    'reward': 20.0,
                    'period_days': 5,
                    'viability_score': 7.2,
                    'status': 'ACTIVE'
                }
            ]
            
            # Insert sample campaigns
            for campaign in sample_campaigns:
                query = """
                    INSERT INTO campaign_data 
                    (campaign_id, token, volume_required, reward, period_days, viability_score, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                self.snowflake.execute_query(query, (
                    campaign['campaign_id'],
                    campaign['token'],
                    campaign['volume_required'],
                    campaign['reward'],
                    campaign['period_days'],
                    campaign['viability_score'],
                    campaign['status']
                ))
            
            logger.info(f"Migrated {len(sample_campaigns)} sample campaigns")
            return True
            
        except Exception as e:
            logger.error(f"Error migrating sample data: {str(e)}")
            return False
    
    def verify_migration(self) -> bool:
        """
        Verify that the migration was successful.
        
        Returns:
            bool: True if verification passed
        """
        try:
            logger.info("Verifying migration...")
            
            # Check if tables exist and have data
            tables_to_check = ['campaign_data', 'task_queue', 'task_results', 'trading_metrics']
            
            for table in tables_to_check:
                query = f"SELECT COUNT(*) FROM {table}"
                cursor = self.snowflake.execute_query(query)
                count = cursor.fetchone()[0]
                logger.info(f"Table {table}: {count} records")
            
            logger.info("Migration verification completed")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying migration: {str(e)}")
            return False
    
    def run_migration(self) -> bool:
        """
        Run the complete migration process.
        
        Returns:
            bool: True if migration was successful
        """
        logger.info("Starting Redis to Snowflake migration...")
        
        # Step 1: Validate environment
        if not self.validate_environment():
            return False
        
        # Step 2: Test connection
        if not self.test_snowflake_connection():
            return False
        
        # Step 3: Setup database
        if not self.setup_snowflake_database():
            return False
        
        # Step 4: Migrate sample data
        if not self.migrate_sample_data():
            return False
        
        # Step 5: Verify migration
        if not self.verify_migration():
            return False
        
        logger.info("Migration completed successfully!")
        return True

def main():
    """Main function to run the migration."""
    migrator = RedisToSnowflakeMigrator()
    
    if migrator.run_migration():
        print("\n✅ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Update your .env file with your Snowflake credentials")
        print("2. Test the application with: python main.py")
        print("3. Start the worker with: celery -A worker worker --loglevel=info")
        print("4. Monitor the application logs for any issues")
    else:
        print("\n❌ Migration failed. Please check the logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 