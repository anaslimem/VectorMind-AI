from fastapi import APIRouter, Response

router = APIRouter()

# Minimal Prommetheus-compatible metric endpoint
@router.get("")
async def metrics():
    body = """# HELP vector_mind_up 1 if API is up\n# TYPE vector_mind_up gauge\nvector_mind_up 1\n"""
    return Response(content=body, media_type="text/plain; version=0.0.4")
