import os
import re
from collections import defaultdict

PDF_IMAGE_DIR = "/home/bonnietyler/doc-chatbot/images/pdf"

def build_page_image_map():
    """
    Returns:
    {
      1: ["/images/pdf/xxx_page1_0.png"],
      2: ["/images/pdf/xxx_page2_0.png"]
    }
    """
    page_map = defaultdict(list)

    pattern = re.compile(r"_page(\d+)_\d+\.png$")

    for filename in os.listdir(PDF_IMAGE_DIR):
        match = pattern.search(filename)
        if not match:
            continue

        page_number = int(match.group(1))

        # IMPORTANT: path must match what UI expects
        page_map[page_number].append(
            f"/images/pdf/{filename}"
        )

    return page_map
