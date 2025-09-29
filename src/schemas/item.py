from pydantic import BaseModel, field_validator


class AddItemPayload(BaseModel):
    id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v
