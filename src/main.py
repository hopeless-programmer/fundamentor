import asyncio
import os

import openai
from config.common_configs import options
from src.ShareholderAnalyser import ShareholderAnalyser
from src.FinancialAnalyser import FinancialAnalyser
from src.NewsAnalyser import NewsAnalyser

async def gather_stock_data(script: str, serp_api_key:str):
    """
    Concurrently fetch:
      - Investor allocations
      - Financial trends
      - Recent news articles
    """
    sh_analyser = ShareholderAnalyser()
    fin_analyser = FinancialAnalyser()
    news_analyser = NewsAnalyser(serpapi_key=serp_api_key)

    investor_task = sh_analyser.get_investor_data(script)
    finance_task = fin_analyser.get_financial_trend(script)
    news_task  = news_analyser.get_news_articles_for_llm(
        script,
        months_back= 2,
        month_step= 1,
        start_offset=0
        )

    investor_data, financial_trend, news_articles = await asyncio.gather(
        investor_task, finance_task, news_task
    )
    return investor_data, financial_trend, news_articles

async def main(*,serp_api_key: str, openai_api_key:str):
    # 1) Read user input
    script = input("Enter stock symbol (e.g. TATAMOTORS): ").strip().upper()

    # 2) Fetch all data
    investor_data, financial_trend, news_articles = await gather_stock_data(script = script, serp_api_key = serp_api_key)

    # 3) Load system prompt
    with open(options["system_prompt_file"], "r") as f:
        system_prompt = f.read()

    # 4) Build user message
    user_message = f"""
    Shareholder Data:
    {investor_data}

    Financial Trends:
    {financial_trend}

    News Articles:
    {news_articles}
    """
    # print("user message: ", user_message)
    # print()
    # 5) Call GPT-4o Mini
    openai.api_key = openai_api_key
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.1,
    )

    # 6) Print prediction
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main(
        serp_api_key= "Your serp api key",
        openai_api_key= "Your open api key"
    ))