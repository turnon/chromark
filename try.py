import re

folder_start_pattern = r"<DT><H3"
folder_end_pattern = r"</DL>"
entry_pattern = r"<DT><A"

folder_name_pattern = r'<H3.*>(.*?)</H3>'
href_pattern = r'HREF="(.*?)"'
date_pattern = r'ADD_DATE="(.*?)"'
title_pattern = r"<A.*>(.*?)</A>"


def regexp_extract(regexp, string):
    match = re.search(regexp, string)
    return match.group(1) if match else None


def iterator(bookmark_path):
    with open(bookmark_path) as f:
        stack = []
        for line in f:
            if re.search(entry_pattern, line):
                url = regexp_extract(href_pattern, line)
                date = regexp_extract(date_pattern, line)
                title = regexp_extract(title_pattern, line)
                yield(url, date, title, stack)
            elif re.search(folder_start_pattern, line):
                folder_name = regexp_extract(folder_name_pattern, line)
                stack.append(folder_name)
            elif re.search(folder_end_pattern, line) and len(stack) > 0:
                stack.pop()
            else:
                pass

for entry in iterator("bookmarks_2024_3_5.html"):
    print(entry)