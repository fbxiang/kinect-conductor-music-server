import json
from flask import Flask, request
from transition import FSM

def main():

    fsm = FSM()

    app = Flask(__name__)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')


    def catch_all(path):
        if path == 'next':
            try:
                return json.dumps(fsm.get_next())

            except:
                return '{}'

        else:

            return 'welcome'


    app.run()

if __name__ == '__main__':
    main()
