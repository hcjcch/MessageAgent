"""
基于 Manus 上下文工程经验的改进版 Mem0 Agent
实现文章中的关键设计原则
"""

import os
import json
import random
from typing import List, Dict
from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ImprovedMem0Agent:
    """基于 Manus 上下文工程经验的改进版 Agent"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        
        # 获取 API Key
        llm_api_key = os.getenv("DEFAULT_LLM_API_KEY")
        if not llm_api_key:
            raise ValueError("请设置 DEFAULT_LLM_API_KEY 环境变量")
        
        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = llm_api_key
        os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        # 配置 Mem0
        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "mem0_improved",
                    "path": "./chroma_storage_improved",
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": os.getenv("QWEN_MODEL", "qwen-plus"),
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-v1",
                }
            }
        }
        
        self.memory = Memory.from_config(config)
        self.llm_client = OpenAI(
            api_key=llm_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = os.getenv("QWEN_MODEL", "qwen-plus")
        
        # 对话历史和目标跟踪
        self.conversation_history: List[Dict[str, str]] = []
        self.current_goals: List[str] = []
        self.completed_goals: List[str] = []
        
        print(f"✓ 改进版 Agent 已初始化 (用户ID: {self.user_id})")
    
    def add_controlled_randomness(self, text: str) -> str:
        """
        引入受控随机性，避免模式固化
        基于文章中的"不要被少样本示例所困"原则
        """
        variations = [
            lambda x: x,
            lambda x: x.replace("相关历史信息:", "历史上下文:"),
            lambda x: x.replace("相关历史信息:", "相关记忆:"),
            lambda x: x.replace("相关历史信息:", "背景信息:"),
        ]
        
        return random.choice(variations)(text)
    
    def build_goal_summary(self) -> str:
        """
        构建目标摘要，实现"通过复述操控注意力"
        类似 Manus 的 todo.md 机制
        """
        if not self.current_goals and not self.completed_goals:
            return ""
        
        goal_parts = ["## 当前任务状态"]
        
        if self.current_goals:
            goal_parts.append("### 进行中的目标:")
            for i, goal in enumerate(self.current_goals, 1):
                goal_parts.append(f"- [ ] {goal}")
        
        if self.completed_goals:
            goal_parts.append("### 已完成的目标:")
            for i, goal in enumerate(self.completed_goals, 1):
                goal_parts.append(f"- [x] {goal}")
        
        return "\n".join(goal_parts)
    
    def compress_context(self, messages: List[Dict[str, str]], max_tokens: int = 4000) -> List[Dict[str, str]]:
        """
        上下文压缩，实现"基于文件的记忆"原则
        当上下文过长时，将旧信息压缩到记忆中
        """
        # 简单的 token 估算（实际应用中应使用 tiktoken）
        total_length = sum(len(str(msg).split()) for msg in messages)
        
        if total_length <= max_tokens:
            return messages
        
        print(f"🔄 上下文过长 ({total_length} tokens)，开始压缩...")
        
        # 保留系统提示和最近的消息
        compressed_messages = [messages[0]]  # 系统提示
        
        # 将中间的历史消息压缩到记忆中
        middle_messages = messages[1:-2]  # 排除系统提示和最后两条消息
        if middle_messages:
            # 提取关键信息并保存到记忆
            for msg in middle_messages:
                if msg.get("role") == "user":
                    self.memory.add(
                        f"用户说: {msg.get('content', '')}",
                        user_id=self.user_id,
                        metadata={"type": "compressed_context", "role": "user"}
                    )
                elif msg.get("role") == "assistant":
                    self.memory.add(
                        f"助手回复: {msg.get('content', '')}",
                        user_id=self.user_id,
                        metadata={"type": "compressed_context", "role": "assistant"}
                    )
        
        # 添加压缩标记和最近消息
        compressed_messages.append({
            "role": "system",
            "content": "[注意：部分历史对话已压缩到记忆中，可通过搜索获取]"
        })
        compressed_messages.extend(messages[-2:])  # 保留最后两条消息
        
        print(f"✅ 上下文已压缩，从 {len(messages)} 条消息减少到 {len(compressed_messages)} 条")
        return compressed_messages
    
    def build_context_from_memory(self, user_message: str) -> str:
        """改进的记忆构建，引入随机性"""
        relevant_memories = self.memory.search(
            user_message, 
            user_id=self.user_id,
            limit=3
        )
        
        if isinstance(relevant_memories, dict) and 'results' in relevant_memories:
            relevant_memories = relevant_memories['results']
        
        if not relevant_memories:
            return ""
        
        # 引入随机性
        context_templates = [
            "相关历史信息:",
            "历史上下文:",
            "相关记忆:",
            "背景信息:"
        ]
        
        context_parts = [random.choice(context_templates)]
        
        for i, memory in enumerate(relevant_memories, 1):
            memory_text = memory.get("memory", "")
            if memory_text:
                # 随机化格式
                formats = [
                    f"{i}. {memory_text}",
                    f"• {memory_text}",
                    f"- {memory_text}",
                    f"📝 {memory_text}"
                ]
                context_parts.append(random.choice(formats))
        
        return self.add_controlled_randomness("\n".join(context_parts))
    
    def extract_goals_from_message(self, user_message: str) -> List[str]:
        """从用户消息中提取目标"""
        # 简单的目标提取逻辑
        goal_indicators = ["需要", "想要", "希望", "计划", "目标", "任务"]
        goals = []
        
        for indicator in goal_indicators:
            if indicator in user_message:
                # 提取包含指示词的句子
                sentences = user_message.split('。')
                for sentence in sentences:
                    if indicator in sentence:
                        goals.append(sentence.strip())
        
        return goals
    
    def chat(self, user_message: str) -> str:
        """改进的对话方法"""
        print(f"\n👤 用户: {user_message}")
        
        # 提取并更新目标
        new_goals = self.extract_goals_from_message(user_message)
        self.current_goals.extend(new_goals)
        
        # 构建上下文
        memory_context = self.build_context_from_memory(user_message)
        goal_summary = self.build_goal_summary()
        
        # 构建系统提示（保持稳定以支持 KV 缓存）
        system_prompt = """你是一个友好且乐于助人的 AI 助手。
