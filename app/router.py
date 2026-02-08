from fastapi import APIRouter, Request
from fastapi.responses import Response
from playwright.async_api import Browser

from app.schemas import GeneratePdfRequest
from app.service import generate_pdf_bytes

router = APIRouter(prefix="/pdf-generator")


@router.post("/generate-pdf")
async def generate_pdf(request: Request, payload: GeneratePdfRequest) -> Response:
    browser: Browser = request.app.state.browser
    pdf_bytes = await generate_pdf_bytes(payload, browser)

    return Response(content=pdf_bytes, media_type="application/pdf")


@router.get("/health")
async def health_check():
    return {"status": "ok"}
