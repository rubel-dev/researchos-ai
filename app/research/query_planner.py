import time

from openai import InternalServerError, OpenAI

from app.core.config import settings
from app.schemas.research import QueryPlan

client = OpenAI(
    api_key=settings.gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    max_retries=0
)

def generate_search_queries(question: str) -> QueryPlan:
    max_retries = 3
    for attempt in range(max_retries):
        try: 
            response = client.chat.completions.parse(
                model = settings.gemini_model,
                messages=[
                        {
                            "role": "system",
                            "content": """
                You are a research query planner.

                Given a research question, generate exactly 3 focused web search queries.

                Each query should:
                - cover a different important aspect of the question
                - be concise and search-engine friendly
                - avoid unnecessary duplication
                - include a short purpose explaining why this query is needed

                Do not answer the research question.
                Only create the research search plan.
                """,
                        },
                        {
                            "role": "user",
                            "content": question,
                        },
                    ],

                    response_format=QueryPlan,
                )

            return response.choices[0].message.parsed
        except InternalServerError:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(F"Gemini unavailable. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    