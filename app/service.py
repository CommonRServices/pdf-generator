import base64
import os

from playwright.async_api import Browser

from app.core.html_to_pdf import html_string_to_pdf
from app.core.pdf_attachments_adder import add_attachments_to_pdfa
from app.core.pdfa_convertor import convert_to_pdfa
from app.core.temp_dir_storage import TempDirStorage
from app.schemas import AttachmentFileData, GeneratePdfRequest


async def generate_pdf_bytes(request: GeneratePdfRequest, browser: Browser) -> bytes:
    with TempDirStorage() as temp_storage:
        initial_pdf_path = os.path.join(temp_storage, "initial.pdf")
        pdfa_pdf_path = os.path.join(temp_storage, "pdfa.pdf")

        await html_string_to_pdf(request.html, initial_pdf_path, browser)

        convert_to_pdfa(initial_pdf_path, pdfa_pdf_path)

        if request.attachments:
            attachment_file_data_list: list[AttachmentFileData] = []

            for att in request.attachments:
                decoded_content = base64.b64decode(att.content_base64)
                local_path = temp_storage.save_bytes(att.filename, decoded_content)

                attachment_file_data_list.append(
                    AttachmentFileData(
                        name=att.filename,
                        local_file_path=local_path,
                    )
                )

                add_attachments_to_pdfa(pdfa_pdf_path, attachment_file_data_list)

        with open(pdfa_pdf_path, "rb") as f:
            result = f.read()

        return result
