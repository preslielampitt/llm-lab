import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def compact(messages):
    '''
    Summarize a chat history in 1-5 lines so it can replace a longer conversation.

    >>> result = compact([{'role': 'user', 'content': 'My name is Bob'}])
    >>> isinstance(result, str)
    True
    '''
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = 'openai/gpt-oss-120b'

    prompt = {
        "role": "system",
        "content": (
            "Summarize this conversation in 1-5 lines. "
            "Keep important facts, prior tool results, and user goals. "
            "Do not include unnecessary detail."
        )
    }

    response = client.chat.completions.create(
        model=model,
        messages=[prompt] + messages,
        temperature=0.0,
        seed=0,
    )

    return response.choices[0].message.content


compact_tool_schema = {
    "type": "function",
    "function": {
        "name": "compact",
        "description": "Summarize the current chat session in 1-5 lines and replace the chat history with the summary.",
        "parameters": {
            "type": "object",
            "properties": {
                "messages": {
                    "type": "array",
                    "description": "The current chat message history to summarize."
                }
            },
            "required": ["messages"],
        },
    },
}
