import mwxml
import wikitextparser as wtp
import pandas as pd


def parse_dump(dump_file, localDB):
    dump = mwxml.Dump.from_file(open(dump_file, encoding="utf8"))
    for index, page in enumerate(dump.pages):
        parse_page(page, localDB)
        if index == 1000:
            break


def parse_page(page, localDB):
    if (page.redirect is None) & (page.namespace == 0):
        for index, revision in enumerate(page):
            parsed = wtp.parse(revision.text)
            for section in range(len(parsed.sections)):
                section_level = parsed.sections[section].level
                sec_title = parsed.sections[section].title
                section_text = parsed.sections[section].plain_text()
                sections_df = pd.DataFrame({"level": [section_level],
                                            "sec_title": [sec_title],
                                            "text": [section_text],
                                            "page_id": [page.id]})
                sections_df.to_sql(name="sections",
                                   if_exists="append",
                                   con=localDB,
                                   index=False)

            page_id = page.id
            page_title = page.title
            page_df = pd.DataFrame({"page_id": [page_id],
                                    "page_title": [page_title]})
            page_df.to_sql(name="pages",
                           if_exists="append",
                           con=localDB,
                           index=False)
            if index == 1:
                break
