from fastapi import APIRouter, Depends
from app.core.security import Principal, optional_principal

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/auth-integration")
async def auth_integration(principal: Principal | None = Depends(optional_principal)) -> dict:
    return {"auth_enforced": False, "principal_detected": principal is not None}
