from celery import Celery

app = Celery('worker')
app.config_from_object('celeryconfig')

# Apply fix for urllib3.packages.six.moves before importing other modules
#import agents.six_fix

# Import tasks to register them with Celery
import agents.campaign_creator
import agents.trading_agent

if __name__ == '__main__':
    app.start()
