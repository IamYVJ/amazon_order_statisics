from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

USE_FIREFOX = True # False for Chrome

USE_DRIVER_MANAGER = True # False if Chrome/Firefox Driver is in PATH

START_YEAR = 2022
END_YEAR = 2022

def write_csv(filename, data):
    fields = ['Date', 'Number', 'Units', 'Amount', 'Details', 'Name'] 
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, escapechar='\\') 
        csvwriter.writerow(fields) 
        csvwriter.writerows(data)


def all_orders(wd):
    data = []
    while True:
        sleep(10)
        orders = wd.find_elements(By.CLASS_NAME, 'a-box-group.a-spacing-base.order.js-order-card')
        # print('Scraping', len(orders))
        for order in orders:
            date = order.find_element(By.CLASS_NAME, 'a-column.a-span3').find_element(By.CLASS_NAME, 'a-color-secondary.value').text.strip()
            # date = order.find_element(By.CLASS_NAME, 'a-row.a-size-base').text
            total = float(order.find_element(By.CLASS_NAME, 'a-column.a-span2.yohtmlc-order-total').find_element(By.CLASS_NAME, 'a-color-secondary.value').text.replace(',', '').strip())
            details = order.find_element(By.CLASS_NAME, 'a-fixed-right-grid-col.actions.a-col-right').find_element(By.CLASS_NAME, 'a-color-secondary.value').text.strip()
            try:
                items = order.find_elements(By.CLASS_NAME, 'a-fixed-left-grid-inner')
                number = len(items)
                units = 0
                for item in items:
                    try:
                        units += int(item.find_element(By.CLASS_NAME, 'item-view-qty').text.strip())
                    except:
                        units += 1
            except:
                number = 1
                units = 1
            try:
                name = order.find_element(By.CLASS_NAME, 'a-fixed-left-grid-col.yohtmlc-item.a-col-right').find_element(By.CLASS_NAME, 'a-row').text.strip()
            except:
                name = ''
            if name =='' and number==1 and units==1:
                try:
                    number = int(order.find_element(By.CLASS_NAME, 'a-fixed-left-grid-col.a-col-right').text.replace('items in this order', '').strip())
                    units = number
                    try:
                        name = 'Amazon Fresh' if order.find_element(By.CLASS_NAME, 'a-fixed-left-grid-col.a-col-left').find_element(By.XPATH, 'div/img').get_attribute('alt').find('Amazon Fresh')!=-1 else ''
                    except:
                        pass
                except:
                    pass
            data.append([date, number, units, total, details, name])
        # print('Scraped', len(data))

        if len(wd.find_elements(By.CLASS_NAME, 'a-disabled.a-last'))>0:
            # print('No Next')
            break
        else:
            try:
                wd.find_element(By.CLASS_NAME, 'a-last').click() 
                # print('Next Clicked')
            except:
                # print('No Next II')
                break
    data = data[::-1]
    return data

def main():
    print('---------------------------------------------------------')
    print('                 Amazon Order Statistics')
    print('---------------------------------------------------------')
    try:
        years = list(range(START_YEAR, END_YEAR + 1))   
        if USE_FIREFOX:
            if USE_DRIVER_MANAGER:
                service = FirefoxService(executable_path=GeckoDriverManager().install())
                wd = webdriver.Firefox(service=service)
            else:
                wd = webdriver.Firefox()
        else:
            if USE_DRIVER_MANAGER:
                service = ChromeService(executable_path=ChromeDriverManager().install())
                wd = webdriver.Chrome(service=service)
            else:
                wd = webdriver.Chrome()
        # wd.implicitly_wait(20)
        wd.get('https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')
        input('Press Enter After Login...')
        print('---------------------------------------------------------')
        all_data = []

        for year in years:
            url = f'https://www.amazon.in/gp/your-account/order-history?opt=ab&digitalOrders=1&unifiedOrders=1&returnTo=&orderFilter=year-{year}'
            wd.get(url)
            print('Scraping', year)
            data = all_orders(wd)
            print(f'Scraped {len(data)} Orders in {year}')
            year_orders = len(data)
            year_items = sum(order[1] for order in data)
            year_units = sum(order[2] for order in data)
            year_amount = sum(order[3] for order in data)
            print(f'{year} Orders:', year_orders)
            print(f'{year} Items:', year_items)
            print(f'{year} Units:', year_units)
            print(f'{year} Amount:', "{:,}".format(round(year_amount, 2)))
            print('---------------------------------------------------------')
            all_data.extend(data)
            write_csv(f'{year}.csv', data)
        wd.quit()
        write_csv('all_years.csv', all_data)
        total_orders = len(all_data)
        total_items = sum(order[1] for order in all_data)
        total_units = sum(order[2] for order in all_data)
        total_amount = sum(order[3] for order in all_data)
        print()
        print('Total Orders:', total_orders)
        print('Total Items:', total_items)
        print('Total Units:', total_units)
        print('Total Amount:', "{:,}".format(round(total_amount, 2)))
        print()
    except Exception as e:
        print('Error:', str(e))
    input('Press Enter To Exit...')

if __name__ == "__main__":
    main()
