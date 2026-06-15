"""Domain models."""

from dataclasses import dataclass


@dataclass
class Invoice:
    event_id: str
    amount: int