你可以记住之前对话中的信息，并在回答时利用这些信息提供更个性化的服务。
如果你从历史信息中了解到用户的偏好或背景，请在回答时自然地体现出来。
请根据当前任务状态调整你的回复。"""
        
        # 构建消息列表
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加目标摘要
        if goal_summary:
            messages.append({
                "role": "system",
                "content": f"\n{goal_summary}"
            })
        
        # 添加记忆上下文
        if memory_context:
            messages.append({
                "role": "system",
                "content": f"\n{memory_context}"
            })
        
        # 添加对话历史
        messages.extend(self.conversation_history[-10:])
        messages.append({"role": "user", "content": user_message})
        
        # 上下文压缩
        messages = self.compress_context(messages)
        
        # 调用 API
        try:
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # 保存到记忆
            self.memory.add(
                f"用户: {user_message}\n助手: {assistant_message}",
                user_id=self.user_id,
                metadata={"type": "conversation"}
            )
            
            # 检查是否有目标完成
            self._check_goal_completion(assistant_message)
            
            print(f"🤖 助手: {assistant_message}")
            return assistant_message
            
        except Exception as e:
            error_msg = f"生成回复时出错: {e}"
            print(f"✗ {error_msg}")
            return error_msg
    
    def _check_goal_completion(self, assistant_message: str):
        """检查目标是否完成"""
        completion_indicators = ["完成", "结束", "搞定", "好了", "已解决"]
        
        for indicator in completion_indicators:
            if indicator in assistant_message:
                # 标记第一个目标为完成
                if self.current_goals:
                    completed_goal = self.current_goals.pop(0)
                    self.completed_goals.append(completed_goal)
                    print(f"✅ 目标完成: {completed_goal}")
                break
    
    def show_status(self):
        """显示当前状态"""
        print("\n" + "="*60)
        print("📊 当前状态")
        print("="*60)
        
        print(f"📝 进行中的目标: {len(self.current_goals)}")
        for i, goal in enumerate(self.current_goals, 1):
            print(f"  {i}. {goal}")
        
        print(f"\n✅ 已完成的目标: {len(self.completed_goals)}")
        for i, goal in enumerate(self.completed_goals, 1):
            print(f"  {i}. {goal}")
        
        print(f"\n💬 对话历史: {len(self.conversation_history)} 条")
        print("="*60)


def main():
    """主程序"""
    print("=" * 60)
    print("🚀 改进版 Mem0 Agent（基于 Manus 经验）")
    print("✓ 目标跟踪和复述")
    print("✓ 上下文压缩")
    print("✓ 受控随机性")
    print("✓ 错误保留")
    print("=" * 60)
    
    user_id = input("\n请输入用户ID (直接回车使用 'default_user'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    try:
        agent = ImprovedMem0Agent(user_id=user_id)
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    print("\n可用命令:")
    print("  - 直接输入消息进行对话")
    print("  - /status - 查看当前状态")
    print("  - /quit 或 /exit - 退出程序")
    print()
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/quit', '/exit']:
                print("\n再见！👋")
                break
            elif user_input.lower() == '/status':
                agent.show_status()
            else:
                agent.chat(user_input)
                
        except KeyboardInterrupt:
            print("\n\n程序已中断。再见！👋")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()
