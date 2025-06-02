import asyncio
import sys
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# requirements: install playwright fist (heavy dependencies!)
#pip install playwright
#playwright install

def clean_text(elem):
    if elem:
        return ' '.join(elem.stripped_strings)
    return ""

def parse_date(date_str):
    try:
        dt = datetime.strptime(date_str.strip(), "%b %d %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Warning: Could not parse date '{date_str}': {e}")
        return date_str

def parse_resolved_rounds(html_path, model_title):
    with open(html_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    heading = soup.find('h1', string="Resolved Rounds")
    if not heading:
        print(f"Could not find 'Resolved Rounds' section for model '{model_title}'.")
        return []

    table = heading.find_next('table', class_='table')
    if not table:
        print(f"Could not find the resolved rounds table for model '{model_title}'.")
        return []

    rows = []
    for tr in table.find_all('tr', class_='resolved'):
        tds = tr.find_all('td')
        if len(tds) < 9:
            continue
        
        round_num = clean_text(tds[0])
        close_date = parse_date(clean_text(tds[1]))
        resolve_date = parse_date(clean_text(tds[2]))
        payout = clean_text(tds[3])
        at_risk = clean_text(tds[4])
        pf = clean_text(tds[5])
        multipliers = clean_text(tds[6])
        corr = clean_text(tds[7])
        mmc = clean_text(tds[8])

        rows.append({
            "model_title": model_title,
            "Round": round_num,
            "Close": close_date,
            "Resolve": resolve_date,
            "Payout": payout,
            "At-risk": at_risk,
            "PF": pf,
            "Multipliers": multipliers,
            "corr": corr,
            "mmc": mmc,
        })

    return rows

def save_to_csv(data, csv_path):
    if not data:
        print("No data to write to CSV.")
        return

    headers = list(data[0].keys())
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} rows to {csv_path}")

async def fetch_and_dump_html(url, html_path="temp.html"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        html = await page.content()
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        await browser.close()
        print(f"✅ HTML dumped to {html_path}")

async def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py model1,model2,model3")
        return

    model_titles = sys.argv[1].split(',')
    all_rows = []
    html_path = "temp.html"
    csv_path = "resolved_rounds.csv"

    for model_title in model_titles:
        model_title = model_title.strip()
        if not model_title:
            continue

        url = f"https://crypto.numer.ai/{model_title}"
        print(f"Fetching data for model: {model_title} from {url} ...")
        await fetch_and_dump_html(url, html_path)
        rounds = parse_resolved_rounds(html_path, model_title)
        if rounds:
            all_rows.extend(rounds)
        else:
            print(f"No data extracted for model '{model_title}'.")

    if all_rows:
        save_to_csv(all_rows, csv_path)
    else:
        print("No data extracted for any models.")

if __name__ == "__main__":
    asyncio.run(main())

