"""Domain models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    tenant_id: str
    role: str  # "member" or "admin" (admins are scoped to their own tenant)


@dataclass(frozen=True)
class Project:
    id: str
    tenant_id: str
    owner_id: str
    name: str
    archived: bool
