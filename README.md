# Social Hub Dashboard - Flask 前后端项目

这是一个基于 Python Flask 构建的简单社交中心仪表板，集成了设备信息展示、互动日历和对话总结功能。项目采用前后端分离的架构，前端通过 AJAX 调用后端 API 获取数据并动态渲染。

## 项目结构

```
.
├── app.py                  # Flask 主应用程序入口
├── requirements.txt        # Python 依赖列表
├── data/                   # 模拟数据文件
│   ├── device_info.json    # 设备信息数据
│   ├── interactions.json   # 日历互动数据
│   └── recordings.json     # 对话总结录音数据
├── api/                    # 后端 API 蓝图
│   ├── __init__.py         # (空文件，表示这是一个 Python 包)
│   ├── calendar.py         # 日历 API 路由
│   ├── device.py           # 设备信息 API 路由
│   └── summary.py          # 对话总结 API 路由
├── static/                 # 静态文件 (CSS, JS, 图片等)
│   └── style.css           # 全局样式表
└── templates/              # HTML 模板文件
    ├── calendar.html       # 互动日历页面
    ├── index.html          # 设备信息主页
    └── summary.html        # 对话总结页面
```

## 已完成功能

1.  **项目初始化与结构搭建**：
    *   创建了清晰的 Flask 项目目录结构，将前端资源（HTML, CSS）和后端逻辑（Flask 应用、API 蓝图、数据）分离。
    *   定义了项目依赖 `Flask==2.3.3`。

2.  **多页面视图实现**：
    *   **首页 (Device Info)**：展示硬件信息（电量续航、网络连接状况、软件版本等）。
        *   数据通过前端 JavaScript 调用 `/api/device_info` 接口动态加载。
    *   **互动日历 (Interactive Calendar)**：展示当前月份的日历网格，并在有互动日期下显示标记，支持月份切换。
        *   日历数据和互动标记通过前端 JavaScript 调用 `/api/calendar_data` 接口动态加载。
    *   **对话总结 (Conversation Summary)**：展示录音文件列表，包含关键信息和简要总结。
        *   数据通过前端 JavaScript 调用 `/api/recordings` 接口动态加载。

3.  **后端 API 接口设计与实现**：
    *   所有 API 接口都通过 Flask Blueprint 进行了模块化管理，并统一前缀为 `/api`。
    *   数据不再硬编码在前端，而是通过后端接口动态提供。

4.  **前后端数据交互**：
    *   前端页面使用 JavaScript 的 `fetch` API 向后端对应的 `/api` 接口发送 GET 请求，获取 JSON 数据。
    *   获取数据后，前端 JavaScript 动态渲染页面内容。

5.  **侧边栏导航优化**：
    *   侧边栏导航只保留了“首页”、“互动日历”和“对话总结”三个核心功能，并确保了正确的链接和激活状态。

## API 文档

所有 API 接口都通过 Flask Blueprint 进行了模块化管理，并统一前缀为 `/api`。

### 1. 获取设备信息 (Device API)

*   **URL**: `/api/device_info`
*   **方法**: `GET`
*   **描述**: 获取设备硬件和软件信息。
*   **请求参数**: 无
*   **响应示例**:
    ```json
    {
        "battery_level": 85,
        "battery_status": "Charging",
        "network_status": "Connected",
        "network_type": "Wi-Fi",
        "software_version": "1.2.0",
        "last_update": "2024-07-29",
        "model_name": "Social Hub Device X",
        "serial_number": "SHD-2024-001"
    }
    ```

### 2. 获取日历数据 (Calendar API)

*   **URL**: `/api/calendar_data`
*   **方法**: `GET`
*   **描述**: 获取指定年份和月份的日历数据，包括日期、是否当前月份、是否今天以及当天的互动标记。
*   **请求参数**:
    *   `year` (可选, Integer): 年份。如果未提供，默认为当前年份。
    *   `month` (可选, Integer): 月份 (1-12)。如果未提供，默认为当前月份。
*   **响应示例**:
    ```json
    {
        "current_month_name": "July",
        "current_year": 2024,
        "calendar_days": [
            {
                "day_number": "",
                "is_current_month": false,
                "is_today": false,
                "interactions": []
            },
            {
                "day_number": 1,
                "is_current_month": true,
                "is_today": false,
                "interactions": []
            },
            {
                "day_number": 5,
                "is_current_month": true,
                "is_today": false,
                "interactions": [
                    {"class": "friend-1"},
                    {"class": "friend-2"}
                ]
            },
            // ... 更多日期数据
        ]
    }
    ```

