"""
用户管理相关的提示词模板
"""
from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


# 系统提示词
USER_ASSISTANT_SYSTEM_PROMPT = """你是一个用户管理助手，可以帮助用户执行以下操作：

1. 搜索用户（按用户名或邮箱）
2. 获取用户数量统计
3. 回答关于用户的问题

请使用提供的工具来完成任务。如果无法完成，请诚实地告诉用户。"""

# 聊天提示词模板
user_assistant_chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(USER_ASSISTANT_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template("{input}"),
])

# 用户分析提示词
USER_ANALYSIS_PROMPT = """请分析以下用户数据并提供洞察：

用户信息：
{user_data}

请提供：
1. 用户的基本信息总结
2. 可能的风险点（如果有）
3. 建议的后续操作"""

user_analysis_prompt = PromptTemplate(
    input_variables=["user_data"],
    template=USER_ANALYSIS_PROMPT
)

# 用户报告生成提示词
USER_REPORT_PROMPT = """根据以下用户列表生成一份简洁的报告：

{users_list}

报告应包括：
- 总用户数
- 活跃用户比例
- 主要发现"""

user_report_prompt = PromptTemplate(
    input_variables=["users_list"],
    template=USER_REPORT_PROMPT
)
