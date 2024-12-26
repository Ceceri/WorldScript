from app.core.config import settings
from openai import OpenAI
import json

# 初始化 OpenAI 客户端
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def call_llm(title: str, description: str, background: str, attributes: list):
    """
    调用 LLM 接口生成内容。
    """
    try:
        # 将属性信息格式化为字符串
        attributes_info = ', '.join([f"{attr['name']}: 初始值 {attr['initial_value']}" for attr in attributes])

        user_message = f"""
        我需要你帮助生成游戏事件和选项。以下是游戏的详细信息：
        
        游戏背景：{background}
        事件标题：{title}
        事件描述：{description}
        游戏属性：{attributes_info}

        任务：
        1. 请根据上述信息扩展事件的描述，使其更加生动、有趣，同时与游戏背景一致。用 "扩展描述：" 开头提供扩展描述。
        2. 根据扩展描述生成 2 到 4 个选项。每个选项应包含以下信息：
           - 选项描述，用 "选项描述：" 开头。
           - 对玩家的影响描述，用 "影响描述：" 开头。
           - 属性变化，以 JSON 格式描述 (例如：{{"属性名": {{"operation": "add", "value": 10}}}})。用 "属性变化：" 开头。
             注意：仅包含你认为会因该选择而实际发生变化的属性。如果某个选择不会影响任何属性，则可以提供空的属性变化对象 {{}}。

        请严格按照以下格式输出：
        扩展描述：
        [扩展的事件描述]

        选项 1:
        选项描述：[选项1的描述]
        影响描述：[选项1的影响]
        属性变化：[选项1的属性变化]

        选项 2:
        选项描述：[选项2的描述]
        影响描述：[选项2的影响]
        属性变化：[选项2的属性变化]

        如果有更多选项，可以继续编号生成。
        """

        # 调用 OpenAI 接口
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_message},
            ],
            model="gpt-4",  # 使用更高质量的模型
        )

        # 正确访问 response 的内容
        generated_message = response.choices[0].message
        content = generated_message.content.strip()  # 获取生成的文本
        return parse_generated_text(content)

    except Exception as e:
        print(f"Error calling LLM: {e}")
        raise RuntimeError(f"Error generating content: {e}")


def parse_generated_text(content: str):
    try:
        print("原始内容:", content)  # 添加日志输出原始内容
        parts = content.split("\n\n")
        extended_description = parts[0].replace("扩展描述：", "").strip()

        options = []
        for part in parts[1:]:
            if part.startswith("选项"):
                lines = part.split("\n")
                text = lines[1].replace("选项描述：", "").strip()
                impact_description = lines[2].replace("影响描述：", "").strip()

                # 使用 json.loads 解析属性变化
                attribute_changes_dict = json.loads(lines[3].replace("属性变化：", "").strip())
                print("解析的属性变化:", attribute_changes_dict)  # 添加日志输出解析的属性变化

                # 确保属性变化是字典格式，并将 value 转换为字符串
                attribute_changes = {
                    key: {"operation": value["operation"], "value": str(value["value"])}
                    for key, value in attribute_changes_dict.items()
                }

                options.append({
                    "text": text,
                    "impact_description": impact_description,
                    "result_attribute_changes": attribute_changes,
                })

        return extended_description, options

    except Exception as e:
        print(f"Error parsing generated text: {e}")
        raise RuntimeError("Error parsing generated content")
