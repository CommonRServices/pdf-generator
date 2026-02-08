import subprocess


def convert_to_pdfa(input_pdf_path: str, output_pdfa_path: str):
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-o",
        output_pdfa_path,
        "-dPFDACompatibilityPolicy=1",
        "-sColorConversionStrategy=RGB",
        "-dPDFA=3",
        "--perfmir-file-read=pdf_assets/srgb.icc",
        "-c",
        "/ICCProfile (pdf_assets/srgb.icc) def",
        "-f",
        "pdf_assets/PDFA_def.ps",
        input_pdf_path,
    ]

    subprocess.run(gs_command, check=True)
