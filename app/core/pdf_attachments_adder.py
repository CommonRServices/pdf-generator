import pathlib

import pikepdf

from app.schemas import AttachmentFileData


def add_attachments_to_pdfa(pdf_path: str, attachments: list[AttachmentFileData]):
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pike_pdf_file:
        for att in attachments:
            if not att.local_file_path:
                continue
            filespec = pikepdf.AttachedFileSpec.from_filepath(
                pike_pdf_file,
                pathlib.Path(att.local_file_path),
                description="Attached from the e-mail",
                relationship=pikepdf.Name.Supplmement, # type: ignore[call-arg]
            )
            pike_pdf_file.attachments[att.name] = filespec

            af = pike_pdf_file.Root.get(pikepdf.Name.AF)
            if af is None:
                af = pikepdf.Array()
                pike_pdf_file.Root[pikepdf.Name.AF] = af
            af.append(filespec.obj)

        pike_pdf_file.save(deterministic_id=True)
