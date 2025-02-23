from agents.dialogue_creator.dialogue_creator_agent import dialogue_creator_agent
from agents.dialogue_creator.tts_utils import DialogueToSpeech
from markitdown import MarkItDown
from pathlib import Path
from pydantic_ai.models.groq import GroqModelSettings


async def main():
    # Create data/pdfs directory if it doesn't exist
    pdf_dir = Path('data/pdfs')
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = pdf_dir / 'attention-is-all-you-need.pdf'
    
    # Check if file exists, if not download it
    if not file_path.exists():
        import requests
        url = "https://arxiv.org/pdf/1706.03762.pdf"
        response = requests.get(url)
        file_path.write_bytes(response.content)
        print(f"Downloaded paper to {file_path}")

    md = MarkItDown()
    file_cmd = md.convert(file_path)

    # Example message to classify
    user_message = f"The content of the file is: {file_cmd.text_content}"
    
    # Call the dialogue creator agent
    result = await dialogue_creator_agent.run(user_message, model_settings=GroqModelSettings(temperature=0.2))
    
    # Save the output to a markdown file
    output_path = Path('data/output.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to markdown format and write to file
    markdown_content = f"# Dialogue\n\n```json\n{result.data.model_dump_json(indent=4)}\n```"
    print(markdown_content)
    output_path.write_text(markdown_content)
    print(f"Saved dialogue to {output_path}")

    # Create DialogueToSpeech instance
    dialogue_to_speech = DialogueToSpeech()
    
    # Generate podcast audio, Combine podcast parts into a single file
    combined_podcast_path = dialogue_to_speech.combine_podcast_parts(result.data)
    print(f"Combined dialogue saved to: {combined_podcast_path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())