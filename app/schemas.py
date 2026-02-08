from pydantic import BaseModel, Field


class AttachmentIn(BaseModel):
    filename: str
    content_base64: str


class AttachmentFileData(BaseModel):
    name: str
    local_file_path: str


class GeneratePdfRequest(BaseModel):
    html: str
    attachments: list[AttachmentIn] = Field(default_factory=list)