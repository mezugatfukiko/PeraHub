import openai
from django.conf import settings

def get_ai_finance_insight(entries):
    prompt = (
        "Analyze the following financial entries and give a short tip or insight for better budgeting:\n"
        f"{entries}\n"
        "Insight:"
    )
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        temperature=0.7,
    )
    return response.choices[0].text.strip()