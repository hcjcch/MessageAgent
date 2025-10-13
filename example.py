"""
Agent 使用示例
演示如何在代码中集成 Mem0 多轮对话 Agent
"""

from agent import ConversationalAgent
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def example_basic_conversation():
    """示例1: 基本对话"""
    print("\n" + "="*60)
    print("示例 1: 基本对话流程")
    print("="*60)
    
    # 创建 Agent
    agent = ConversationalAgent(user_id="demo_user_1")
    
    # 进行对话
    agent.chat("你好！我叫张三，我是一名软件工程师。")
    agent.chat("我特别喜欢使用 Python 和 Go 语言开发。")
    agent.chat("我最近在学习 AI 和机器学习。")
    
    # 查看记忆
    agent.show_memories()


def example_memory_recall():
    """示例2: 记忆回忆"""
    print("\n" + "="*60)
    print("示例 2: 记忆回忆")
    print("="*60)
    
    # 使用相同的 user_id 创建新的 Agent 实例
    # 这模拟了用户在新会话中返回的场景
    agent = ConversationalAgent(user_id="demo_user_1")
    
    # Agent 会从记忆中回忆起之前的对话
    agent.chat("你还记得我是做什么工作的吗？")
    agent.chat("我擅长哪些编程语言？")


def example_personalized_service():
    """示例3: 个性化服务"""
    print("\n" + "="*60)
    print("示例 3: 个性化推荐")
    print("="*60)
    
    # 新用户
    agent = ConversationalAgent(user_id="demo_user_2")
    
    # 建立用户偏好
    agent.chat("我喜欢喝咖啡，尤其是美式咖啡。")
    agent.chat("我平时喜欢阅读科幻小说和技术书籍。")
    
    # 基于记忆的个性化推荐
    agent.chat("你能推荐一些适合我的活动吗？")


def example_search_memories():
    """示例4: 搜索特定记忆"""
    print("\n" + "="*60)
    print("示例 4: 搜索记忆")
    print("="*60)
    
    agent = ConversationalAgent(user_id="demo_user_1")
    
    # 搜索与编程相关的记忆
    print("\n🔍 搜索关键词: '编程语言'")
    memories = agent.search_memory("编程语言", limit=3)
    
    for i, memory in enumerate(memories, 1):
        memory_text = memory.get("memory", "")
        score = memory.get("score", 0)
        print(f"{i}. {memory_text} (相关度: {score:.2f})")


def example_multiple_users():
    """示例5: 多用户隔离"""
    print("\n" + "="*60)
    print("示例 5: 多用户记忆隔离")
    print("="*60)
    
    # 用户 A
    print("\n--- 用户 A ---")
    agent_a = ConversationalAgent(user_id="user_a")
    agent_a.chat("我喜欢吃披萨。")
    
    # 用户 B
    print("\n--- 用户 B ---")
    agent_b = ConversationalAgent(user_id="user_b")
    agent_b.chat("我喜欢吃寿司。")
    
    # 验证记忆隔离
    print("\n--- 验证: 用户 A 的记忆 ---")
    agent_a.chat("我喜欢吃什么？")
    
    print("\n--- 验证: 用户 B 的记忆 ---")
    agent_b.chat("我喜欢吃什么？")


def main():
    """运行所有示例"""
    print("="*60)
    print("Mem0 多轮对话 Agent - 示例演示")
    print("="*60)
    
    try:
        # 运行各个示例
        example_basic_conversation()
        
        input("\n按回车继续下一个示例...")
        example_memory_recall()
        
        input("\n按回车继续下一个示例...")
        example_personalized_service()
        
        input("\n按回车继续下一个示例...")
        example_search_memories()
        
        input("\n按回车继续下一个示例...")
        example_multiple_users()
        
        print("\n" + "="*60)
        print("所有示例运行完成！")
        print("="*60)
        
    except ValueError as e:
        print(f"\n错误: {e}")
        print("\n请确保已正确配置环境变量:")
        print("1. 创建 .env 文件")
        print("2. 设置 MEM0_API_KEY 和 OPENAI_API_KEY")
        print("3. 参考 env_template.txt 文件")
    except Exception as e:
        print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()

