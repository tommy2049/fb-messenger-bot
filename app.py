import os
import sys
import json
#import pexpect
# from pymessenger.bot import Bot

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        # calling helper function to extract intent from message
                        access_token = "EAAGfba4cPrgBAM6DKrGOiOFj5AfU2urmR1irqgTLXtEnk9QhgsP78NZCuVl477fFwBtj6tupSoY5WELTbZCKJiq9JOELoNnQYuf5RamcJSDnerrv1286HptNSLSWrUsPqhIh6UHvDg1M7DhMNaQAcgkrMhFxTGFjGZCtc8NtZBllUP29QS1ZA"
                        nlu(sender_id, message_text, access_token)
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_image(sender_id, image_url, access_token):
        headers = {'Content-Type': 'application/json',}
        data = '{\n  "recipient":{\n    "id":'+sender_id+'\n  },\n  "message":{ "attachment":{"type":"image","payload":{"url": "'+image_url+'"}}}\n\n}'
        requests.post("https://graph.facebook.com/v2.6/me/messages?access_token="+access_token, headers=headers, data=data)

# def feedback():
#     feedback = ['feedback']
#     if any(substring in message for substring in feedback):
#     send_message(sender_id, "Please let me know what I can work on!")

# simple natural language processing function, can not handle long conversations
def nlu(sender_id, message, access_token):
    greetings = ['hello', 'hi', 'how are you']
    general_tips = ['tips', 'advise', 'ideas', 'first date']
    male = ['guy','man']
    female = ['girl','lady']
    restaurant = ['food', 'hungry', 'adventurous']
    sushi = ['sushi']
    feedback = ['feedback']
    if any(substring in message for substring in greetings):
        send_message(sender_id, "Hi there! I'm an advisor bot from Onet Marriage Group, you can ask me questions and tips like what you should wear on your first date, please also provide feedback on how I can improve ;)")
    if any(substring in message for substring in general_tips):
        if any(substring in message for substring in male):
            send_message(sender_id, "Girls like guys who dress tastefully, for example smart casual makes you appear smart and attractive")
            send_image(sender_id, "https://cache.mrporter.com/journal-images/production/10873276-1d9a-4372-9834-00ba5cd7b867", access_token)
        if any(substring in message for substring in female):
            send_message(sender_id, "dresses in the summer is a great idea, it's light and makes you look cute ;)")
            send_image(sender_id, "https://s-media-cache-ak0.pinimg.com/originals/54/80/87/548087e58e8ad87813cc7dc4920d4142.jpg", access_token)
    if any(substring in message for substring in restaurant):
        send_message(sender_id, "Please check out alcatraz-er-restaurant-tokyo-japan-1, they serve a variety of interesting food including funky drinks and blue curry.")
        send_image(sender_id, "https://media-cdn.tripadvisor.com/media/photo-s/05/c9/46/88/alcatraz-er.jpg", access_token)
        send_image(sender_id, "http://for91days.com/photos/Tokyo/Alacatraz%20ER%20Restaurant%20Tokyo/Alacatraz%20ER%20Restaurant%20Tokyo%2011%2020140403%20for91days.com.JPG", access_token)
    if any(substring in message for substring in sushi):
        send_message(sender_id, "Heiroku sushi is a great conveyor belt sushi located at 150-0001 Tokyo, Shibuya, Jingumae, 5 chrome-8-5!")
        send_image(sender_id, "https://resources.matcha-jp.com/archive_files/jp/2014/02/DSCF0578.jpg", access_token)
    # if any(substring in message for substring in feedback):
    #     send_feedback("Please learn to speak Japanese\n")
    #     send_message(sender_id, "Thank you for the feedback!")

        
# def send_feedback(feedback_message):
#     with open("feedback.txt", "a") as myfile:
#         myfile.write(feedback_message)
#     child=pexpect.spawn('scp feedback.txt ar-luojun01@stg-loginjpe1101z.stg.jp.local:/home/ar-luojun01')
#     child.expect('ar-luojun01@stg-acap101zd\'s password:')
#     time.sleep(45)
#     child.sendline('951127Da!')


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)

