import sys
from modules.url_utils import (
    normalize_url,
    validate_url,
    is_valid_url,
    get_output_filename,
)
from modules.crawler_core import CrawlerCore
from modules.progress import ProgressTracker


def get_yes_no_input(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please answer 'yes' or 'no' (or 'y' or 'n')")


def main():
    print(
        """
╔═══════════════════════════════════════╗
║        Website Crawler Tool           ║
║     (Site Mapping & Discovery)        ║
╚═══════════════════════════════════════╝
    """
    )

    while True:
        start_url = input(
            "Enter the website URL to crawl (e.g., https://example.com): "
        ).strip()

        if not start_url:
            print("URL cannot be empty. Please try again.")
            continue

        if not start_url.startswith(("http://", "https://")):
            start_url = "https://" + start_url

        if not validate_url(start_url):
            print("Invalid URL format. Please enter a valid URL.")
            continue

        break

    aggressive = get_yes_no_input(
        "\nEnable aggressive crawling? This will test for common hidden paths (yes/no): "
    )

    print("\nInitializing crawler..." + (" (Aggressive Mode)" if aggressive else ""))
    crawler = CrawlerCore(start_url, aggressive=aggressive)

    try:
        urls = crawler.crawl()

        # Generate output filename based on the site URL
        output_file = get_output_filename(start_url)

        # Save results
        with open(output_file, "w") as f:
            for url in urls:
                f.write(f"{url}\n")

        print(f"\n\nCrawl complete!")
        print(f"Found {len(urls)} unique URLs")
        print(f"Results saved to: {output_file}")
        if aggressive:
            print(
                "\nNote: Aggressive crawling was used. Some discovered URLs might be sensitive."
            )

    except KeyboardInterrupt:
        print("\n\nCrawling stopped by user. Saving current results...")
        output_file = get_output_filename(start_url)
        with open(output_file, "w") as f:
            for url in crawler.found_urls:
                f.write(f"{url}\n")
        print(f"Partial results saved to: {output_file}")
        sys.exit(0)


if __name__ == "__main__":
    main()
