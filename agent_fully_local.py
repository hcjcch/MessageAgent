"""
完全本地化的多轮对话 Agent
- 不需要 Mem0 API Key
- 不需要 OpenAI API Key
- 使用 Ollama 本地 LLM
- 所有数据完全本地存储
"""

import os
from typing import List, Dict
from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class FullyLocalAgent:
    """完全本地化的对话 Agent"""
    
    def __init__(self, user_id: str = "default_user", model: str = "llama2"):
        """
        初始化完全本地化的 Agent
        
        Args:
            user_id: 用户唯一标识符
            model: Ollama 模型名称（llama2, mistral, llama3 等）
        """
        self.user_id = user_id
        self.model = model
        
        # 配置本地 Mem0 - 使用文件存储
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "mem0_fully_local",
                    "path": "./qdrant_storage_local",
                }
            }
        }
        
        # 初始化本地 Memory
        self.memory = Memory.from_config(config)
        print("✓ 本地向量存储已初始化")
        
        # 初始化 Ollama 客户端（使用 OpenAI 兼容接口）
        try:
            self.llm_client = OpenAI(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama"  # Ollama 不需要真实 API key
            )
            
            # 测试连接
            self.llm_client.models.list()
            print(f"✓ Ollama 已连接，使用模型: {self.model}")
            
        except Exception as e:
            raise ValueError(
                f"无法连接到 Ollama: {e}\n"
                "请确保 Ollama 已安装并运行。\n"
                "安装: https://ollama.com/download\n"
                f"运行: ollama run {self.model}"
            )
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
        
        print(f"✓ 完全本地化 Agent 已初始化 (用户ID: {self.user_id})")
        print("✓ 无需任何外部 API Key")
        print("✓ 所有数据和计算都在本地")
    
    def add_to_memory(self, messages: List[Dict[str, str]]):
        """将对话消息添加到本地记忆中"""
        try:
            for msg in messages:
                content = msg.get("content", "")
                if content:
                    self.memory.add(
                        content, 
                        user_id=self.user_id,
                        metadata={"role": msg.get("role", "user")}
                    )
            print(f"✓ 已保存 {len(messages)} 条记忆到本地")
        except Exception as e:
            print(f"✗ 保存记忆失败: {e}")
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """从本地记忆中搜索相关内容"""
        try:
            results = self.memory.search(
                query, 
                user_id=self.user_id,
                limit=limit
            )
            return results if results else []
        except Exception as e:
            print(f"✗ 搜索记忆失败: {e}")
            return []
    
    def get_all_memories(self) -> List[Dict]:
        """获取用户的所有本地记忆"""
        try:
            memories = self.memory.get_all(user_id=self.user_id)
            return memories if memories else []
        except Exception as e:
            print(f"✗ 获取记忆失败: {e}")
            return []
    
    def build_context_from_memory(self, user_message: str) -> str:
        """基于用户消息从本地记忆中构建上下文"""
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
        """进行对话"""
        print(f"\n👤 用户: {user_message}")
        
        # 从本地记忆中获取相关上下文
        memory_context = self.build_context_from_memory(user_message)
        
        # 构建系统提示
        system_prompt = """你是一个友好且乐于助人的 AI 助手。
你可以记住之前对话中的信息，并在回答时利用这些信息提供更个性化的服务。
如果你从历史信息中了解到用户的偏好或背景，请在回答时自然地体现出来。
请用中文回答。"""
        
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
        
        # 调用本地 Ollama
        try:
            print("⏳ 正在生成回复（本地模型可能较慢）...")
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            
            assistant_message = response.choices[0].message.content
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # 将对话添加到本地记忆中
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
        """显示所有本地记忆"""
        print("\n" + "="*60)
        print("📚 当前用户的所有本地记忆:")
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
        """清空当前会话的对话历史"""
        self.conversation_history = []
        print("✓ 已清空当前会话历史")


def main():
    """主程序入口"""
    print("=" * 60)
    print("完全本地化的多轮对话 Agent")
    print("=" * 60)
    print("✓ 无需 Mem0 API Key")
    print("✓ 无需 OpenAI API Key")
    print("✓ 使用本地 Ollama 模型")
    print("✓ 所有数据和计算都在本地")
    print("=" * 60)
    
    # 获取用户ID
    user_id = input("\n请输入用户ID (直接回车使用 'default_user'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    # 选择模型
    print("\n可用模型（需要先下载）:")
    print("  1. llama2 (推荐)")
    print("  2. llama3")
    print("  3. mistral")
    print("  4. qwen")
    model_choice = input("\n选择模型 (直接回车使用 llama2): ").strip()
    
    model_map = {
        "1": "llama2",
        "2": "llama3",
        "3": "mistral",
        "4": "qwen",
        "": "llama2"
    }
    model = model_map.get(model_choice, model_choice if model_choice else "llama2")
    
    # 创建 Agent
    try:
        agent = FullyLocalAgent(user_id=user_id, model=model)
    except ValueError as e:
        print(f"\n错误: {e}")
        return
    except Exception as e:
        print(f"\n初始化错误: {e}")
        print("\n💡 提示：")
        print("1. 确保已安装 Ollama: https://ollama.com/download")
        print(f"2. 下载模型: ollama pull {model}")
        print("3. 启动模型: ollama run {model}")
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

