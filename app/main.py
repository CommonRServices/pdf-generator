from contextlib import asynccontextmanager

from fastapi import FastAPI
from playwright.async_api import async_playwright

from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch()

    app.state.browser = browser

    yield

    await browser.close()
    await playwright.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(router)
