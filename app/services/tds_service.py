from app.schemas import GameResponse
import google.generativeai as genai
import json
import re
import os

def model_to_json(model_instance):
    """
    Converts a Pydantic model instance to a JSON string.
    Args:
        model_instance (YourModel): An instance of your Pydantic model.
    Returns:
        str: A JSON string representation of the model.
    """
    return model_instance.model_dump_json()

def extract_json(text_response):
    # This pattern matches a string that starts with '{' and ends with '}'
    pattern = r'\{[^{}]*\}'
    matches = re.finditer(pattern, text_response)
    json_objects = []
    for match in matches:
        json_str = match.group(0)
        try:
            # Validate if the extracted string is valid JSON
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            # Extend the search for nested structures
            extended_json_str = extend_search(text_response, match.span())
            try:
                json_obj = json.loads(extended_json_str)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                # Handle cases where the extraction is not valid JSON
                continue
    if json_objects:
        return json_objects
    else:
        return None  # Or handle this case as you prefer

def extend_search(text, span):
    # Extend the search to try to capture nested structures
    start, end = span
    nest_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            nest_count += 1
        elif text[i] == '}':
            nest_count -= 1
            if nest_count == 0:
                return text[start:i+1]
    return text[start:end]

def get_prompt(rounds: None, gender:None, age_group:None, playing_with:None, user_prompt:None):
    json_model = model_to_json(GameResponse(truth=["truth 1", "truth 2"], dare=["dare 1", "dare 2"]))
    base_prompt = f"You are expert in Truth & Dare Game. You are fun, interesting and creative. Generate {rounds} Truth questions and {rounds} tough dare suggestions.  Questions should be for {gender} gender in age group of {age_group}. People playing the game are {playing_with}. User Request: {user_prompt}"
    optimized_prompt = base_prompt + f'.Please provide a response in a structured JSON format that matches the following model: {json_model}'
    return optimized_prompt

def get_tds_answer(prompt):
    genai.configure(api_key=os.getenv("GEMENI_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt, safety_settings={
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL' : 'BLOCK_NONE',
        'DANGEROUS' : 'BLOCK_NONE'
    })
    json_objects = extract_json(response.text)
    return json_objects