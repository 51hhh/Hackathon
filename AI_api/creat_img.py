import base64
import os
import argparse
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    """保存二进制文件

    Args:
        file_name (str): 文件保存路径
        data (bytes): 二进制数据
    """
    # 打开文件并以二进制写入模式保存数据
    f = open(file_name, "wb")
    f.write(data)
    f.close()


def generate(prompt: str, output_file: str, input_image_path: str = None):
    # 设置Google AI API密钥
    api_key ="AIzaSyA2AG44rdblnoR3S3ESJCSluPUYKpJVwGA"

    # 初始化Google AI客户端
    client = genai.Client(api_key=api_key)

    # 构造内容对象，包含用户提示词
    contents = []
    
    # 如果提供了输入图片，则添加到内容中
    if input_image_path and os.path.exists(input_image_path):
        with open(input_image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
            
        # 获取文件扩展名以确定MIME类型
        mime_type = "image/jpeg"
        if input_image_path.lower().endswith(".png"):
            mime_type = "image/png"
        elif input_image_path.lower().endswith(".gif"):
            mime_type = "image/gif"
            
        contents.append(types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="请根据这张图片进行修改：" + prompt),
                types.Part(inline_data=types.Blob(data=image_data, mime_type=mime_type))
            ],
        ))
    else:
        # 如果没有提供图片，则只使用文本提示
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
    
    # 配置生成内容的参数
    generate_content_config = types.GenerateContentConfig(
        temperature=1,           # 控制输出随机性
        top_p=0.95,              # 核采样参数
        top_k=40,                # 限制考虑的最高概率词汇数
        max_output_tokens=8192,  # 最大输出token数
        response_modalities=[    # 响应模态类型
            "image",
            "text",
        ],
        response_mime_type="text/plain",  # 响应MIME类型
    )

    # 流式生成内容，使用gemini-2.0-flash-exp模型
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash-exp",
        contents=contents,
        config=generate_content_config,
    ):
        # 检查返回的数据块是否包含有效内容
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
            
        # 遍历所有parts分别处理文本和图像
        for part in chunk.candidates[0].content.parts:
            if part.inline_data:
                save_binary_file(
                    output_file, part.inline_data.data
                )
                print(
                    "图片文件已保存："
                    f" {part.inline_data.mime_type} 保存在"
                    f" : {output_file}"
                )
            elif part.text:
                print(part.text)

def main():
    # 硬编码提示词和输出文件路径

    # prompt = "请绘制一只猫，场景中需要有树木、草地，天空"
    # output_file = "img.png"
    # input_image = None  # 可以指定要修改的输入图片路径
    
    prompt = "请转换为卡通形象的猫"
    output_file = "img.png"
    input_image = "img.png"  # 可以指定要修改的输入图片路径

    # 调用生成函数
    generate(prompt, output_file, input_image)


# 程序入口点
if __name__ == "__main__":
    main()
