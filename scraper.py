from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
import csv
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CHROMEDRIVER_PATH = r'C:\Users\gurra\chromedriver.exe'

def scrape_odisha_rera_project_details(max_projects=6):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    project_data = []
    csv_file = "odisha_rera_output.csv"

    try:
        driver.get("https://rera.odisha.gov.in/projects/project-list")

        try:
            close_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Close')]")
            driver.execute_script("arguments[0].click();", close_button)
            time.sleep(1)
        except NoSuchElementException:
            pass

        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card"))
        )

        cards = driver.find_elements(By.CSS_SELECTOR, "div.card.project-card")

        for index in range(min(max_projects, len(cards))):
            retries = 3
            while retries > 0:
                try:
                    cards = driver.find_elements(By.CSS_SELECTOR, "div.card.project-card")
                    if index >= len(cards):
                        break
                    card = cards[index]

                    view_link = WebDriverWait(card, 15).until(
                        EC.element_to_be_clickable((By.XPATH, ".//a[contains(., 'View Details')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_link)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", view_link)

                    try:
                        close_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Close')]")
                        driver.execute_script("arguments[0].click();", close_button)
                        time.sleep(1)
                    except NoSuchElementException:
                        pass

                    WebDriverWait(driver, 90).until(
                        EC.all_of(
                            EC.visibility_of_element_located((
                                By.XPATH,
                                "//div[@class='details-project ms-3']//label[contains(text(), 'Project Name')]/following-sibling::strong"
                            )),
                            EC.visibility_of_element_located((
                                By.XPATH,
                                "//div[@class='details-project ms-3']//label[contains(text(), 'RERA')]/following-sibling::strong"
                            ))
                        )
                    )

                    project_name = ""
                    rera_regd_no = ""
                    promoter_name = ""
                    promoter_address = ""
                    gst_no = ""

                    def extract_text(xpath, wait=30, retries=3):
                        for attempt in range(retries):
                            try:
                                return WebDriverWait(driver, wait).until(
                                    EC.visibility_of_element_located((By.XPATH, xpath))
                                ).text.strip()
                            except Exception:
                                time.sleep(2)
                        return "--"

                    project_name = extract_text("//div[@class='details-project ms-3']//label[contains(text(), 'Project Name')]/following-sibling::strong")
                    rera_regd_no = extract_text("//div[@class='details-project ms-3']//label[contains(text(), 'RERA')]/following-sibling::strong")

                    try:
                        promoter_tab = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Promoter Details')]"))
                        )
                        driver.execute_script("arguments[0].click();", promoter_tab)
                        WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='ms-3']"))
                        )
                        time.sleep(1)
                    except Exception:
                        pass

                    promoter_name = extract_text("//div[@class='ms-3']//label[contains(text(), 'Company Name') or contains(text(), 'Propietory Name')]/following-sibling::strong")
                    promoter_address = extract_text("//div[@class='ms-3']//label[contains(text(), 'Registered Office Address') or contains(text(), 'Address')]/following-sibling::strong")
                    gst_no = extract_text("//div[@class='ms-3']//label[contains(text(), 'GST No')]/following-sibling::strong", retries=2)

                    project_data.append([rera_regd_no, project_name, promoter_name, promoter_address, gst_no])
                    driver.back()
                    WebDriverWait(driver, 45).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card"))
                    )
                    time.sleep(1)
                    break

                except (StaleElementReferenceException, NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                    retries -= 1
                    time.sleep(3)
                    if retries == 0:
                        driver.back()
                        try:
                            WebDriverWait(driver, 45).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.project-card"))
                            )
                        except TimeoutException:
                            break

    except Exception as e:
        logging.error(f"Critical error: {str(e)}")

    finally:
        try:
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Rera Regd. No", "Project Name", "Promoter Name", "Address of the Promoter", "GST No."])
                writer.writerows(project_data)
                logging.info(f"Saved {len(project_data)} projects to {csv_file}")
        except PermissionError:
            logging.error(f"Permission denied when writing to {csv_file}.")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            fallback_file = f"odisha_rera_output_{timestamp}.csv"
            with open(fallback_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Rera Regd. No", "Project Name", "Promoter Name", "Address of the Promoter", "GST No."])
                writer.writerows(project_data)
                logging.info(f"Saved {len(project_data)} projects to fallback file {fallback_file}")

        driver.quit()

if __name__ == "__main__":
    scrape_odisha_rera_project_details(max_projects=6)
