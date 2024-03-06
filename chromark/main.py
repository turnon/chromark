import re
from urllib.parse import urlparse
from datetime import datetime


def regexp_extract_first(regexp):
    def m(string):
        match = re.search(regexp, string)
        return match.group(1) if match else None

    return m


class Entry:
    xlink = r'^\s*<DT><A HREF="(.*)" ADD_DATE="([0-9]+)".*>(.*)</A>.*$'

    def __init__(self, folders, line):
        self.folders = [fo for fo in folders]
        m = re.match(self.__class__.xlink, line)
        if m:
            self.url = m.group(1)
            self.datetime = datetime.fromtimestamp(float(m.group(2))).strftime("%F %T")
            self.title = m.group(3)

    @property
    def netloc(self):
        return urlparse(self.url).netloc if self.url is not None else None

    def __repr__(self):
        folder_str = "/".join(self.folders)
        return f"{folder_str}/{self.title}"


def read(bookmark_path):
    folder_start_pattern = r"<DT><H3"
    folder_end_pattern = r"</DL>"
    entry_pattern = r"<DT><A"
    extract_folder = regexp_extract_first(r"<H3.*>(.*?)</H3>")

    with open(bookmark_path) as f:
        stack = []
        for line in f:
            if re.search(entry_pattern, line):
                yield Entry(stack, line)
            elif re.search(folder_start_pattern, line):
                folder_name = extract_folder(line)
                stack.append(folder_name)
            elif re.search(folder_end_pattern, line) and len(stack) > 0:
                stack.pop()
            else:
                pass
