import urllib.parse
import re


def normalize_url(url, base_url):
    url = url.split("#")[0]
    if not url:
        return None

    try:
        if url.startswith("/"):
            return urllib.parse.urljoin(base_url, url)
        elif not url.startswith(("http://", "https://")):
            return urllib.parse.urljoin(base_url, url)
        return url
    except:
        return None


def is_valid_url(url, base_domain):
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc == base_domain and parsed.scheme in ["http", "https"]
    except:
        return False


def validate_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_output_filename(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    filename = re.sub(r"[^\w\-_.]", "_", domain)
    return f"{filename}.txt"
