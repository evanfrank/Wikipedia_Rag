import mwxml
import wikitextparser as wtp
from sqlalchemy import (insert,
                        engine)


def parse_dump(dump_file):
    dump = mwxml.Dump.from_file(open(dump_file))
    with engine.connect() as conn:
        for index, page in enumerate(dump.pages):
            parse_page(page, conn)
            if index == 1000:
                break


def parse_page(page, conn):
    if (page.redirect is None) & (page.namespace == 0):
        for index, revision in enumerate(page):
            parsed = wtp.parse(revision.text)
            for section in range(len(parsed.sections)):
                section_level = parsed.sections[section].level
                sec_title = parsed.sections[section].title
                section_text = parsed.sections[section].plain_text()

                stmt = insert("section_data").values(level=section_level,
                                                     sec_title=sec_title,
                                                     text=section_text,
                                                     page_id=page.id)

                conn.execute(stmt)
                conn.commit()

            page_id = page.id
            page_title = page.title
            stmt = insert("PAGE_data").values(page_id=page_id,
                                              page_title=page_title)
            conn.execute(stmt)
            conn.commit()
            if index == 1:
                break
