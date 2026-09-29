from fastapi import APIRouter
from app.tools.schema_tools import get_schema

router = APIRouter()

@router.get("/schema")
def schema():
    return get_schema()
