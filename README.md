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
```bash
git clone https://github.com/yourusername/odisha-rera-webscraper.git
cd odisha-rera-webscraper