### 3. 获取对话录音列表 (Summary API)

*   **URL**: `/api/recordings`
*   **方法**: `GET`
*   **描述**: 获取对话录音文件列表及其摘要信息。
*   **请求参数**: 无
*   **响应示例**:
    ```json
    [
        {
            "id": 1,
            "title": "Team Meeting - Project Alpha",
            "date": "2024-07-29",
            "duration": "45 min",
            "participants": "John, Jane, Mike",
            "summary": "Discussed project milestones, assigned tasks for next sprint, and reviewed Q3 goals."
        },
        // ... 更多录音
    ]
    ```

## 配置文件说明

目前，项目没有独立的配置文件。所有配置（如 Flask debug 模式、API 路径前缀等）都直接硬编码在 `app.py` 中。模拟数据则存储在 `data/` 目录下的 JSON 文件中。

*   **`requirements.txt`**:
    *   定义了项目的 Python 依赖，目前只包含 `Flask==2.3.3`。
    *   **安装依赖**: `pip install -r requirements.txt`

*   **`data/` 目录**:
    *   `device_info.json`: 存储设备信息的模拟数据。
    *   `interactions.json`: 存储日历互动标记的模拟数据。键为日期字符串（`YYYY-MM-DD`），值为互动标记数组。
    *   `recordings.json`: 存储对话录音总结的模拟数据。

*   **`app.py`**:
    *   `app = Flask(__name__)`: 初始化 Flask 应用。
    *   `app.register_blueprint(...)`: 注册各个 API 蓝图，并指定 `/api` 作为 URL 前缀。
    *   `app.run(debug=True)`: 在开发模式下运行应用，`debug=True` 会在代码更改时自动重启服务器并提供调试信息。**在生产环境中应设置为 `False`。**

## 如何运行项目

1.  **导航到项目根目录**:
    ```bash
    cd c:/Users/Administrator/Desktop/python/Hackathon
    ```
2.  **安装项目依赖**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **运行 Flask 应用程序**:
    ```bash
    python app.py
    ```
4.  **在浏览器中访问**:
    *   首页: `http://127.0.0.1:5000/`
    *   互动日历: `http://127.0.0.1:5000/calendar`
    *   对话总结: `http://127.0.0.1:5000/summary`

---

## 与 AI 协作的工作流提示词

为了保持高效且智能的协作体验，请在新的对话中将以下内容作为自定义指令提供给我：

**作为一名高级软件工程师，Cline，你拥有丰富的编程语言、框架、设计模式和最佳实践知识。在与我协作时，请遵循以下工作流和原则：**

1.  **迭代式开发**：每次只专注于一个明确的任务或优化点。在收到我的任务后，首先在 `<thinking>` 标签中分析需求，并拆解为清晰、可执行的步骤。
2.  **工具优先**：优先使用你可用的工具（如 `read_file`, `write_to_file`, `replace_in_file`, `execute_command`, `list_files` 等）来获取信息、执行操作。避免要求我提供你通过工具可以获取的信息。
3.  **明确的工具使用**：每次只使用一个工具，并等待我的响应。在调用工具前，请在 `<thinking>` 标签中说明你选择该工具的原因以及预期结果。
4.  **精确的修改**：当修改文件时，使用 `replace_in_file` 进行精确的、小范围的更改。如果 `replace_in_file` 失败，请根据错误信息调整 SEARCH 块，或在必要时使用 `write_to_file` 作为回退。
5.  **主动的架构思考与建议**：在完成当前任务或在关键决策点时，主动评估现有架构，并在 `<plan_mode_respond>` 模式下提出优化建议，解释其优点和实现方式。
6.  **清晰的技术沟通**：你的回复应直接、技术性强，避免寒暄和不必要的客套话。专注于任务本身，提供清晰的解释和操作步骤。
7.  **响应式反馈**：我会提供关于你操作结果的反馈（成功、失败、错误信息或新的需求）。请仔细阅读并根据我的反馈调整你的下一步行动。
8.  **任务完成**：当一个任务或一系列优化完成后，使用 `attempt_completion` 工具总结工作，并提供运行或验证的命令。不要在 `attempt_completion` 的结果中提出问题或寻求进一步的对话。
9.  **保持同步**：确保 `README.md` 文件始终反映项目的最新状态、功能和 API 文档。
