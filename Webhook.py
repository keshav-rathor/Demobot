import json
import os
import traceback
# import datetime
from datetime import datetime

# import db as db
from flask import Flask
from flask import request, make_response
from pymongo import MongoClient

# Connecting to MongoDB database

MONGODB_URI = "mongodb://uptime:Basketball10@134.122.18.134:27017/admin"
client = MongoClient(MONGODB_URI, connectTimeoutMS=300000)
db = client.afla_db
questions = db.questions  # This collection contains all Question-Answer and Explanations
history = db.history# This collection stores all user chat history
feed=db.feedback


# Flask app should start in global layout
app = Flask(__name__)

def make_text_response(message):
    """
    This function takes a text (string) as an input and return a dictionary as per dialogflow requirement
    for text message.

    Args:
        message (str): A text message which to be send in reply

    Returns:
        dict: A dictionary as per dialogflow require to send a text message on Facebook Messenger.

    """
    return {
        "text": {
            "text": [
                message
            ]
        },
        "platform": "FACEBOOK"
    }

def make_video_response(video_url):
    """
    This function takes an url (string) as an input and return a dictionary as per dialogflow requirement for
    sending video message using Facebook Messenger.

    Args:
        video_url (str): URL of a Facebook video (video has to been from facebook and not from Youtube or any other sources).

    Returns:
        object (dict): A dictionary as per dialogflow require to send a video message on Facebook Messenger.
    """
    return {
        "payload": {
            "facebook": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                                "media_type": "video",
                                "url": video_url,
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": video_url,
                                        "title": "Watch"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        },
        "platform": "FACEBOOK"
    }

# def get_response_media(document, platform="FACEBOOK"):
#     """
#     This function takes a MongoDB document as an input (which is basically a dictionary) and checks whether
#     the document contains a Video URl or an Image URL and return a dictionary as per Dialogflow requirement
#     for video or an image.
#
#     Args:
#         document (dict): A dictionary we get from MongoDB database (explanations)
#         platform (str): A String which indicates the where the response should be posted (on Facebook or on Whatsapp).
#                         Use platform=`FACEBOOK` for Messenger and platform=None for Whatsapp.
#
#     Returns: A dictionary as per dialogflow require to send a video message on Facebook Messenger or on Whatsapp.
#     """
#
#     if document.get('image_url').split("/")[-3] == "videos":
#         if platform == "FACEBOOK":
#             return make_video_response(document.get("image_url"))
#         else:
#             return {
#                 "text": {
#                     "text": [
#                         document.get("video", "").replace("Plato", "Aflatoun") + "\nWhat would you like to do next? "
#                                                                                  "🤔\n7. Next Lesson ⛓\n8. Quiz Time 🔎"
#                                                                                  "\n4. Fun 🎢 "
#                     ]
#                 }
#             }
#     else:
#         if platform == "FACEBOOK":
#             return {
#                 "image": {
#                     "imageUri": document["image_url"]
#                 },
#                 "platform": "FACEBOOK"
#             }
#         else:
#             return {
#                 "text": {
#                     "text": [
#                         document.get("description") + "\n\nWhat would you like to do next? 🤔\n8. Quiz Time 🔎\n7. "
#                                                       "Next Lesson ⛓\n4. Fun 🎢 "
#                     ]
#                 }
#             }

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = process_request(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#t1_start = perf_counter_ns()
def process_request(req):


    # req.update({"datetime": datetime.date(datetime.now()).isoformat(),"time": datetime.time(datetime.now()).isoformat()})
    req.update({"date": datetime.date(datetime.now()).isoformat(), "time": datetime.time(datetime.now()).isoformat()})
    # today = date.today()
    # req.update({"today date":today.strftime("%B %d, %Y")})
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    timestamp1 = int(timestamp * (10 ** 3))
    req.update({"timestamp": timestamp1})
    req.update({"PlanUSA": 'DataPlanUSA'})
    #req.update({"feedback": feedback})
    # Inserting whole JSON object into databases
    try:
        feed.insert(req, check_keys=False)
    except:
        pass

    try:
        result = req.get("queryResult")
        action = result.get("action")


    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return {
            "fulfillmentText": "Oops... 😮 I am not able to help you at the moment, please try again..",
            "source": "webhook"
        }

#t1_stop = perf_counter_ns()
#time_session=((t1_stop-t1_start)/10**9)
#print(time_session)



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port {}".format(port))
    app.run(debug=False, port=port, host='0.0.0.0')
