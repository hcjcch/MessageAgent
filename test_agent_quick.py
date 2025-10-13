"""
快速测试 agent_local.py 是否正常工作
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_agent():
    """测试 Agent 基本功能"""
    print("=" * 60)
    print("快速测试 Agent")
    print("=" * 60)
    
    # 检查环境变量
    if not os.getenv("DEFAULT_LLM_API_KEY"):
        print("✗ 缺少 DEFAULT_LLM_API_KEY 环境变量")
        return False
    
    try:
        from agent_local import LocalConversationalAgent
        
        print("\n1️⃣ 创建 Agent...")
        agent = LocalConversationalAgent(user_id="test_user")
        
        print("\n2️⃣ 测试对话...")
        response = agent.chat("你好，我叫测试用户，喜欢编程")
        
        print("\n3️⃣ 测试记忆搜索...")
        memories = agent.search_memory("编程")
        print(f"✓ 搜索到 {len(memories)} 条相关记忆")
        
        print("\n4️⃣ 测试获取所有记忆...")
        all_memories = agent.get_all_memories()
        print(f"✓ 共有 {len(all_memories)} 条记忆")
        
        print("\n5️⃣ 测试显示记忆...")
        agent.show_memories()
        
        print("\n6️⃣ 测试记忆回忆...")
        response2 = agent.chat("我喜欢什么？")
        
        # 清理测试数据
        import shutil
        if os.path.exists("./chroma_storage"):
            # 不删除，保留用户数据
            pass
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！Agent 工作正常")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)

