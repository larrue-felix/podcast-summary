import time

from utils import write_to_file

from .scrape_episode_list import scrape_all_pages
from .scrape_episode_transcript import scrape_episode_details


def run() -> list[dict[str, str]]:
    episode_paths = scrape_all_pages()
    print(f"Total episodes found: {len(episode_paths)}")

    episodes_data: list[dict[str, str]] = []

    for idx, episode_path in enumerate(episode_paths):
        print(f"Processing episode {idx + 1}/{len(episode_paths)}: {episode_path}")

        transcript = scrape_episode_details(episode_path)
        slug = episode_path.split("/")[-1]
        filename = f"data/postgresfm/{idx + 1:03d}_{slug}.txt"
        write_to_file(file_path=filename, content=transcript)
        time.sleep(5)

    return episodes_data


run()
