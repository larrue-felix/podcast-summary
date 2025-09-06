import requests
from bs4 import BeautifulSoup


def get_soup(page_number: int) -> BeautifulSoup:
    url = f"https://postgres.fm/episodes?page={page_number}&per=50"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def retrieve_episode_list_from_page(soup: BeautifulSoup) -> list[str]:
    episodes = soup.find_all("div", class_="site-episode")
    print(f"Found {len(episodes)} episodes on the page.")

    episode_paths: list[str] = []
    for ep in episodes:
        a_tag = ep.find("h2").find("a")
        href = a_tag["href"]

        episode_paths.append(href)

        print(f"Full href: {href}")
        print("---")

    return episode_paths


def has_next_page(soup: BeautifulSoup) -> bool:
    next_button = soup.find("a", class_="page-item next-page site-button")
    return next_button is not None


def scrape_one_page(page_number: int) -> list[str]:
    print(f"Scraping page {page_number}...")
    soup = get_soup(page_number)
    episode_paths = retrieve_episode_list_from_page(soup)
    return episode_paths


def scrape_all_pages() -> list[str]:
    all_episode_paths: list[str] = []
    page_number = 1

    while True:
        episode_paths = scrape_one_page(page_number)
        all_episode_paths.extend(episode_paths)

        soup = get_soup(page_number)
        if not has_next_page(soup):
            break

        page_number += 1

    return all_episode_paths
