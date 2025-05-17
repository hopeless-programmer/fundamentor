import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

import aiohttp
from newspaper import Article

from src.utils.datetime_utils import parse_date


class NewsAnalyser:
    def __init__(
        self,
        serpapi_key: str,
        max_concurrent_requests: int = 5,
        max_workers: int = 5,
    ):
        self.serpapi_key = serpapi_key
        # throttle concurrent HTTP requests to SerpApi
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)
        # thread pool for blocking Article parsing
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    async def __search_interval(
        self,
        session: aiohttp.ClientSession,
        stock: str,
        start_date: datetime,
        end_date: datetime,
        num_results: int,
    ) -> list[tuple[str, str]]:
        """
        Async call to SerpApi news search.
        """
        params = {
            "engine": "google",
            "q": f"{stock} company news -earnings -report -%",
            "tbm": "nws",
            "api_key": self.serpapi_key,
            "num": num_results,
            "tbs": (
                f"cdr:1,"
                f"cd_min:{start_date.strftime('%m/%d/%Y')},"
                f"cd_max:{end_date.strftime('%m/%d/%Y')}"
            ),
        }
        async with self._semaphore:
            async with session.get("https://serpapi.com/search.json", params=params) as resp:
                data = await resp.json()
        results = data.get("news_results", [])[:num_results]
        return [(item.get("link"), item.get("date")) for item in results]

    async def __extract_article(self, url: str) -> tuple[str | None, str | None]:
        """
        Offload blocking newspaper.Article to a thread.
        """
        def fetch():
            art = Article(url)
            art.download()
            art.parse()
            return art.title, art.text

        try:
            return await asyncio.get_event_loop().run_in_executor(self._executor, fetch)
        except Exception:
            return None, None

    async def __process_interval(
        self,
        session: aiohttp.ClientSession,
        stock: str,
        m: int,
        num_results: int,
    ) -> tuple[str, str, str] | None:
        """
        For one monthly window, fetch up to `num_results` URLs
        and return the first successfully parsed (date, title, snippet).
        """
        end = datetime.today() - timedelta(days=30 * m)
        start = datetime.today() - timedelta(days=30 * (m + 1))

        candidates = await self.__search_interval(session, stock, start, end, num_results)

        for url, date_str in candidates:
            if not url or not date_str:
                continue
            title, text = await self.__extract_article(url)
            if title and text:
                snippet = text.replace("\n", " ").strip()[:1500]
                return date_str, title, snippet

        # no success in this window
        print(f"[WARN] no article for {m=} months ago ({start.date()}–{end.date()})")
        return None

    async def get_news_articles_for_llm(
        self,
        stock: str,
        months_back: int = 12,
        month_step: int = 1,
        start_offset: int = 0,
        num_results: int = 3,
    ) -> str:
        """
        Concurrently process each interval window, then sort & format.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.__process_interval(session, stock, m, num_results)
                for m in range(start_offset, months_back + 1, month_step)
            ]
            raw_samples = await asyncio.gather(*tasks)

        # filter out failed windows, sort by date
        samples = sorted(
            (s for s in raw_samples if s),
            key=lambda x: parse_date(x[0])
        )

        # bullet-format
        return "\n\n".join(
            f"• [{date}] {title}\n  {text}..."
            for date, title, text in samples
        )


# ───── Example usage ─────
if __name__ == "__main__":

    async def main():
        analyser = NewsAnalyser(
            serpapi_key="98d5c1b6686213dec23b000ef7e5166f9e57c54edb9897e4f65cca98024a5cfa",
            max_concurrent_requests=5,
            max_workers=5,
        )
        prompt = await analyser.get_news_articles_for_llm(
            "Tata Motors",
            months_back=5,
            month_step=2,
            start_offset=0,
            num_results=3,
        )
        print(prompt)

    asyncio.run(main())
