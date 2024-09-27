from marshmallow import Schema, fields
from pydantic import BaseModel
from typing import List

class TDSSchema(Schema):
    rounds = fields.Int(required=True)
    playing_with = fields.Str(required=True)
    age_group = fields.Str(required=True)
    gender = fields.Str(required=True)
    user_prompt = fields.Str(required=True)

class GameResponse(BaseModel):
    truth: List[str]
    dare: List[str]