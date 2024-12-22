import openai
import json
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_event_description(context: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "你是一个游戏事件描述生成器。"},
          {"role": "user", "content": f"根据以下上下文生成一个游戏事件描述：\n{context}\n要求中文描述。"}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

def generate_options(context: str) -> list:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "你是一个游戏选项生成器，会返回JSON格式的选项数组。"},
          {"role": "user", "content": f"根据以下上下文生成3个游戏选项，每个选项用JSON对象表示，包括text和result_attribute_changes字段。例如：[\n{{\"text\":\"前往市场\",\"result_attribute_changes\":{{\"wealth\":+10}}}},\n{{\"text\":\"与村民交谈\",\"result_attribute_changes\":{{\"intelligence\":+2}}}},\n{{\"text\":\"休息一晚\",\"result_attribute_changes\":{{\"strength\":+5}}}}\n]\n上下文：\n{context}\n请直接返回JSON数组。"}
        ],
        max_tokens=300,
        temperature=0.7
    )
    response = completion.choices[0].message.content.strip()
    try:
        options = json.loads(response)
        return options
    except:
        raise ValueError("LLM返回的选项格式不是有效的JSON，请检查提示或重新生成。")

def generate_ending(context: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "你是一个游戏结局描述生成器。"},
          {"role": "user", "content": f"根据以下上下文生成一个中文游戏结局描述：\n{context}"}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()
