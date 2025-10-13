"""
基于 Mem0 的多轮对话 Agent
支持上下文记忆和个性化对话
"""

import os
from typing import List, Dict
from mem0 import MemoryClient
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ConversationalAgent:
    """支持记忆功能的多轮对话 Agent"""
    
    def __init__(self, user_id: str = "default_user"):
        """
        初始化对话 Agent
        
        Args:
            user_id: 用户唯一标识符，用于区分不同用户的记忆
        """
        self.user_id = user_id
        
        # 初始化 Mem0 客户端
        mem0_api_key = os.getenv("MEM0_API_KEY")
        if not mem0_api_key:
            raise ValueError("请设置 MEM0_API_KEY 环境变量")
        
        self.memory_client = MemoryClient(api_key=mem0_api_key)
        
        # 初始化 OpenAI 客户端
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
        
        print(f"✓ Agent 已初始化 (用户ID: {self.user_id})")
    
    def add_to_memory(self, messages: List[Dict[str, str]]):
        """
        将对话消息添加到 Mem0 记忆中
        
        Args:
            messages: 对话消息列表
        """
        try:
            result = self.memory_client.add(messages, user_id=self.user_id)
            print(f"✓ 已保存 {len(messages)} 条记忆")
            return result
        except Exception as e:
            print(f"✗ 保存记忆失败: {e}")
            return None
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """
        从记忆中搜索相关内容
        
        Args:
            query: 搜索查询
            limit: 返回结果数量限制
            
        Returns:
            相关记忆列表
        """
        try:
            filters = {
                "AND": [
                    {"user_id": self.user_id}
                ]
            }
            results = self.memory_client.search(
                query, 
                version="v2", 
                filters=filters,
                limit=limit
            )
            return results.get("results", []) if results else []
        except Exception as e:
            print(f"✗ 搜索记忆失败: {e}")
            return []
    
    def get_all_memories(self) -> List[Dict]:
        """
        获取用户的所有记忆
        
        Returns:
            所有记忆列表
        """
        try:
            memories = self.memory_client.get_all(user_id=self.user_id)
            return memories.get("results", []) if memories else []
        except Exception as e:
            print(f"✗ 获取记忆失败: {e}")
            return []
    
    def build_context_from_memory(self, user_message: str) -> str:
        """
        基于用户消息从记忆中构建上下文
        
        Args:
            user_message: 用户消息
            
        Returns:
            上下文字符串
        """
        relevant_memories = self.search_memory(user_message, limit=3)
        
        if not relevant_memories:
            return ""
        
        context_parts = ["相关历史信息:"]
        for i, memory in enumerate(relevant_memories, 1):
            memory_text = memory.get("memory", "")
            if memory_text:
                context_parts.append(f"{i}. {memory_text}")
        
        return "\n".join(context_parts)
    
    def chat(self, user_message: str) -> str:
        """
        进行对话
        
        Args:
            user_message: 用户输入的消息
            
        Returns:
            助手的回复
        """
        print(f"\n👤 用户: {user_message}")
        
        # 从记忆中获取相关上下文
        memory_context = self.build_context_from_memory(user_message)
        
        # 构建系统提示
        system_prompt = """你是一个友好且乐于助人的 AI 助手。
你可以记住之前对话中的信息，并在回答时利用这些信息提供更个性化的服务。
如果你从历史信息中了解到用户的偏好或背景，请在回答时自然地体现出来。"""
        
        # 构建消息列表
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # 如果有相关记忆，添加到消息中
        if memory_context:
            messages.append({
                "role": "system", 
                "content": f"\n{memory_context}"
            })
        
        # 添加对话历史（最近5轮）
        messages.extend(self.conversation_history[-10:])
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        # 调用 OpenAI API
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # 将对话添加到 Mem0 记忆中
            self.add_to_memory([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message}
            ])
            
            print(f"🤖 助手: {assistant_message}")
            return assistant_message
            
        except Exception as e:
            error_msg = f"生成回复时出错: {e}"
            print(f"✗ {error_msg}")
            return error_msg
    
    def show_memories(self):
        """显示所有记忆"""
        print("\n" + "="*60)
        print("📚 当前用户的所有记忆:")
        print("="*60)
        
        memories = self.get_all_memories()
        
        if not memories:
            print("暂无记忆")
        else:
            for i, memory in enumerate(memories, 1):
                memory_text = memory.get("memory", "")
                created_at = memory.get("created_at", "")
                print(f"\n{i}. {memory_text}")
                if created_at:
                    print(f"   时间: {created_at}")
        
        print("\n" + "="*60)
    
    def clear_conversation_history(self):
        """清空当前会话的对话历史（不清除 Mem0 中的记忆）"""
        self.conversation_history = []
        print("✓ 已清空当前会话历史")


def main():
    """主程序入口"""
    print("=" * 60)
    print("欢迎使用基于 Mem0 的多轮对话 Agent")
    print("=" * 60)
    
    # 获取用户ID
    user_id = input("\n请输入用户ID (直接回车使用 'default_user'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    # 创建 Agent
    try:
        agent = ConversationalAgent(user_id=user_id)
    except ValueError as e:
        print(f"\n错误: {e}")
        print("\n请按照以下步骤配置环境变量:")
        print("1. 复制 .env.example 文件为 .env")
        print("2. 在 .env 文件中填入你的 API 密钥")
        print("   - MEM0_API_KEY: 从 https://app.mem0.ai/ 获取")
        print("   - OPENAI_API_KEY: 从 https://platform.openai.com/ 获取")
        return
    
    print("\n可用命令:")
    print("  - 直接输入消息进行对话")
    print("  - /memories - 查看所有记忆")
    print("  - /clear - 清空当前会话历史")
    print("  - /quit 或 /exit - 退出程序")
    print()
    
    # 对话循环
    while True:
        try:
            user_input = input("\n>>> ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ['/quit', '/exit']:
                print("\n再见！👋")
                break
            elif user_input.lower() == '/memories':
                agent.show_memories()
            elif user_input.lower() == '/clear':
                agent.clear_conversation_history()
            else:
                # 正常对话
                agent.chat(user_input)
                
        except KeyboardInterrupt:
            print("\n\n程序已中断。再见！👋")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()

