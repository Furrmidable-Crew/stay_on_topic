import argparse
import os
import requests
import time
from bs4 import BeautifulSoup


def crawl(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href.startswith("https") and not href.startswith("#") and not len(href) == 1:
            urls.append(os.path.join(url, href))

    return urls


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CLI tool to scrape an url and upload the content in the Cat's memory")

    parser.add_argument("--url", type=str,
                        help="URL to scrape")
    parser.add_argument("--host", type=str, default="localhost",
                        help="base URL for WebSocket connection")
    parser.add_argument("--api_key", type=str, default="",
                        help="API key for WebSocket authentication")
    parser.add_argument("--size", type=int, default=1000,
                        help="Chunk size")
    parser.add_argument("--overlap", type=int, default=500,
                        help="Chunk overlap")

    args = parser.parse_args()
    print(args)

    # wipe out memory
    res = requests.delete(
        f"http://{args.host}:1865/memory/collections/declarative",
        headers={
            "access_token": args.api_key
        }
    )
    assert int(res.status_code) == 200
    print("Declarative collection deleted")

    urls = crawl(args.url)

    for u in urls:
        print(f"uploading {u}")
        post_response = requests.post(f"http://{args.host}:1865/rabbithole/web/",
                                      json={
                                          "url": u,
                                          "chunk_size": args.size,
                                          "chunk_overlap": args.overlap
                                      },
                                      headers={
                                          "accept": "application/json",
                                          "Content-Type": "application/json",
                                          "access_token": args.api_key
                                      })
        time.sleep(5)

# python upload_documentation_to_cat_discord_memory.py --host 51.68.190.246 --url https://cheshire-cat-ai.github.io/docs --api_key disbigcock-bot