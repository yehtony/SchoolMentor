import requests
import json
from typing import List, Any, Dict
import os


def genExample(example: Dict[str, str]):
    return [
        {"role": "user", "content": example["question"]},
        {"role": "assistant", "content": example["answer"]},
    ]


# def callGPT_finetuneQuestion(userText: str) -> str:
#         return callGpt(userText, [
#                 {
#                     "role": "system",
#                     "content": """
#                     我們是一個自然科的討論課程，你是這堂課的教師，你負責將學生的問題優化另一個問題，請理解學生的問題後提出更明確的問題。
#                     切記我們不提出自然以外的內容，所有提出的問題維持在自然領域之中。
#                     """
#                 },
#                 {"role": "user", "content": "蜘蛛 八隻腳"},
#                 {"role": "assistant", "content": "請問蜘蛛是八隻腳嗎"},
#                 {"role": "user", "content": userText}
#         ],0.3)


def callGPT_AnswerQuestion(
    examples: List[Dict[str, str]], userText: str
) -> (str, List[Dict[str, str]]):

    body: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": """
                    我們是一個自然科的討論課程，你是這堂課的教師，你負責回應學生的問題，請理解學生的問題後提出明確的。
                    切記我們不提出自然以外的內容，所有確保回應維持在自然領域之中，並在200個字內回答問題。
                    """,
        }
    ]

    for e in examples:
        body.extend(genExample(e))

    body.extend([{"role": "user", "content": userText}])
    return callGpt(userText, body, 0.7), body


def callGpt(userText: str, messages: List[Any], temperature: float = 0.3) -> str:
    url: str = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps(
        {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature,
            "top_p": 1,
            "n": 1,
            "stream": False,
            "max_tokens": 250,
            "presence_penalty": 0,
            "frequency_penalty": 0,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + os.environ.get("ChatGPTApiKey", "None"),
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        return str(response.json()["choices"][0]["message"]["content"])
    except:
        return "ERROR:" + str(response.text)


api_url = "http://ml.hsueh.tw/callapi/"


# Call API
def callNLPAPI(messages):
    payload = {
        "engine": "gpt-35-turbo-16k",
        "temperature": 0,
        "max_tokens": 1000,
        "top_p": 0.95,
        "top_k": 1,
        "roles": messages,
        "frequency_penalty": 0,
        "repetition_penalty": 1.03,
        "presence_penalty": 0,
        "stop": "",
        "past_messages": 0,
        "purpose": "dev",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # 發送 POST 請求
    response = requests.post(api_url, json=payload, headers=headers)

    # 取得回應內容
    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    return reply


def callNLP_ideaTopicRelevant(activity_topic, userText):
    message = [
        {
            "role": "system",
            "content": f"你要判斷學生回覆的想法是否有針對探究題目去做回答，如果有請回覆「是」，如果沒有請回覆「否」，除此之外不要回覆其他訊息。'\n'探究題目：「{activity_topic}」。",
        },
        {"role": "user", "content": userText},
    ]

    return callNLPAPI(message)


# def callNLP_ideaSummarize(idea_summary):
#     message = [
#         {
#             "role": "system",
#             "content": f"你要判斷學生回覆的想法是否有針對探究題目去做回答，如果有請回覆「是」，如果沒有請回覆「否」，除此之外不要回覆其他訊息。'\n'探究題目：「{idea_summary}」。",
#         },
#         {"role": "user", "content": idea_summary},
#     ]

#     return callNLPAPI(message)