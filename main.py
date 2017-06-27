import logging
from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify_fb():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    	if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
    		return "Verification token mismatch", 403
    	return request.args["hub.challenge"], 200
    return "This is great :)", 200

@app.route('/', methods=['POST'])
def webhook():
        return "ok", 200

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
