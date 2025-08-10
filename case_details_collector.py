from bs4 import BeautifulSoup
import os
import asyncio

async def get_case_details():
    file_path = "scrapped_page/case_details.html"

    # Prepare dictionary from known fields
    data = {}

    try:
        if os.path.exists(file_path):

            # Reading html page
            with open(file_path,"r") as file:
                html_doc = file.read()

            # using Beutiful Soup for extraction
            soup = BeautifulSoup(html_doc,"html.parser")


            # Getting Case Details

            case_details = soup.find("h2",string="Original Side")

            case_details_str = case_details.find_next_sibling("div")

            case_details_text = case_details_str.get_text(separator="\n",strip=True)

            # Split into lines and strip
            lines = [line.strip().replace(u'\xa0', ' ') for line in case_details_text.split('\n') if line.strip()]
            # print(lines,"\n\n")
            i = 0
            while i < len(lines):
                if "Case Type" in lines[i]:
                    data["case_type"] = lines[i+1].replace(':', '').strip()
                elif "Filing Number" in lines[i]:
                    data["filing_number"] = lines[i+1].replace(':', '').strip()
                elif "Filing Date" in lines[i]:
                    data["filing_date"] = lines[i+1].replace(':', '').strip()
                elif "Registration Number" in lines[i]:
                    data["registration_number"] = lines[i+1].replace(':', '').strip()
                elif "Registration Date" in lines[i]:
                    data["registration_date"] = lines[i+1].replace(':', '').strip()
                elif "CNR Number" in lines[i]:
                    data["cnr_number"] = lines[i+1].replace(':', '').strip()
                i += 1

            # Getting Case Status Details
            case_status_details = soup.find("h2",class_="h2class")

            # Getting it's next div which contains all the details
            case_status = case_status_details.find_next("div")

            # Getting all the text from the div
            case_status_text = case_status.get_text(separator="\n", strip=True)

            # Split the text into lines and strip whitespace
            lines = [line.strip().replace(u'\xa0', ' ') for line in case_status_text.split('\n') if line.strip()]

            # print(lines)
            # Process lines in pairs
            i = 0
            while i < len(lines):
                if "First Hearing Date" in lines[i]:
                    data["first_hearing_date"] = lines[i+1].replace(':', '').strip()
                elif "Next Hearing Date" in lines[i]:
                    data["next_hearing_date"] = lines[i+1].replace(':', '').strip()
                elif "Stage of Case"  in lines[i]:
                    data["case_stage"] = lines[i+1].replace(':', '').strip()
                elif "Case Status" in lines[i]:
                    data["case_stage"] = lines[i+1].replace(':', '').strip()
                    # Making the first hearing and last hearing date as N/A for temparary perpose
                    data["first_hearing_date"] = "N/A"
                    data["next_hearing_date"] = "N/A"
                elif "Coram" in lines[i]:
                    data["coram"] = lines[i+1].replace(':', '').strip()
                elif "State" in lines[i]:
                    data["state"] = lines[i+1].replace(':', '').strip()
                elif "District" in lines[i]:
                    data["distict"] = lines[i+1].replace(':', '').strip()
                i += 1

            # print(data)

            # Getting parties Details
            petitioner = soup.find("span",class_="Petitioner_Advocate_table")
            lines = [line.strip() for line in petitioner.get_text(separator="\n").split("\n") if line.strip()]

            petitioners = []
            for line in lines:
                if ")" in line:
                    ans = line.split(")")[-1].strip()
                    petitioners.append(ans)


            # print("Petitioner Name :",petitioners)
            # print("Petitioner Advocate Name :",advocate_name)

            # data["petitioner_advocate_name"] = advocate_name

            # Respondent Details

            respondent = soup.find("span",class_="Respondent_Advocate_table")

            raw_lines = [line.strip() for line in respondent.get_text(separator="\n").split("\n") if line.strip()]
            respondents = []
            for line in raw_lines:
                respondents.append(line.split(")")[-1].strip())
            # print(respondents)

            # Adding respondents and petitioners
            data["petitioner_names"] = petitioners
            data["respondent_names"] = respondents


            print(data)


            # Getting acts 
            try:
                # If table Doen't Exists
                data["acts"] = ["N/A"]
                data["sections"] = ["N/A"]
    
                act_table = soup.find("table",id="act_table")

                # Geting all the rows (excluding the header)
                rows = act_table.find_all('tr')[1:]  # skip the header row

                # For Storing the data
                acts = []
                sections = []
                # Extracting acts and sections
                for row in rows:
                    cols = row.find_all('td')
                    act = cols[0].get_text(strip=True)
                    section = cols[1].get_text(strip=True)
                    # print("Act:", act)
                    # print("Section:", section)

                    acts.append(act)
                    sections.append(section)

                
                # Adding data
                data["acts"] = acts
                data["sections"] = sections

            except Exception as e:
                print("Act Table Scrapping Error : ",e)
            try:
                # Getting orders details
                order_table = soup.find("table",class_="order_table")
                orders = order_table.find_all("tr")[1:]

                # For Storing details
                judges = []
                order_dates = []
                # Getting all the order and thier order pdf
                for order in orders:
                    cols = order.find_all("td")
                    
                    # Extract Judge, Order Date, and Order Details
                    judge = cols[2].get_text(strip=True)
                    order_date = cols[3].get_text(strip=True)
                    # order_link_tag = cols[4].find("a")
                    # order_link = order_link_tag['href'] if order_link_tag else None

                    judges.append(judge)
                    order_dates.append(order_date)
                    # order_pdf_link.append(website_prefix)
                
                # Getting Stored PDF links
                order_pdf_link = []
                if os.path.exists("static/pdf"):
                    files = os.listdir("static/pdf")

                    # Making files sorted for orders 
                    files.sort(key=lambda x: int(x.replace("order_", "").replace(".pdf", "")))

                    for file in files:
                        order_pdf_link.append("./static/pdf/"+file)


                # Adding orders details
                data["judges"] = judges
                data["order_dates"] = order_dates
                data["order_links"] = order_pdf_link
            except Exception as e:
                print("Orders Table Scrapping Error :",e)
            print(data)
        return data
    except Exception as e:
        print("Scrapping Error : ",e)


if __name__ =="__main__":
    asyncio.run(get_case_details())