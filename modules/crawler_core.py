import urllib.request
import urllib.parse
from html.parser import HTMLParser
from collections import deque
import time
from .progress import ProgressTracker


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.links.add(attr[1])


class CrawlerCore:
    def __init__(self, start_url, aggressive=False):
        self.start_url = start_url
        self.aggressive = aggressive
        parsed_start = urllib.parse.urlparse(start_url)
        self.base_domain = parsed_start.netloc
        self.base_url = f"{parsed_start.scheme}://{self.base_domain}"
        self.visited = set()
        self.to_visit = deque([start_url])
        self.found_urls = set([start_url])
        self.progress = ProgressTracker()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; PythonSitemapGenerator/1.0)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }

    def load_common_words(self):
        try:
            with open("words.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("\nWarning: words.txt not found. Using default word list.")
            return ["admin", "login", "dashboard"]

    def test_url(self, url):
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.getcode() < 400
        except:
            return False

    def crawl(self):
        print(f"\nStarting crawl of domain: {self.base_domain}")

        if self.aggressive:
            print("Aggressive mode: Testing common paths and directories...\n")
            # Test common paths first
            common_words = self.load_common_words()
            extensions = [
                "",
                ".html",
                ".php",
                ".asp",
                ".aspx",
                ".jsp",
                ".xml",
                ".json",
                ".txt",
            ]

            total_combinations = (
                len(common_words) * len(extensions) * 3
            )  # 3 for normal, underscore, and dot prefix
            current_index = 0

            for word in common_words:
                for ext in extensions:
                    for prefix in ["", "_", "."]:
                        path = f"/{prefix}{word}{ext}"
                        potential_url = self.base_url + path

                        current_index += 1
                        self.progress.update_word_progress(
                            f"{prefix}{word}{ext}", current_index, total_combinations
                        )

                        if self.test_url(potential_url):
                            if potential_url not in self.found_urls:
                                self.found_urls.add(potential_url)
                                self.to_visit.append(potential_url)

            self.progress.clear_line()
            print("\nStarting deep crawl of discovered pages...")
        else:
            print("Standard mode: Crawling linked pages only...\n")

        while self.to_visit:
            current_url = self.to_visit.popleft()
            if current_url in self.visited:
                continue

            try:
                req = urllib.request.Request(current_url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    content_type = response.getheader("Content-Type", "").lower()

                    if (
                        "text/html" in content_type
                        or "application/json" in content_type
                    ):
                        html = response.read().decode("utf-8")
                        self.visited.add(current_url)

                        parser = LinkParser()
                        parser.feed(html)

                        for link in parser.links:
                            normalized_url = urllib.parse.urljoin(
                                current_url, link.split("#")[0]
                            )
                            parsed = urllib.parse.urlparse(normalized_url)

                            if (
                                parsed.netloc == self.base_domain
                                and parsed.scheme in ["http", "https"]
                                and normalized_url not in self.found_urls
                            ):
                                self.found_urls.add(normalized_url)
                                self.to_visit.append(normalized_url)

                        self.progress.update_crawl_progress(
                            len(self.visited), len(self.to_visit), len(self.found_urls)
                        )

            except KeyboardInterrupt:
                raise
            except Exception:
                continue

        self.progress.clear_line()
        return sorted(self.found_urls)
