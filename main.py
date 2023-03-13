import asyncio
import re
from urllib.parse import unquote

import aiohttp
import requests
from aiohttp import ClientConnectorError
from lxml import etree


class ParsingPath:
    """Path parsing from link to link"""

    def __init__(self):
        self.domain = 'wikipedia.org'
        self.all_domain = 'https://ru.wikipedia.org'
        self.file = 'source_links'
        self.data_links = {}
        self.offers = []
        self.lst_links = []

    def reading_input_data(self):
        """Reading input data from file"""
        with open(self.file, 'r', encoding='utf-8') as f:
            links = f.read().split('\n')
        pattern = '(\w+:\/\/)(\w{2}|www).(' + self.domain + ')'
        result = [i for i in links if re.match(pattern, i)]
        return result if len(result) == 2 else None

    def get_result(self):
        """Get result"""
        res_links = []
        input_data = self.reading_input_data()
        while input_data[0] not in res_links:
            for i in self.lst_links:
                if (input_data[1] in i) and (i[0] not in res_links):
                    res_links.append(i[0])
                    break
                try:
                    if (res_links[-1] in i) and (i[0] not in res_links):
                        res_links.append(i[0])
                except IndexError:
                    continue
        res_links.insert(0, input_data[1])

        urls = []
        for link in res_links:
            if link == input_data[0]:
                urls.insert(0, link)
                break
            urls.insert(0, link)
        return self.get_offers(urls)

    def get_offers(self, urls):
        """Get offers"""
        i = 0
        while True:
            response = requests.get(urls[i]).text
            offers_lst = response.split('.')
            tree = etree.HTML(response)
            try:
                link_split = urls[i + 1].split(self.all_domain)[-1]
            except IndexError:
                break
            links = tree.xpath('//*[@id="mw-content-text"]/*[@class="mw-parser-output"]/p/a/@href')
            for link in links:
                parent = link.getparent()
                link_url = parent.xpath('.//@href')
                link_text = parent.xpath('.//text()')
                if link_url[0] == link_split:
                    for offer in offers_lst:
                        if link_url[0] in offer and link_text[0] in offer:
                            res_offer = ''.join(etree.HTML(offer).xpath('//text()')).split('\n')[-1]
                            print(f'{i + 1}--------\n{res_offer}\n{unquote(urls[i + 1], "utf-8")}\n')
                            break
                    break
            i += 1

    async def get_tasks(self, urls):
        """Get tasks"""
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.get_links(url))
            tasks.append(task)
        return tasks

    async def get_links(self, url):
        """Get links"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, ssl=True) as response:
                    html = await response.text()
                    tree = etree.HTML(html)
                    if getattr(tree, 'xpath', None):
                        offers_html = tree.xpath('//*[@id="mw-content-text"]/*[@class="mw-parser-output"]/p/text()')
                        links_text = tree.xpath('//*[@id="mw-content-text"]/*[@class="mw-parser-output"]/p/a/text()')
                        links_xpath = tree.xpath('//*[@id="mw-content-text"]/*[@class="mw-parser-output"]/p/a/@href')
                        links = [f'{self.all_domain}{i}' for i in links_xpath]
                        data_links = dict(zip(links, links_text))
                        self.data_links.update(**data_links)
                        offers = ''.join(map(lambda x, y: f'{x} {y}', offers_html, links_text)).split('.')
                        self.offers += offers
                        self.lst_links += [[url, i] for i in links]
                        if self.reading_input_data()[1] in links:
                            tasks = asyncio.all_tasks()
                            for task in tasks:
                                task.get_loop().stop()
                        elif self.reading_input_data()[1] not in links:
                            tasks = await self.get_tasks(links)
                            return await asyncio.gather(*tasks)
            except ClientConnectorError:
                return []

    async def main(self, url=None):
        """Running"""
        if url is None:
            url = self.reading_input_data()[0]
        pages = await self.get_links(url)
        tasks = []
        if pages:
            for page in pages:
                task = asyncio.create_task(self.get_links(f'{self.all_domain}{page}'))
                tasks.append(task)
            await asyncio.gather(*tasks)


if __name__ == '__main__':
    parsing = ParsingPath()
    data = parsing.reading_input_data()
    if data:
        try:
            asyncio.run(parsing.main())
        except RuntimeError:
            parsing.get_result()
