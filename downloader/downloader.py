import logging
from typing import Optional

from aiohttp import ClientSession

from downloader.config import DATA_DIR


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': '*/*'
}

STATUS_CODE_OK = 200


async def download_presentation_svg_files(url: str) -> None:
    page = 1

    async with ClientSession(headers=HEADERS) as session:
        while True:
            data = await _get_file_data(session, url.format(page))
            if not data:
                break
            _save_file(page, data)

            logging.info('page %s was downloaded' % page)
            page += 1


async def _get_file_data(session: ClientSession, url: str) -> Optional[str]:
    async with session.get(url) as response:
        if not response.ok:
            return None
        return await response.text()


def _save_file(file_name: str, file_data: str) -> None:
    with open(DATA_DIR / f'{file_name}.svg', 'w') as f:
        f.write(file_data)
