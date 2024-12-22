from app.core.config import settings
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def call_llm(title: str, description: str, background: str):
    """
    调用 LLM 接口生成内容。
    """
    try:
        user_message = f"""
        我需要你帮助生成游戏事件和选项。以下是游戏的详细信息：
        
        游戏背景：{background}
        事件标题：{title}
        事件描述：{description}

        任务：
        1. 请根据上述信息扩展事件的描述，使其更加生动、有趣，同时与游戏背景一致。用 "扩展描述：" 开头提供扩展描述。
        2. 根据扩展描述生成 2 到 4 个选项。每个选项应包含以下信息：
           - 选项描述，用 "选项描述：" 开头。
           - 对玩家的影响描述，用 "影响描述：" 开头。
           - 属性变化 (可选)，以 JSON 格式描述 (例如：{{"属性名": {{"operation": "add", "value": 10}}}})。用 "属性变化：" 开头。

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
        parts = content.split("\n\n")
        extended_description = parts[0].replace("扩展描述：", "").strip()

        options = []
        for part in parts[1:]:
            if part.startswith("选项"):
                lines = part.split("\n")
                text = lines[1].replace("选项描述：", "").strip()
                impact_description = lines[2].replace("影响描述：", "").strip()

                # 解析属性变化
                attribute_changes = eval(lines[3].replace("属性变化：", "").strip())  # 使用 eval 解析 JSON
                
                # 确保属性变化中的值是字符串类型
                for key in attribute_changes:
                    attribute_changes[key]["value"] = str(attribute_changes[key]["value"])

                options.append({
                    "text": text,
                    "impact_description": impact_description,
                    "result_attribute_changes": attribute_changes,
                })

        return extended_description, options

    except Exception as e:
        print(f"Error parsing generated text: {e}")
        raise RuntimeError("Error parsing generated content")
