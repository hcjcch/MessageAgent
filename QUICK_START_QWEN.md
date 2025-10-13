# 快速开始 - 通义千问 + ChromaDB 版本

## 🚀 三步快速启动

### 第一步：设置环境变量

你已经把 API Key 放到系统环境变量里了，确认一下：

```bash
# 检查环境变量是否存在
echo $DEFAULT_LLM_API_KEY
```

如果显示空白，需要设置：

#### macOS/Linux：

```bash
# 临时设置（仅当前终端有效）
export DEFAULT_LLM_API_KEY=sk-your-qwen-api-key-here

# 永久设置（推荐）
# 编辑 ~/.zshrc 或 ~/.bashrc
echo 'export DEFAULT_LLM_API_KEY=sk-your-qwen-api-key-here' >> ~/.zshrc
source ~/.zshrc
```

#### 可选：设置模型

```bash
# 默认使用 qwen-plus，也可以指定其他模型
export QWEN_MODEL=qwen-plus
# 或 qwen-turbo (更快更便宜)
# 或 qwen-max (更强大)
```

### 第二步：运行测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行配置测试
python test_qwen_setup.py
```

### 第三步：开始对话

```bash
python agent_local.py
```

## 📋 完整示例

```bash
# 1. 激活虚拟环境
cd /Users/huangchen/Develop/mem0
source venv/bin/activate

# 2. 确认环境变量（如果还没设置）
export DEFAULT_LLM_API_KEY=sk-xxxxx

# 3. 运行测试
python test_qwen_setup.py

# 4. 看到 "✅ 所有测试通过！" 后，开始使用
python agent_local.py
```

## 💬 使用示例

```
============================================================
欢迎使用基于 Mem0 的多轮对话 Agent（本地版本）
✓ 使用通义千问 LLM
✓ 使用 ChromaDB 本地存储
✓ 无需 Mem0 云服务 API Key
============================================================

请输入用户ID (直接回车使用 'default_user'): 张三

✓ 使用 ChromaDB 向量数据库（本地文件存储）
✓ 数据存储路径: ./chroma_storage
✓ 使用通义千问模型: qwen-plus
✓ 本地 Agent 已初始化 (用户ID: 张三)
✓ 使用通义千问 + ChromaDB 本地存储

可用命令:
  - 直接输入消息进行对话
  - /memories - 查看所有记忆
  - /clear - 清空当前会话历史
  - /quit 或 /exit - 退出程序

>>> 你好，我是一名 Python 开发者，喜欢做 AI 相关的项目

👤 用户: 你好，我是一名 Python 开发者，喜欢做 AI 相关的项目
✓ 已保存 2 条记忆到本地
🤖 助手: 你好！很高兴认识你这位 Python 开发者。AI 项目确实是目前最热门和最有前景的方向之一...

>>> 你记得我是做什么的吗？

👤 用户: 你记得我是做什么的吗？
🤖 助手: 当然记得！你是一名 Python 开发者，而且特别喜欢做 AI 相关的项目...
```

## 🎯 环境变量说明

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `DEFAULT_LLM_API_KEY` | ✅ 是 | 无 | 通义千问 API Key |
| `QWEN_MODEL` | ❌ 否 | `qwen-plus` | 使用的模型 |

## 🔧 故障排除

### 问题 1：环境变量未生效

**症状**：运行时提示 "请设置 DEFAULT_LLM_API_KEY 环境变量"

**解决**：
```bash
# 检查环境变量
echo $DEFAULT_LLM_API_KEY

# 如果为空，重新设置
export DEFAULT_LLM_API_KEY=your_key_here

# 或者在当前目录创建 .env 文件
echo "DEFAULT_LLM_API_KEY=your_key_here" > .env
```

### 问题 2：ChromaDB 初始化失败

**症状**：提示 "ChromaDB 初始化失败"

**解决**：
```bash
# 确认已安装 ChromaDB
pip list | grep chromadb

# 如果没有，安装
pip install chromadb
```

### 问题 3：通义千问连接失败

**症状**：提示 API 调用失败

**解决**：
1. 检查 API Key 是否正确
2. 确认已在 https://dashscope.aliyun.com/ 开通服务
3. 检查账户余额是否充足
4. 确认网络连接正常

### 问题 4：.env 文件不生效

**症状**：设置了 .env 但还是提示未配置

**解决**：
```bash
# 确认 .env 文件在项目根目录
ls -la .env

# 确认文件内容
cat .env

# 应该看到：
# DEFAULT_LLM_API_KEY=sk-xxxxx
```

## 📊 模型选择建议

| 场景 | 推荐模型 | 特点 |
|------|----------|------|
| 日常聊天 | `qwen-turbo` | 速度快、成本低 |
| 通用对话 | `qwen-plus` | 平衡性能和成本 ⭐ 推荐 |
| 复杂任务 | `qwen-max` | 能力强、准确度高 |
| 长文本 | `qwen-long` | 支持超长上下文 |

切换模型：
```bash
export QWEN_MODEL=qwen-turbo  # 或其他模型
```

## 📁 数据存储位置

```
./chroma_storage/          # ChromaDB 数据目录
├── chroma.sqlite3         # 数据库文件
└── ...                   # 其他索引文件
```

**备份记忆数据**：
```bash
# 备份
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_storage

# 恢复
tar -xzf chroma_backup_20241013.tar.gz
```

## 🎉 开始使用

现在你可以：

1. **运行测试**：`python test_qwen_setup.py`
2. **启动 Agent**：`python agent_local.py`
3. **开始对话**：享受带记忆的智能对话！

---

**祝使用愉快！有问题随时查看文档或运行测试脚本。** 🚀

