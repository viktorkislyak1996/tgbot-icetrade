import asyncio
import logging
from collections import namedtuple
from urllib.parse import quote

from aiohttp import (
    ClientSession,
    ClientTimeout,
    ServerDisconnectedError,
    ClientConnectionError
)
from bs4 import BeautifulSoup
from faker import Faker

logger = logging.getLogger(__name__)

fake = Faker()

AuctionTable = namedtuple(
    'AuctionTable',
    ['link', 'description', 'customer_name', 'country', 'number', 'cost', 'expires_at']
)


class IcetradeScraper:
    """
    The class that allows to scrape Icetrade auctions
    based on a specific search keyword

    Args:
        keyword: The keyword to scrape.

    Attributes:
        headers: The headers for request.
        url: The URL to be parsed.
    """

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Host': 'icetrade.by',
        'User-Agent': fake.user_agent(),
        'Referer': 'icetrade.by',
        'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,la;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'text/html; charset=utf-8'
    }
    ICETRADE_AUCTION_URL = (
        'https://icetrade.by/search/auctions?search_text={}'
        '&sort=num%3Adesc'
        '&onPage=50'
    )

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword
        self.url = self.ICETRADE_AUCTION_URL.format(quote(self.keyword))

    async def __process_request(
            self,
            url: str,
            headers: dict,
            retries: int = 3,
            semaphore: int = 50,
            timeout: int = 30
    ) -> str:
        """
        Makes a request by URL and returns the content.

        Args:
            url: The URL to make request.
            headers: The headers for request.
            retries: The number of attempts to make a request
            semaphore: The semaphore
            timeout: Time to interrupt the request (in seconds)

        Returns:
            The page content.
        """
        timeout = ClientTimeout(total=timeout)
        semaphore = asyncio.Semaphore(semaphore)
        try:
            async with semaphore:
                async with ClientSession(timeout=timeout, raise_for_status=True) as session:
                    async with session.get(url, headers=headers, ssl=False) as response:
                        if response.status == 429:
                            logger.error(f'Too many requests - url: {url}')
                            await asyncio.sleep(5)
                            if retries > 0:
                                return await self.__process_request(url=url, headers=headers, retries=retries - 1)
                        page_content = await response.text()
                        return page_content
        except (ServerDisconnectedError, ClientConnectionError, asyncio.exceptions.TimeoutError):
            if retries > 0:
                await asyncio.sleep(5)
                return await self.__process_request(url=url, headers=headers, retries=retries - 1)
            raise
        except Exception as e:
            logger.error(f"Error while fetching data: {e}")
            raise

    async def __get_content(self) -> BeautifulSoup:
        """
        Obtain the BeautifulSoup content.

        Returns:
            The BeautifulSoup content.
        """
        page_content = await self.__process_request(self.url, self.headers)
        try:
            soup = BeautifulSoup(page_content, "lxml")
        except TypeError:
            logger.error(
                "Parser didn't find the auction data."
                "Please check the correctness of the parser"
            )
        else:
            return soup

    async def get_auction(self) -> list[AuctionTable] | None:
        """
        Receive top 5 tenders from the Icetrade auction.

        Returns:
            The list of namedtuples that contain link, description,
            customer_name, country, number, cost and expires_at info.
        """
        soup = await self.__get_content()
        if not soup:
            return

        total_result = []
        try:
            table = soup.find(id='auctions-list')
            for row in table.find_all('tr'):
                result = []
                for index, cell in enumerate(row.find_all('td')):
                    cell_text = cell.text
                    if cell_text == 'Тендеры не найдены':
                        break
                    if index == 0:
                        a_tag = cell.find('a')
                        if a_tag:
                            link = a_tag.get('href', self.url)
                        else:
                            link = self.url
                        result.append(link)
                    result.append(cell_text.strip())
                if result:
                    total_result.append(AuctionTable(*result))
        except AttributeError:
            logger.error(
                "Parser didn't find the auction data."
                "Please check the correctness of the parser"
            )
            return
        return total_result[:5]

    async def get_auction_info(self, auction_list: list[AuctionTable] = None) -> dict:
        """
        Receive Icetrade auction info.

        Args:
            auction_list: The list of namedtuples that contain link, description,
                          customer_name, country, number, cost and expires_at info.

        Returns:
            The dict that contains the number of offers,
            info about the last tender and auction link (if the auction was found)
        """
        if not auction_list:
            auction_list = await self.get_auction()
        result = {'auction_link': self.url}
        if auction_list:
            offers_number = len(auction_list)
            last_tender = max(auction_list, key=lambda x: int(x.number.split('-')[1]))
            result.update(
                {
                    'offers_number': offers_number,
                    'last_tender': last_tender
                }
            )
        return result
