import asyncio
import logging
import os
from typing import Optional
from pathlib import Path

from aiohttp import ClientSession


URL = 'https://bbb.comsys.kpi.ua/bigbluebutton/presentation/858f01fb83d17b6bc4c11bbb02c2bd93721c20cc-1663662515773/858f01fb83d17b6bc4c11bbb02c2bd93721c20cc-1663662515773/637ccadd19817b0ece912d96bd008be1e5cbde0b-1663662515776/svg/{}'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': '*/*'
}

STATUS_CODE_OK = 200

FILES_DIR = Path('data')

logging.basicConfig(
    level=logging.INFO
)


async def get_file_data(session: ClientSession, url: str) -> Optional[str]:
    async with session.get(url) as response:
        if response.status == STATUS_CODE_OK:
            return await response.text()
        return None


def save_file(file_name: str, file_data: str) -> None:
    with open(FILES_DIR / f'{file_name}.html', 'w') as f:
        f.write(file_data)


def create_files_dir() -> None:
    try:
        os.mkdir(FILES_DIR.name)
    except FileExistsError:
        pass


async def main() -> None:
    create_files_dir()

    files_data = []
    page = 1

    logging.info('Start downloading pages...')

    async with ClientSession(headers=HEADERS) as session:
        while True:
            file_data = await get_file_data(session, URL.format(page))

            if not file_data:
                logging.info('End of downloading. Start saving...')
                break

            files_data.append({'page': page, 'data': file_data})

            logging.info('page %s was downloaded' % page)

            page += 1
    
    for item in files_data:
        save_file(item['page'], item['data'])

    logging.info('%s pages are saved' % page)


if __name__ == '__main__':
    asyncio.run(main())
