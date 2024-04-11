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
import json
import os


def send(d: CollectingDispatcher, obj: Any): d.utter_message(str(obj))
def getStage(t: Tracker): return t.get_slot('stage')
def getUserLatestMEG(t: Tracker): return t.latest_message

class ActionFAQ(Action):

    def name(self) -> Text:
        return "action_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        obj_TLM =getUserLatestMEG(tracker)

        faqRanking: list[Dict[str,Any]] = obj_TLM["response_selector"]['faq']['ranking']
        userText: str = obj_TLM["text"]
        topOneKey: str = faqRanking[0]['intent_response_key'][4:]
        topOneConf: float = faqRanking[0]['confidence']
        examples: List[Dict[str, str]] = getKN(topOneKey)
        result, rqBody = callGPT_AnswerQuestion(examples, userText)
        dispatcher.utter_message(text=result)
        if os.environ.get("ActionServerMode", None) == "debug":
            dispatcher.utter_message(text=str(rqBody))

        stage = getStage(tracker)
        # dispatcher.utter_message(text="get_slot(newQuestion): "+str(slotNewQuestion))
        # dispatcher.utter_message(text="get_slot(newQuestion): "+str(userContent))

        # dispatcher.utter_message(text=f"text_latest_message"+text_latest_message)
        # gptResponse = callGPT_finetuneQuestion(userContent)
        # dispatcher.utter_message(text=gptResponse)
        return [
            SlotSet("stage", "CustomAction")
        ]

class ActionDivergentThinkingZero(Action):
    def name(self) -> Text:
        return "divergentthinkingzero"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="想法發散 Meta-Talk")
        return []
