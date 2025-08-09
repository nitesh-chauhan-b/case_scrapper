# import requests
# import os


# def download_pdf(pdf_url, filename):
#     # Ensure the directory exists
#     os.makedirs("static/pdf", exist_ok=True)
    
#     # Set the path where the PDF will be saved
#     save_path = os.path.join("static/pdf", filename)

#     try:
#         response = requests.get(pdf_url, stream=True)
#         if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
#             with open(save_path, 'wb') as f:
#                 f.write(response.content)
#             print(f"PDF saved to: {save_path}")
#         else:
#             print(f"Failed to download PDF. Status: {response.status_code}")
#     except Exception as e:
#         print(f"Error while downloading PDF: {e}")


# pdf_url = "https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/display_pdf.php?filename=bzPoyUlszYLCUcCpirIpqJq8JHuZuQx3VlTxAM2gAp5mCKjtC0oTFisdYS3PkDCD&caseno=APOT/26/2024&cCode=1&appFlag=&cino=WBCHCO0003192024&state_code=16"
# filename = "APOT_26_2024.pdf"

# download_pdf(pdf_url, filename)

import os
if os.path.exists("static/pdf"):
    files = os.listdir("static/pdf")
    files.sort(key=lambda x: int(x.replace("order_", "").replace(".pdf", "")))

    print(files)
    