from pydantic import BaseModel, Field, field_validator


class OwnerIn(BaseModel):
    notional_code: int
    password: str = Field(min_length=10)

    @field_validator('notional_code')
    def notional_code_validate(cls, notional_code: int):
        if len(str(notional_code)) < 10 or len(str(notional_code)) > 10:
            raise ValueError('Invalid notional code')
        return notional_code

    class Config:
        json_schema_extra = {
            'example': {
                'notional_code': 1234567890,
                'password': 'jios*23N('
            }
        }


class OwnerRead(BaseModel):
    notional_code: int
    hashed_password: str

    class Config:
        from_attributes = True
