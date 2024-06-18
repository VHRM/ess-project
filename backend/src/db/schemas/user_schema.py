
from src.db.schemas.model_schema import ModelSchema


class UserSchema(ModelSchema):
  bson_type: str = "object"
  required: list = ["id", "email", "password", "cpf", "name", "role"]
  properties: dict = {
    "id": {
      "bson_type": "string",
      "description": "The user's unique identifier"
    },
    "email": {
      "bson_type": "string",
      "description": "The user's email"
    },
    "password": {
      "bson_type": "string",
      "description": "The user's password"
    },
    "cpf": {
      "bson_type": "string",
      "description": "The user's CPF"
    },
    "name": {
      "bson_type": "string",
      "description": "The user's name"
    },
    "role": {
      "bson_type": "string",
      "description": "The user's role"
    },
    "created_at": {
      "bson_type": "string",
      "description": "The user's creation time"
    },
    "deleted": {
      "bson_type": "bool",
      "description": "The user's deletion status"
    },
    "token": {
        "bson_type": "string",
        "description": "The user's bearer token"
    }
  }

  def get(self) -> dict:
        return {
            "bson_type": self.bson_type,
            "required": self.required,
            "properties": self.properties
        }