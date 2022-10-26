from flask import Flask
from threading import Thread

app = Flask('')
code = 200

@app.route('/')
def main():
  return f"Water Reminder Discord Bot Client: Status {code}", code

def run():
    app.run(host="0.0.0.0", port="8080")

def change_code(status_code: int = 0):
    global code
    code = status_code

def host(no_thread: bool = False):
    if no_thread: run()  # Runs directly
    else:
        server = Thread(target=run)
        server.start()
