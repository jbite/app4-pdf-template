from pypdf import PdfReader, PdfWriter
import os
import re
import zipfile

def Split_pdf_by_pages(pdfreader, output_prefix, start_page, end_page=None):
    """
    Splits a PDF file into multiple files based on page ranges.

    Args:
        input_pdf: Path to the input PDF file.
        output_prefix: Prefix for the output PDF files (e.g., "output_part").
        start_page:
        end-page:

    Raises:
        FileNotFoundError: If the input PDF file does not exist.
        ValueError: If the ranges are invalid (e.g., end < start).
    """
    # if not os.path.exists(input_pdf):
    #     raise FileNotFoundError(f"Input PDF file '{input_pdf}' not found.")

    try:
        num_pages = len(pdfreader.pages)
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")
    
    if end_page is None:
        end_page = num_pages
        print(end_page,"|",num_pages,"|",type(start_page))

    if end_page is not None:
        if end_page <= start_page:
            raise ValueError(f"Invalid range {start_page}: end page ({end_page}) must be greater than start page ({start_page}).")
        if end_page > num_pages:
            end_page = num_pages #adjust end to max page if it exceeds number of pages

    # for i in range(start_page,end_page):
    if start_page-1 < 0 or end_page > num_pages:
        raise ValueError(f"Invalid start page in range {start_page}: {end_page}. Must be between 1 and {num_pages}")

   
    writer = PdfWriter()
    try:
        writer.append(pdfreader, "",(start_page-1,end_page))
    except IndexError:
        print(f"Warning: Page {end_page + 1} not found in the PDF. Skipping.") #Handles potential issues if a range exceeds the real number of pages

    output_filename = f"output\\{output_prefix}_{start_page}-{end_page}.pdf"
    try:
        with open(output_filename, "wb") as output_file:
            writer.write(output_file)
        print(f"Created {output_filename} (pages {start_page}-{end_page if end_page != num_pages else 'end'})")
    except Exception as e:
        print(f"Error writing output file: {e}")
    
    return output_filename

def split_pdf_by_ranges(pdfreader, output_prefix, ranges_string):
    """Splits a PDF into multiple parts based on comma-separated ranges and creates a zip archive."""
    
    ranges = []
    for part in ranges_string.split(','):
        match = re.match(r'(\d+)-(\d+)', part)
        if match:
            start, end = map(int, match.groups())
            ranges.append((start, end))
        elif re.match(r'(\d+)-', part):
            print(part)
            start = int(part[:-1].strip('-'))
            ranges.append((start, None))
        else:
            raise ValueError(f"Invalid range format: {part}. Use format 'start-end' or 'start-'")

    output_files = []
    try:
        for start, end in ranges:
            output_file = Split_pdf_by_pages(pdfreader, output_prefix, start, end)
            output_files.append(output_file)
    except (ValueError, FileNotFoundError) as e:
        raise  # Re-raise the exception to be handled by the caller

    zip_filename = f"output\\{output_prefix}_parts.zip"
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))
                os.remove(file) # Delete the individual PDF after adding to zip
        print(f"Created zip archive: {zip_filename}")
        return zip_filename
    except Exception as e:
        print(f"Error creating zip archive: {e}")
        # Clean up created PDF files in case of zip error
        for file in output_files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        return None