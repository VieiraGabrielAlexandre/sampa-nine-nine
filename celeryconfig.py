
# Apply fix for urllib3.packages.six.moves before any other imports
import agents.six_fix

# Celery configuration
broker_url = 'redis://localhost:6380/0'
result_backend = 'redis://localhost:6380/0'
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Import tasks modules to ensure they are registered with Celery
imports = [
    'agents.campaign_creator',
    'agents.trading_agent',
]