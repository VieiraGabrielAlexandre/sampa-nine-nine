from celery import Celery

app = Celery('worker')
app.config_from_object('celeryconfig')

# Import tasks to register them with Celery
import agents.campaign_creator
import agents.trading_agent

if __name__ == '__main__':
    app.start()
