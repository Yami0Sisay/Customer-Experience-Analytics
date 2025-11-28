# Customer-Experience-Analytics

**Week 2 – Task 1: Data Collection and Preprocessing**  
This repository analyzes customer sentiment and user experience for three major Ethiopian mobile banking apps:
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

Task 1 focuses on:

- Scraping Google Play Store reviews  
- Cleaning and preprocessing the data  
- Saving structured datasets for analysis  
- Documenting methodology using GitHub best practices  
---

---

## Task 1 Overview 
Task 1 involves four core components

### 1. Git Setup  
- Created repo with clean structure
- Added .gitignore (ignoring pycache, env files, notebooks checkpoints)
- Added requirements.txt
- Used a dedicated feature branch: task-1
- Committed in small, logical steps

### 2. Web Scraping  
Using `google-play-scraper`, the pipeline collected:
- Review text  
- Rating (1–5)  
- Timestamp  
- Bank code  
- App ID
- Source platform  

The scraper gathers 600 reviews per bank (1,800 total), making cross-bank comparisons fair and balanced.

### 3. Preprocessing  
The automated cleaning pipeline performed:

- Duplicate removal  
- Missing value handling  
- Date normalization (`YYYY-MM-DD`)  
- Text cleaning  
- Rating validation  
- Added metadata (`text_length`, `bank_code`)  

### 4. EDA Notebook
The notebook includes:
- Ratings distribution
- Reviews per bank
- Review length distribution
- Interpretation of patterns
- Reproducible code for visualizing processed data

### How the Code Works 
---

#### **1. `config.py`**

**Defines:**
- App IDs for each bank  
- Number of reviews per bank  
- Retry settings  
- File paths for raw & processed data  

**Purpose:**  
Keeps the entire project configurable without editing individual scripts.

---

#### **2. `scripts/scraper.py`**

**Responsibilities:**
- Loads settings from `config.py`  
- Fetches metadata for each app  
- Scrapes reviews using `google-play-scraper`  
- Saves:  
  - `data/raw/reviews_raw.csv`  
  - `data/raw/app_info.csv`  

**Key Features:**
- Automatically loops through all apps in `APP_IDS`  
- Uses progress bars (`tqdm`)  
- Handles retries  
- Fully reproducible  

**To run:**
```bash
python scripts/scraper.py
```
or run it inside the notebook

#### **3. `scripts/preprocessing.py`**

**Responsibilities:**
- Loads raw scraped data  
- Removes duplicates  
- Drops empty or invalid reviews  
- Normalizes dates  
- Cleans text  
- Validates rating values  
- Adds new columns  
- Saves:  
  - `data/processed/reviews_processed.csv`  

**Generates a detailed report showing:**
- Data retention rate  
- Number of removed rows  
- Rating distribution  
- Review length statistics  
- Reviews per bank  

**To run:**
```bash
python scripts/preprocessing.py
```


### 📁 Project Structure  

```bash
Customer-Experience-Analytics/
│
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── Ci.yml
│
├── data/
│ ├── raw/
│ │ ├── reviews_raw.csv
│ │ └── app_info.csv
│ └── processed/
│ └── reviews_processed.csv
│
├── scripts/
│ ├── scraper.py
│ ├── preprocessing.py
│ ├── __init__.py
│ └── README.md
│
├── notebooks/
│   ├── __init__.py
│   ├── README.md
│   └── preprocessing_EDA.ipynb
│
├── .env
│
├── tests/
│   └── __init__.py
│
├── config.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

