import asyncio
import logging

from downloader.config import RESULT_FILE
from downloader.downloader import download_presentation_svg_files
from downloader.transformer import convert_svg_files_to_pdf, merge_pdf_files
from downloader.util import clear_data_dir, create_data_dir


URL = 'https://bbb.comsys.kpi.ua/bigbluebutton/presentation/858f01fb83d17b6bc4c11bbb02c2bd93721c20cc-1663662515773/858f01fb83d17b6bc4c11bbb02c2bd93721c20cc-1663662515773/637ccadd19817b0ece912d96bd008be1e5cbde0b-1663662515776/svg/{}'

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(module)s:%(message)s',
    level=logging.INFO
)


async def main() -> None:
    create_data_dir()

    logging.info('Downloading files...')
    await download_presentation_svg_files(URL)

    logging.info('Converting downloaded files to pdf...')
    convert_svg_files_to_pdf()

    logging.info('Merging pdfs to one file...')
    merge_pdf_files()

    logging.info(
        'Pdfs were successfully merged into result file: %s' % RESULT_FILE
    )

    clear_data_dir()


if __name__ == '__main__':
    asyncio.run(main())
