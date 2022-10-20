import os
os.system('pip install flask[async]')

from flask import Flask
from threading import Thread
from helper import restartHuburt

app = Flask('')

@app.route('/')
async def home():
    return "I'm alive"
@app.route('/restart')
async def restart():
    await restartHuburt()
    return "Noted"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()