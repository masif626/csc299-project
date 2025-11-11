import os
from openai import OpenAI
def get_summary(long_description: str) -> str:
    print(f"Summarizing: '{long_description[:40]}...'")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "ERROR: OPENAI_API_KEY not set."
    client = OpenAI(api_key = api_key)
    try:
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "system",
                    "content": "Your job is to summerize a long task "
                               "description into a short 3-5 word phrase. "
                               "Reply with *only* the summary phrase."
                },
                {
                    "role": "user",
                    "content": long_description
                }
            ]
        )
        summary = completion.choices[0].message.content
        return summary
    except Exception as e:
        return f"ERROR: {e}"
def main():
    paragraphs = [
        "I need to go to the grocery store and pick up several things. I am out of nuggets,"
        "mangos, and edamame. I also need some spices and maybe "
        "some bars of chocolate if they are on sale.",
        
        "This is my project for my course CSC 299. I need to make sure I have "
        "written at least two pytest tests, and the main app runs the 'uv ran' command."
    ]
    print("-----AI Task Summarizer-----")
    for p in paragraphs:
        summary = get_summary(p)
        print(f"     -> Summary: {summary}\n")
    print("--------------------")    