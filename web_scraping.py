import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def datos_ICAB(url):
    d = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    try:
        req = requests.get(url, headers=headers, timeout=10)
        req.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"Error": str(e), "status_code": req.status_code if 'req' in locals() else "N/A"}

    soup = BeautifulSoup(req.text, "html.parser")

    try:
        d["url"] = req.url
        d["id"] = d["url"].split("=")[-1]
        d["Nom advocat"] = soup.find("h1", class_="title").text.strip()
        d["E-mail"] = soup.find("li", class_="email").text.strip() if soup.find("li", class_="email") else "No Email"
        d["Publicitat"] = soup.find("span", class_="note-error").text.strip() if soup.find("span", class_="note-error") else "No Info"
    except AttributeError as e:
        d["Error"] = f"Missing data: {str(e)}"

    return d

def main():
    url = 'https://www.icab.es/ca/colegi/membres/index.html?id='
    start = 500
    end = 1500  #possible f:48117    400 x 15 min
    data_list = []

    for i in range(start, end):
        data = datos_ICAB(url + str(i))
        data_list.append(data)
        time.sleep(1)  # Delay to avoid overloading the server

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data_list)
    
    # Save the DataFrame to an Excel file
    df.to_excel('ICAB_members.xlsx', index=False)

if __name__ == '__main__':
    main()