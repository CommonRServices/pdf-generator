from playwright.async_api import Browser


async def html_string_to_pdf(html_content: str, output_pdf_path: str, browser: Browser):
    context = await browser.new_context()
    page = await context.new_page()
    await page.set_content(html_content, wait_until="load")
    await page.pdf(path=output_pdf_path, format="A4", print_background=True)
    await page.close()
    await context.close()
