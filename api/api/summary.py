from flask import Blueprint, jsonify
import json
import os

summary_bp = Blueprint('summary_api', __name__)

MP3_DIR = './mp3'
METADATA_FILE = './mp3/mp3_metadata.json'

@summary_bp.route('/recordings')
def get_recordings():
    all_metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            all_metadata = json.load(f)

    recordings_list = []
    if os.path.exists(MP3_DIR):
        for filename in os.listdir(MP3_DIR):
            if filename.endswith('.mp3'):
                metadata = all_metadata.get(filename, {})
                
                # Generate a default title if not provided in metadata
                title = metadata.get('title', os.path.splitext(filename)[0].replace('_', ' '))
                
                # Generate a default date if not provided, try to parse from filename
                file_date = metadata.get('date')
                if not file_date:
                    try:
                        # Assuming filename format like YYYY_MM_DD.mp3
                        date_parts = os.path.splitext(filename)[0].split('_')
                        if len(date_parts) == 3:
                            file_date = f"{date_parts[0]}-{date_parts[1]}-{date_parts[2]}"
                    except:
                        file_date = "未知日期"

                recordings_list.append({
                    'id': filename, # Use filename as ID for stability
                    'title': title,
                    'date': file_date,
                    'duration': metadata.get('duration', '未知时长'),
                    'participants': metadata.get('participants', '未知参与者'),
                    'summary': metadata.get('summary', '无摘要信息。'),
                    'filename': filename # Store filename to link to detail
                })
    
    # Sort recordings by date, if dates are in YYYY-MM-DD format
    try:
        recordings_list.sort(key=lambda x: x['date'], reverse=True)
    except TypeError:
        # Fallback if dates are not consistently sortable
        pass

    return jsonify(recordings_list)

@summary_bp.route('/recordings/<string:filename>') # Change to string:filename
def get_recording_detail(filename):
    all_metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            all_metadata = json.load(f)

    metadata = all_metadata.get(filename) # Directly get metadata by filename

    if metadata:
        # Simulate transcription and AI summary
        transcription = f"这是音频文件 '{filename}' 的文字提取内容。它包含了会议的详细讨论，对啊，金华，您点击一下构建，然后选择一下。他说今天晚上是极客职夜，然后我告诉你个好事儿，嗯嗯，你说吧，好事是什么？什么好事什么好事？好事是今天晚上自己给自己做一些黑暗料理去喝啊，他说今天晚上要自己做。对啊，你这个东西能识别三个人说话，能能能能能你知道坏事是什么吗？能坏事什么？"
        ai_summary = f"这是音频文件 '{filename}' 的AI 总结。主要内容是关于项目Hackathon的进展会议"+"""
有人提到了一个操作步骤，让“金华”点击构建，然后进行选择。

会议中提到了一个活动，叫做“极客职夜”，就在今天晚上。

记录中出现了关于“好事”的对话，但具体内容似乎与做“黑暗料理”和“喝东西”有关。"""

        return jsonify({
            'id': filename, # Use filename as ID
            'title': metadata.get('title', os.path.splitext(filename)[0].replace('_', ' ')),
            'date': metadata.get('date', '未知日期'),
            'duration': metadata.get('duration', '未知时长'),
            'participants': metadata.get('participants', '未知参与者'),
            'summary': metadata.get('summary', '无摘要信息。'),
            'audio_url': f'/mp3/{filename}', # Serve audio from the new /mp3/ route
            'transcription': transcription,
            'ai_summary': ai_summary
        })
    
    return jsonify({'error': 'Recording not found'}), 404
