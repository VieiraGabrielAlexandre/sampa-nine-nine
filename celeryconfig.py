# Apply fix for urllib3.packages.six.moves before any other imports
import agents.six_fix

# Celery configuration with Snowflake only
# Using Snowflake for both broker and backend

# Add the current directory to Python path to find snowflake_backend module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our custom backend
from snowflake_backend import SnowflakeBackend

# Broker configuration - using memory broker for now
broker_url = 'memory://'

# Result backend using Snowflake - pass as string to avoid import issues
result_backend = 'snowflake_backend.SnowflakeBackend'

accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Task routing
task_routes = {
    'agents.campaign_creator.*': {'queue': 'campaign_queue'},
    'agents.trading_agent.*': {'queue': 'trading_queue'},
    'agents.prediction_agent.*': {'queue': 'prediction_queue'},
}

# Import tasks modules to ensure they are registered with Celery
imports = [
    'agents.campaign_creator',
    'agents.trading_agent',
    'agents.prediction_agent',
]

# Task result settings
task_ignore_result = False
task_store_errors_even_if_ignored = True

# Worker settings
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000
worker_disable_rate_limits = False

# Result backend settings
result_expires = 3600  # Results expire after 1 hour
result_persistent = True