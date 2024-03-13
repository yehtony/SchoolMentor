import requests
import json
from typing import List, Any, Dict
import os

def genExample(example: Dict[str, str]): return  [
    {"role": "user", "content": example["question"]},
    {"role": "assistant", "content": example["answer"]}
]
def callGpt(
        messages: List[Any],
        temperature: float = 0.3
    ) -> str:
    url: str = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": temperature,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "max_tokens": 250,
        "presence_penalty": 0,
        "frequency_penalty": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ os.environ.get("ChatGPTApiKey", "None")
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        return str(response.json()['choices'][0]['message']['content'])
    except:
        return "ERROR:"+str(response.text)


def callGPT_finetuneQuestion(userText: str) -> str:
        return callGpt([
                {
                    "role": "system",
                    "content": """
                    我們是一個自然科的討論課程，你是這堂課的教師，你負責將學生的問題優化另一個問題，請理解學生的問題後提出更明確的問題。
                    切記我們不提出自然以外的內容，所有提出的問題維持在自然領域之中。

                    ### examples:
                    user: 蜘蛛 八隻腳
                    assistant: 請問蜘蛛是八隻腳嗎?
                    """
                },
                {"role": "user", "content": userText}
        ],0.3)

def callGPT_AnswerQuestion(examples: List[Dict[str, str]],userText: str) -> (str, List[Dict[str,str]]):

        body: List[Dict[str,str]] = [
                {
                    "role": "system",
                    "content": """
                    我們是一個自然科的討論課程，你是這堂課的教師，你負責回應學生的問題，請理解學生的問題後提出明確的。
                    切記我們不提出自然以外的內容，所有確保回應維持在自然領域之中，並在200個字內回答問題。
                    """
                }
        ]

        for e in examples:
            body.extend(genExample(e))
        
        body.extend([{"role": "user", "content": userText}])
        return callGpt(body,0.7), body
        