# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .models import callGPT_AnswerQuestion
from .db import getKN
from .document import *
import base64
import json
import os


def decrypt(decoded_text):
    SecretKey = "20240116";
    decoded_text = base64.b64decode(decoded_text).decode('utf-8')
    result = ''
    for i in range(len(decoded_text)):
        charCode = ord(decoded_text[i]) ^ ord(SecretKey[i % len(SecretKey)])
        result += chr(charCode)
    assert len(result.split("."))==4
    return result
def send(d: CollectingDispatcher, obj: Any): d.utter_message(str(obj))
def getSlot_StoryStage(t: Tracker): return t.get_slot('story_stage')
def getUserLatestMEG(t: Tracker): return t.latest_message
def getUserText(t: Tracker): return getUserLatestMEG(t)["text"]
def getUserId(t: Tracker): return decrypt(t.sender_id)
client = createClient()
assert(checkClient(client))


class ActionFAQ(Action):

    def name(self) -> Text:
        return "action_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #
        REDISLABELSTATUS = getUserId(tracker)
        REDISLABELCOUNT = getUserId(tracker)+"-ROUNDCOUNT"
        userStatus = getByKey(client, REDISLABELSTATUS)
        userStatus = userStatus if userStatus is not None else {}
        roundCount = getByKey(client, REDISLABELCOUNT)
        roundCount = roundCount if roundCount is not None else 1


        #
        obj_TLM =getUserLatestMEG(tracker)
        faqRanking: list[Dict[str,Any]] = obj_TLM["response_selector"]['faq']['ranking']
        userText: str = obj_TLM["text"]
        topOneKey: str = faqRanking[0]['intent_response_key'][4:]
        topOneConf: float = faqRanking[0]['confidence']
        examples: List[Dict[str, str]] = getKN(topOneKey)
        # dispatcher.utter_message(text="*** Hi It's Action Server")
        # dispatcher.utter_message(text="*** topOneConf: "+str(topOneConf))
        # dispatcher.utter_message(text="*** faqRanking: "+str(faqRanking))
        if topOneConf > 0.9:
            result, rqBody = callGPT_AnswerQuestion(examples, userText)
            dispatcher.utter_message(text=result)
            if os.environ.get("ActionServerMode", None) == "debug":
                dispatcher.utter_message(text=str(rqBody))
            dispatcher.utter_message(text=str(examples))
        elif 0.75<topOneConf<=0.9:

            # dispatcher.utter_message(text=f"text_latest_message"+text_latest_message)
            result, rqBody = callGPT_finetuneQuestion(userText)
            dispatcher.utter_message(text=result)
            # dispatcher.utter_message(text=gptResponse)

            #
            # updateDocuments(client, [{"key":REDISLABELCOUNT, "value": roundCount+1}])


        return [
            SlotSet("stage", "CustomAction")
        ]