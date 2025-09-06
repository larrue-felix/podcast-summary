import requests
from bs4 import BeautifulSoup


def get_soup(episode_path: str) -> BeautifulSoup:
    """
    Get the BeautifulSoup object for a given episode page.

    Args:
        episode_path: The path of the episode page, e.g., "/episodes/123".
    """
    url = f"https://postgres.fm{episode_path}/transcript"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_title_and_transcript(soup: BeautifulSoup) -> str:
    """
    Extract the title and transcript text from the episode page soup.

    Args:
        soup: BeautifulSoup object of the episode page.

    Returns:
        A tuple containing the title and transcript text.
    """
    transcript_div = soup.find("div", class_="site-episode-transcript")
    transcript = (
        transcript_div.get_text(strip=True) if transcript_div else "No Transcript Found"
    )

    return transcript


def scrape_episode_details(episode_path: str) -> str:
    """
    Scrape the title and transcript of a single episode given its path.

    Args:
        episode_path: The path of the episode page, e.g., "/episodes/123".

    Returns:
        A dictionary containing the title and transcript.
    """
    soup = get_soup(episode_path)
    return get_title_and_transcript(soup)
