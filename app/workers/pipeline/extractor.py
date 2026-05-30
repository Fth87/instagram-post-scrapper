import json
from typing import List, Optional, Any
from PIL import Image
import google.generativeai as genai
from app.workers.pipeline.schemas import CompetitionExtraction

class GeminiExtractor:
    """
    Decoupled AI Service handling API communication with the Generative AI Model.
    Accepts raw caption strings and Pillow image objects, validating output against a Pydantic schema.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def extract_competition_details(
        self, 
        caption: str, 
        image: Optional[Image.Image] = None
    ) -> CompetitionExtraction:
        # Prompt instructing unified cross-referencing visual and text layouts
        prompt = (
            "You are an expert event data extractor. Carefully analyze the provided competition "
            "poster image AND the accompanying caption text to extract structured details about the competition.\n\n"
            "Instructions:\n"
            "1. Cross-reference data between the poster image and the caption text to find complete details.\n"
            "2. registration_link and guidebook_link must be extracted if present. Look for forms.gle, bit.ly, linktr.ee, or similar shortlinks.\n"
            "3. Parse all timelines. Format due_date cleanly as ISO 8601 strings (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ).\n"
            "4. Parse all categories. Provide price as a float (e.g. 150000.0). Set free categories to 0.0.\n"
            "5. Translate or keep text informative and clean. If details are missing, return null."
        )

        contents: List[Any] = [prompt, f"Instagram Caption:\n{caption}"]
        if image:
            contents.append(image)

        # Query LLM with strict response schemas
        response = self.model.generate_content(
            contents,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=CompetitionExtraction
            )
        )

        # Parse structural JSON response text to our Pydantic Model
        extracted_dict = json.loads(response.text)
        return CompetitionExtraction(**extracted_dict)
