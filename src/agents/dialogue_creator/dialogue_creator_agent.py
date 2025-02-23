'''
This agent is used to create a dialogue from a content of a file.

The purpose to simplify the content of a file to a dialogue. By using the dialogue, the user can understand the content of the file.
Later, the dialogue will be used to create a text to speech audio file to mimic a real people explaining and discussing the content of the file. 
'''

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.groq import GroqModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field
from typing import List, Literal
from dataclasses import dataclass
from groq import Client as GroqClient
from dotenv import load_dotenv

load_dotenv()

class DialogueLine(BaseModel):
    speaker: Literal["Fable", "Isabella"] = Field(..., description="Name of the speaker")
    speaker_gender: Literal["male", "female"] = Field(..., description="Gender of the speaker")
    content: str = Field(..., description="Speaker's dialogue content")


class PodcastPart(BaseModel):
    title: str = Field(..., description="Title of discussion part")
    summary: str = Field(..., description="Concise summary of key points to be discussed in this part. Be very specific and detailed.")
    questions: List[str] = Field(..., description="List of questions to be answered in this part.", min_length=4)
    dialogue: List[DialogueLine] = Field(
        ...,
        description=(
            "Sequence of dialogue exchanges."
            "It should be a conversation between two people."
            "The dialogue should be based on the questions and the summary."
            "It should long and comperhensive."
            "Be creative and make it interesting."
            "Be natural and not scripted."
            "Add pauses, breaks, and other natural human behaviors to make it more engaging."
            "Be funny and interesting."
        ),
        min_length=5
    )
    
    
class Podcast(BaseModel):
    parts: List[PodcastPart] = Field(..., description="List of parts of the podcast", min_length=5)
    
    

# Create a PydanticAI instance
# TODO: Change the model to a better one that can handle the structured output
# _model_name = "llama-3.3-70b-versatile"
# _model = GroqModel(
#     _model_name, 
#     # groq_client=GroqClient(base_url="https://api.me-central-1.groqcloud.com"),
# )

_model = OpenAIModel("gpt-4o") # Best model so far for structured output
podcast_planner_agent = Agent(
    _model,
    system_prompt=("You are a model that creates a dialogue from a content of a file for the purpose of explaining and discussing the content in an engaging way."),
    result_type=Podcast,
    result_retries=2,
    result_tool_name="podcast_creator",
    result_tool_description="Create a dialogue from a content of a file",
)