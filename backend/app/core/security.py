from dataclasses import dataclass
from fastapi import Header


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: tuple[str, ...]
    branch_id: str | None = None


async def optional_principal(authorization: str | None = Header(default=None)) -> Principal | None:
    """Authentication integration seam.

    Future modules will validate JWT/OIDC tokens here. Module 01 intentionally exposes
    the dependency contract without enforcing authentication.
    """
    if not authorization:
        return None
    return Principal(subject="integration-placeholder", roles=("system",))
