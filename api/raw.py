import requests
from bs4 import BeautifulSoup
import bs4
import html
import config

with open("header.html", "r") as f:
    HEADER = f.read()

def generate_html(body: str, data: dict) -> str:
    assets_url = "/assets" if config.custom_domain is True else f"/{config.gh_repo}/assets"
    return f"""
    <html>
        <head>
            <link rel="stylesheet" href="{assets_url}/style.css">
            <script src="{assets_url}/script.js"></script>
        </head>
        {HEADER}
        <body>
            {body}
        </body>
        <script>
            const data = {data}
        </script>
    </html>
    """


def _render(word: str, data: dict) -> str:
    url = f"https://www.spanishdict.com/translate/{word}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    finds: list[bs4.Tag] = soup.find_all("div", {"class": "_0PgdvwpU WmZAoL5E"})
    for find in finds:
        textTag = find.find("a")
        if isinstance(textTag, bs4.Tag) and textTag.attrs["href"].endswith("en"):
            ans_url = textTag.attrs["href"]
            text: str = textTag.contents[0]  # type: ignore
            x = word.replace("`", "\\`")
            txt = f'<span class="spanish-word" onclick="showSpanishWord(`{x}`)">{word}</span>'
            data[word] = {
                "def_url": f"https://spanishdict.com{ans_url}",
                "text": text,
                "url": url,
            }
            return txt
    return word


def render_all(txt: str) -> str:
    data = {}
    done: list[str] = []
    for word in txt.split():
        for char in (",", ".", "?", "!", ":", ";", "\"", "'"):
            word = word.removeprefix(char).removesuffix(char)

        if word not in done:
            txt = txt.replace(word, _render(word, data))
            done.append(word)

    txt = "<br>\n".join(txt.splitlines())
    return generate_html(txt, data)


def render_syntax(txt: str) -> str:
    temp = ""
    inside = False
    data = {}
    escaped = False
    done = []

    for line in txt.splitlines():
        for char in line:
            if escaped is True:
                escaped = False
                if char != "\\":
                    continue
            elif char == "\\":
                escaped = True
            if inside is True:
                if char == "}":
                    inside = False
                    if temp not in done:
                        txt = txt.replace(f"{{{temp}}}", _render(temp, data))
                        done.append(temp)
                    temp = ""
                else:
                    temp += char
            elif char == "{":
                inside = True

    txt = "<br>\n".join(txt.splitlines())
    return generate_html(txt, data)

def render(txt: str) -> str:
    txt = html.escape(txt)

    split = txt.splitlines()

    if split[0] == "!CUSTOM-CHOSEN":
        split.pop(0)
        return render_syntax("\n".join(split))
    else:
        if len(txt.split()) > 30:
            raise ValueError("Custom Chosen is required for texts that have more than 30 words")
        return render_all(txt)

if __name__ == '__main__':
    with open("before", "r", encoding="utf-8") as f:
        txt = f.read()

    after = render(txt)

    with open("after.html", "w") as f:
        f.write(after)
