import openai
from django.conf import settings

def get_ai_finance_insight(entries):
    prompt = (
        "Analyze the following financial entries and give a short tip or insight for better budgeting:\n"
        f"{entries}\n"
        "Insight:"
    )
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial advisor providing concise budgeting insights."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()