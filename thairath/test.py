from flask import Flask,request
import subprocess
import threading
from collections import deque
app = Flask(__name__)
scrape_in_progress = False
scrape_complete = False
queue = deque()
def progressFinishCheck():
    global scrape_in_progress
    global queue
    if len(queue) == 0:
        scrape_in_progress = False
    print('gets called')
def popenAndCall(onExit, *popenArgs, **popenKWArgs):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.

    Use it exactly the way you'd normally use subprocess.Popen, except include a
    callable to execute as the first argument. onExit is a callable object, and
    *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs, popenKWArgs):
        proc = subprocess.Popen(*popenArgs, **popenKWArgs)
        proc.wait()
        onExit()
        return

    thread = threading.Thread(target=runInThread,
                              args=(onExit, popenArgs, popenKWArgs))
    thread.start()

    return thread # returns immediately after the thread starts
@app.route('/')
def hello_world():
    global scrape_in_progress
    global scrape_complete
    global queue
    search_field = request.args.get('search_field')
    queue.append(search_field)
    if not scrape_in_progress:
        scrape_in_progress = True
        while len(queue)>0:
            field = queue.pop()
            popenAndCall(progressFinishCheck, ['python3', 'main2.py', field], cwd='.')
            # popenAndCall(progressFinish,['python3','main2.py','อนุทิน'],cwd='./thairath')
    return 'SCRAPE IN PROGRESS'

if __name__ == '__main__':
    app.run()