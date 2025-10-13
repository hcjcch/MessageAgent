# Mem0 多轮对话 Agent - 快速入门指南

## 🚀 5分钟快速开始

### 第一步：激活虚拟环境

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

你应该看到命令提示符前面出现 `(venv)` 标记。

### 第二步：配置 API 密钥

创建 `.env` 文件（从模板复制）：

```bash
# 查看模板
cat env_template.txt

# 创建 .env 文件
touch .env
```

编辑 `.env` 文件，添加你的 API 密钥：

```bash
# 使用你喜欢的编辑器打开
nano .env
# 或
vim .env
# 或
code .env
```

填入以下内容：

```env
MEM0_API_KEY=your_mem0_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

#### 如何获取 API 密钥？

1. **Mem0 API Key**: 
   - 访问 https://app.mem0.ai/
   - 注册/登录账号
   - 在控制台中创建 API 密钥

2. **OpenAI API Key**:
   - 访问 https://platform.openai.com/
   - 注册/登录账号
   - 在 API Keys 页面创建新密钥

### 第三步：运行你的第一个对话

```bash
python agent.py
```

#### 试试这些对话：

1. **介绍自己**：
   ```
   >>> 你好！我叫李明，我是一名产品经理，喜欢跑步和看电影。
   ```

2. **添加更多信息**：
   ```
   >>> 我最喜欢的电影类型是科幻片，特别是《星际穿越》和《银翼杀手2049》。
   ```

3. **测试记忆**：
   ```
   >>> 你能根据我的喜好推荐一些活动吗？
   ```

4. **查看记忆**：
   ```
   >>> /memories
   ```

5. **退出**：
   ```
   >>> /exit
   ```

### 第四步：测试记忆持久化

再次运行程序，使用相同的用户 ID：

```bash
python agent.py
```

输入相同的用户 ID（例如 "李明"），然后问：

```
>>> 你还记得我喜欢什么吗？
```

Agent 会从 Mem0 中回忆起之前的对话！

## 🎯 运行示例代码

查看更多使用场景：

```bash
python example.py
```

这将运行多个示例：
- 基本对话流程
- 记忆回忆
- 个性化推荐
- 记忆搜索
- 多用户隔离

## 📝 在你的代码中使用

```python
from agent import ConversationalAgent

# 创建 Agent
agent = ConversationalAgent(user_id="your_user_id")

# 对话
response = agent.chat("你好！")
print(response)

# 查看记忆
memories = agent.get_all_memories()
```

## ⚡ 常见问题

### Q: 如果没有 API 密钥怎么办？

A: Mem0 和 OpenAI 都提供免费试用额度。注册后即可获得 API 密钥。

### Q: 可以使用其他 LLM 吗？

A: 可以！修改 `agent.py` 中的 OpenAI 客户端部分，替换成其他兼容的 API（如 Claude、Gemini 等）。

### Q: 记忆会永久保存吗？

A: 是的，Mem0 会持久化存储所有记忆。你可以随时检索和使用。

### Q: 如何删除记忆？

A: 你可以通过 Mem0 的控制台或 API 来管理和删除记忆。

### Q: 成本大概多少？

A: 
- Mem0: 提供免费额度，超出后按使用量计费
- OpenAI: 根据所选模型和 token 使用量计费

## 🎓 下一步

1. **自定义系统提示**: 修改 `agent.py` 中的 `system_prompt` 来定制 Agent 行为
2. **集成到应用**: 将 Agent 集成到你的 Web 应用、聊天机器人等
3. **添加功能**: 扩展 Agent 功能，如工具调用、文件处理等
4. **优化记忆**: 调整记忆搜索和存储策略

## 📚 更多资源

- [Mem0 官方文档](https://docs.mem0.ai/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [项目 README](README.md)

---

开始享受 AI 带来的记忆能力吧！🧠✨

