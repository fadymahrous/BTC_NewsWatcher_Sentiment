import re
import html
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
from typing import List,Dict

class GetLatestHeadlinesForexlive:
    URL = 'https://www.forexlive.com/'
    SOURCE = 'forexlive'
    HEADERS = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def clean_html(self, raw_html)->str:
        """Remove HTML tags and decode entities."""
        raw_html=raw_html.encode("latin1").decode("utf-8")
        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text(separator=" ")
        return html.unescape(text)

    def get_recent_articles(self, within_last_minutes:int)->List[Dict]:
        """Fetch and parse articles published within the given timeframe."""
        try:
            response = self.session.get(self.URL)
            html_content = response.text
        except Exception as e:
            raise RuntimeError(f"Couldnt fetch the Webpage for more details check:{e}") from e

        # Uncomment if you want to save the raw HTML for inspection
        # with open('ooo.html', 'w', encoding='utf-8') as f:
        #     f.write(html_content)

        soup = BeautifulSoup(html_content, "html.parser")
        result = {}

        # Extract mapping {identifier: title}
        divs = soup.find_all("div", class_="article-slot__content")
        for div in divs:
            h3 = div.find("h3")
            if not h3:
                continue
            a_tag = h3.find("a")
            if not a_tag:
                continue
            title_text = a_tag.get_text(strip=True)

            span = div.find("span", attrs={"data-disqus-identifier": True})
            if not span:
                continue
            identifier = span["data-disqus-identifier"]
            result[identifier] = title_text

        # Regex patterns
        pattern_all_articles = re.compile(r"articles\s*:\s*\[(.*)\],")
        pattern_article_details = re.compile(
            r"articleId:(.*?),title.*?expandedContent\:(.*?),slug.*?publishedOn:(.*?)\."
        )

        match = pattern_all_articles.search(html_content)
        if not match:
            return None

        # Extract article JSON blobs
        headers_raw = (
            match.group(1)
            .encode("utf-8")
            .decode("unicode_escape")
            .replace("},{", "}@{")
            .split("@")
        )

        articles_list = []

        for header in headers_raw:
            punket = {}
            element = pattern_article_details.search(header)
            if element:
                article_id = element.group(1).replace('"', '')
                punket["title"] = result.get(article_id, "Unknown Title")
                punket["details"] = self.clean_html(element.group(2)).replace('"', '')
                published_on_dt = datetime.fromisoformat(element.group(3).replace('"', '')).replace(tzinfo=timezone.utc)
                punket["published_on"] = published_on_dt
                punket["source"] = self.SOURCE

                # Compute age in minutes
                delta_minutes = (
                    (datetime.now(timezone.utc) - published_on_dt).total_seconds() / 60
                )
                if delta_minutes < within_last_minutes:
                    articles_list.append(punket)

        return articles_list
