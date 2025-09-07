import os

from openai import OpenAI

from utils import read_from_file, write_to_file

client = OpenAI()


def list_files_from_directory(directory_path: str) -> list[str]:
    return [
        os.path.join(directory_path, file_name)
        for file_name in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, file_name))
    ]


def get_file_name_from_path(file_path: str) -> str:
    return os.path.basename(file_path)


def load_transcript_from_file(file_path: str) -> str:
    return read_from_file(file_path)


def summarize_transcript(transcript: str) -> str:
    print("Asking GPT-5 Nano for summary...")
    response = client.responses.create(
        model="gpt-5-nano",
        instructions="You are a summarization engine. Always output only the summary in valid Markdown. Do not add introductions or follow-ups.",
        input="Summarize the following podcast transcript:\n\n" + transcript,
    )
    print("✅")
    return response.output_text


def summarize_all_transcripts(transcript_directory: str, output_directory):
    transcript_file_paths = list_files_from_directory(transcript_directory)

    for idx, transcript_file_path in enumerate(transcript_file_paths):
        print(
            f"Processing file {idx + 1}/{len(transcript_file_paths)}: {transcript_file_path}"
        )
        filename = get_file_name_from_path(transcript_file_path).replace(
            ".txt", "_summary.md"
        )
        transcript = load_transcript_from_file(transcript_file_path)
        summary = summarize_transcript(transcript)
        write_to_file(
            file_path=os.path.join(output_directory, filename),
            content=summary,
        )


summarize_all_transcripts(
    transcript_directory="data/postgresfm/transcripts",
    output_directory="data/postgresfm/summaries",
)
