import json
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

@dataclass
class Item:
    sport_league: str = ''
    event_date_utc: str = ''
    team1: str = ''
    team2: str = ''
    pitcher: str = ''
    period: str = ''
    line_type: str = ''
    price: str = ''
    side: str = ''
    team: str = ''
    spread: float = 0.0

driver = webdriver.Chrome()

driver.get('https://veri.bet/odds-picks?filter=upcoming')
time.sleep(20) #aumente o time caso o site demore para carregar

items = []
events = driver.find_elements(By.CLASS_NAME, 'dataTable')

for event in events:
    item = Item()
    item.sport_league = event.find_elements(By.TAG_NAME, 'h2')[0].text

    badge_element = event.find_element(By.CSS_SELECTOR, 'span.badge.badge-light')
    
    event_date_text = badge_element.text
    
    match = re.search(r'\((\d{2}/\d{2}/\d{4})\)', event_date_text)
    if match:
        item.event_date_utc = match.group(1)
    else:
        item.event_date_utc = "Data não encontrada"

    span_elements = event.find_elements(By.CSS_SELECTOR, 'a.text-muted')
    item.team1 = span_elements[0].text
    item.team2 = span_elements[1].text
    item.period = event.find_element(By.CSS_SELECTOR, 'td span.text-muted').text
    line_type_elements = event.find_elements(By.CSS_SELECTOR, 'tr span.text-muted')
    if len(line_type_elements) >= 3:
        item.line_type = line_type_elements[2].text
    item_price_elements = event.find_elements(By.CSS_SELECTOR, '.col-lg span.text-muted')
    item.price = item_price_elements[5].text    
    item.side = span_elements[0].text
    item.team = span_elements[0].text
    spread_elements = event.find_elements(By.CSS_SELECTOR, '.col-lg span.text-muted')
    spread_elements_1 = spread_elements[6].text
    spread_elements_2 = spread_elements[10].text
    valor1 = int(spread_elements_1.split('\n')[0])
    valor2 = int(spread_elements_2.split('\n')[0])
    item.spread = valor1 + valor2
    items.append(item)

driver.quit()

json_data = json.dumps([item.__dict__ for item in items], indent=2)
print(json_data)