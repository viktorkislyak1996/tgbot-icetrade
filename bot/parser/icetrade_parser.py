import asyncio
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class IcetradeParser:
    keywords = (
        'АСКУЭ',
        'АСУ ТП',
        'АСУТП',
        'телемеханика',
        'ТЛМ',
        'трансформаторная подстанция',
        'подстанция',
        'ТП',
        'РП',
        'распределительный пункт'
    )

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Host': 'icetrade.by',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Referer': 'icetrade.by',
        'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,la;q=0.6',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'text/html; charset=utf-8'
    }
    url = ('https://icetrade.by/search/auctions?search_text=%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D0%BA%D0%B0'
           '&zakup_type%5B1%5D=1'
           '&zakup_type%5B2%5D=1'
           '&auc_num='
           '&okrb='
           '&company_title='
           '&establishment=0'
           '&industries='
           '&period='
           '&created_from='
           '&created_to='
           '&request_end_from='
           '&request_end_to='
           '&t%5BTrade%5D=1'
           '&t%5BeTrade%5D=1'
           '&t%5BsocialOrder%5D=1'
           '&t%5BsingleSource%5D=1'
           '&t%5BAuction%5D=1'
           '&t%5BRequest%5D=1'
           '&t%5BcontractingTrades%5D=1'
           '&t%5Bnegotiations%5D=1'
           '&t%5BOther%5D=1'
           '&r%5B1%5D=1'
           '&r%5B2%5D=2'
           '&r%5B7%5D=7'
           '&r%5B3%5D=3'
           '&r%5B4%5D=4'
           '&r%5B6%5D=6'
           '&r%5B5%5D=5'
           '&sort=num%3Adesc'
           '&sbm=1'
           '&onPage=20'
           )

    async def __process_request(self) -> str:
        async with ClientSession() as session:
            async with session.get(self.url, headers=self.headers, ssl=False) as response:
                response = await response.text()
                # print(response)
                return response

    async def __get_content(self) -> BeautifulSoup:
        page_content = await self.__process_request()
        try:
            self.soup = BeautifulSoup(page_content, "lxml")
        except TypeError:
            logger.error(
                "Parser didn't find the total number of ads. "
                "Please check the correctness of the parser"
            )
        else:
            return self.soup

    async def parse(self):
        await self.__get_content()
        if not self.soup:
            return None

        total_result = []
        try:
            table = self.soup.find(id='auctions-list')
            for row in table.find_all('tr'):
                result = []
                for cell in row.find_all('td'):
                    cell_text = cell.text
                    result.append(cell_text.strip())
                    # print(cell_text)
                if result:
                    total_result.append(result)
        except AttributeError:
            logger.error(
                "Parses didn't find the total number of ads. "
                "Please check the correctness of the parser"
            )
            return
        print(total_result)
        return total_result


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(parse_icetrade(url, headers))
    parser = IcetradeParser()
    asyncio.run(parser.parse())
