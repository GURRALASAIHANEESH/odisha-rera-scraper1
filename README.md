# 🏗️ Odisha RERA Web Scraper using Selenium

This project is a Python-based web scraper built with Selenium to extract real estate project details from the [Odisha RERA Official Website](https://rera.odisha.gov.in/projects/project-list). It collects important information like the project name, promoter name, RERA registration number, promoter address, and GST number, and stores the data in a CSV file.

---

## 📌 Features

- ✅ Handles dynamic content loading using `WebDriverWait`
- ✅ Extracts key project details from individual project pages
- ✅ Navigates and interacts with multiple tabs (like Promoter Details)
- ✅ Implements error handling, retries, and graceful fallbacks
- ✅ Saves output to a clean, structured `.csv` file
- ✅ Logs progress and errors for easier debugging

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/yourusername/odisha-rera-webscraper.git
cd odisha-rera-webscraper
2. Install Dependencies
Ensure you have Python 3.8+ installed. Then install the required packages:
pip install selenium
✅ Note: Make sure ChromeDriver is installed and the path is updated in the script (default: C:\Users\yourname\chromedriver.exe)

📄 Usage
To scrape project data:
python odisha_rera_scraper.py
By default, the script scrapes data from the first 6 projects and saves it to:
odisha_rera_output.csv
📊 Sample Output (CSV)
Rera Regd. No	Project Name	Promoter Name	Address of the Promoter	GST No.
RP/XX/YYYY	XYZ Heights	ABC Developers	Bhubaneswar, Odisha	22XXXXX
⚠️ Known Issues
Some elements may fail to load due to slow internet — handled using retries and fallbacks.

File write permission errors are automatically handled by saving output to a timestamped fallback file.

📦 File Structure

├── odisha_rera_scraper.py     # Main scraping script
├── odisha_rera_output.csv     # Output file (auto-generated)
├── README.md                  # Project documentation

🙌 Acknowledgments
Selenium WebDriver for browser automation

Odisha RERA Portal for public data

🔗 Connect with Me
Feel free to ⭐ this repo, fork it, or reach out!

LinkedIn

GitHub


