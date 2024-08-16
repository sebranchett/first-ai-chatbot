import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,
)
from langchain import hub

EMAILS_CHROMA_PATH = "chroma_data/"

dotenv.load_dotenv()

email_template_str = """Your job is to use Erik's
emails to answer questions about his life and work.
Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know.

{context}
"""

email_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=email_template_str,
    )
)

email_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)
messages = [email_system_prompt, email_human_prompt]

email_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"],
    messages=messages,
)

chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

output_parser = StrOutputParser()

emails_vector_db = Chroma(
    persist_directory=EMAILS_CHROMA_PATH,
    embedding_function=OpenAIEmbeddings()
)

emails_retriever = emails_vector_db.as_retriever(k=10)

email_chain = (
    {"context": emails_retriever, "question": RunnablePassthrough()}
    | email_prompt_template
    | chat_model
    | output_parser
)

tools = [
    Tool(
        name="Emails",
        func=email_chain.invoke,
        description="""Useful when you need to answer questions
        about Erik based on his emails.
        Pass the entire question as input to the tool. For instance,
        if the question is "Who is Erik?",
        the input should be "Who is Erik?"
        """,
    ),
]

email_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

agent_chat_model = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    temperature=0,
)

email_agent = create_openai_functions_agent(
    llm=agent_chat_model,
    prompt=email_agent_prompt,
    tools=tools,
)

email_agent_executor = AgentExecutor(
    agent=email_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
