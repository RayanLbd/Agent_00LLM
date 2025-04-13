from typing import List
from pydantic import BaseModel, Field
from agents import function_tool
import json


class CalculatorItemInput(BaseModel):
    item_name: str = Field(
        ..., description="Name of the item to be calculated (e.g., 'hotel', 'flight')"
    )
    item_price: float = Field(
        ..., description="Price of the item to be calculated (e.g., 100.0), in euros"
    )
    item_quantity: int = Field(
        ...,
        description="Quantity of the item to be calculated, e.g., 2 for 2 people (flight) or 2 nights (hotel).",
    )


class CalculatorInput(BaseModel):
    items: List[CalculatorItemInput] = Field(
        ..., description="List of items to be calculated"
    )


@function_tool
def calculator(input: CalculatorInput) -> str:
    """
    Use this tool to calculate the total price of items.
    The function will return a JSON string containing the total price.
    """
    total_price = 0.0
    for item in input.items:
        item_total = item.item_price * item.item_quantity
        total_price += item_total
    result = {
        "total_price": total_price,
    }

    return json.dumps(result)
