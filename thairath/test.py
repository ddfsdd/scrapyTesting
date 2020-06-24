from flask import Flask
from main2 import run_everything
app = Flask(__name__)
scrape_in_progress = False
scrape_complete = False

@app.route('/')
def hello_world():
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        y=run_everything()
        scrape_complete = True
    elif scrape_complete:
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'

    return 'yeah'