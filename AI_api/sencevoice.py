import requests
import json
import logging

# 启用调试日志
logging.basicConfig(level=logging.DEBUG)

# 替换为您的 API 密钥
API_KEY = "sk-ukrvwweyscnelxjxohafljyugaezcuvfcmmdtynpmenyjxzc"

# SiliconFlow 语音转文字 API 端点
API_ENDPOINT = "https://api.siliconflow.cn/v1/audio/transcriptions"

# 音频文件路径
AUDIO_FILE_PATH = "./AI_api/1.mp3"  # 替换为您的音频文件路径

# 模型名称
MODEL_NAME = "FunAudioLLM/SenseVoiceSmall"

def transcribe_audio(audio_file_path, api_key, model_name):
    """
    使用 SiliconFlow API 将音频文件转录为文字。

    Args:
        audio_file_path (str): 音频文件的路径。
        api_key (str): 您的 SiliconFlow API 密钥。
        model_name (str): 使用的模型名称。

    Returns:
        str: 转录后的文字，如果发生错误则返回 None。
    """

    try:
        # 打开音频文件
        with open(audio_file_path, "rb") as audio_file:
            files = {
                "file": audio_file,  # 注意：这里参数名改为 "file"
                "model": (None, model_name) # 添加 model 参数, None 表示这不是一个文件
            }

            # 设置请求头，包含 API 密钥
            headers = {
                "Authorization": f"Bearer {api_key}",
            }

            # 发送 POST 请求
            logging.debug(f"发送请求到: {API_ENDPOINT}")
            response = requests.post(API_ENDPOINT, files=files, headers=headers)

            logging.debug(f"请求头: {response.request.headers}")
            #logging.debug(f"请求体: {response.request.body}")    # 打印请求体 (由于是 multipart/form-data，打印body可能不可读)
            logging.debug(f"响应状态码: {response.status_code}")
            logging.debug(f"响应内容: {response.text}")

            # 检查响应状态码
            response.raise_for_status()  # 如果状态码不是 200，则抛出 HTTPError 异常

            # 解析 JSON 响应
            response_json = response.json()

            # 根据 API 文档提取转录结果。
            transcription = response_json.get("text")

            return transcription

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None
    except FileNotFoundError:
        print(f"找不到文件: {audio_file_path}")
        return None
    except json.JSONDecodeError:
        print("JSON 解析出错，请检查API返回的数据格式")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


if __name__ == "__main__":
    # 调用转录函数
    transcription = transcribe_audio(AUDIO_FILE_PATH, API_KEY, MODEL_NAME)

    # 打印转录结果
    if transcription:
        print("转录结果:")
        print(transcription)
    else:
        print("转录失败。请检查错误信息。")
