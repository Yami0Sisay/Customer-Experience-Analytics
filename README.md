# Customer-Experience-Analytics

**Week 2 **  
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

## Task 2 Overview

Task 2 focuses on quantifying user sentiment and identifying recurring themes in reviews to uncover satisfaction drivers and pain points.

### 1. Sentiment Analysis

The sentiment pipeline uses three models to ensure high coverage and reliability:
Main Model:
- distilbert-base-uncased-finetuned-sst-2-english
- Generates positive/negative probabilities
- Computes a final sentiment score
- Assigns a sentiment label
Additional Models (for comparison):
- VADER
- TextBlob
The pipeline outputs:
- Sentiment score (BERT, VADER, TextBlob)
- Sentiment label
Aggregated metrics:
- Mean sentiment per bank
- Mean sentiment per rating
Output file:
``` bash
data/processed/sentiment_results.csv
```
(included inside the thematic_results file)

### 2. Thematic Analysis

The goal is to identify recurring topics that reveal user frustrations and strengths.

Keyword Extraction:
The following were computed:
- Cleaned text
- Unigram frequencies
- Bigram frequencies
- TF-IDF (global and per bank)
- spaCy noun chunks
- Optional topic modeling (LDA)

This surfaces patterns such as:
“doesn’t work”, “mobile banking”, “user friendly”, “slow”, “login problem”.

Theme Assignment (Rule-Based):
Each review is matched to one or more of the following themes:
- Account Access & Login Issues
- App Performance & Stability
- User Interface & Experience
- Transaction & Payment Problems
- Features & Functionality
- Positive Experience
- Uncategorized (fallback)

Output file:
``` bash
data/processed/thematic_results.csv
```
This file contains sentiment labels + score + themes for every review.

### 3. EDA Notebooks

Two notebooks provide supporting analysis:
`sentiment_EDA.ipynb`:
- Sentiment distribution per bank
- Sentiment vs. star rating
- Compare BERT, VADER, TextBlob
- Examples of extreme positive/negative reviews

`thematic_EDA.ipynb`:
- TF-IDF top terms
- Bigram counts
- Word clouds
- LDA topics
- Theme examples with review text

### How the Code Works
`scripts/sentiment_analysis.py`
Processes reviews and generates:
- BERT sentiment probabilities
- TextBlob polarity
- VADER compound score
- Unified sentiment score and label
- Saves enriched dataset
Run with:
``` bash
python scripts/sentiment_analysis.py
```
`scripts/thematic_analysis.py`
Handles thematic analysis:
- Clean text
- Extract keywords + bigrams
- Compute TF-IDF
- Run optional LDA topic modeling
- Assign themes using rule-based logic
- Merge sentiment + theme results
- Save final CSV

Run with:
``` bash
python scripts/thematic_analysis.py
```
## Task 3 Overview
Task 3 focuses on storing the cleaned, structured dataset in a relational PostgreSQL database.
This simulates a real-world data engineering workflow where data needs to be persisted, queried, validated, and used by downstream analytics systems.

### 1. PostgreSQL Setup

To begin, PostgreSQL was installed locally and configured for the project.

Database Created:`bank_reviews`

Users Created:
- `postgres` (default superuser)
- `bank_user` (project user for Python insert operations)

Connection verified:
``` bash
psql -U bank_user -d bank_reviews
```
### 2. Database Schema
A clean, normalized schema was created with two tables: `banks` and `reviews`.

Banks Table
- Stores basic information about each bank.
``` bash
| Column    | Type         | Description             |
| --------- | ------------ | ----------------------- |
| bank_id   | INT (PK)     | Unique bank identifier  |
| bank_code | VARCHAR(10)  | CBE, BOA, DASHEN        |
| bank_name | VARCHAR(255) | Full bank name          |
| app_name  | VARCHAR(255) | App name on Google Play |
```
Reviews Table
- Stores all processed review records.
``` bash
| Column          | Type             | Description                |
| --------------- | ---------------- | -------------------------- |
| review_id       | UUID (PK)        | Review's unique ID         |
| bank_id         | INT (FK)         | References `banks.bank_id` |
| review_text     | TEXT             | Review content             |
| rating          | INT              | Star rating (1–5)          |
| review_date     | DATE             | Normalized date            |
| sentiment_label | VARCHAR(50)      | BERT sentiment label       |
| sentiment_score | DOUBLE PRECISION | BERT sentiment score       |
| source          | VARCHAR(50)      | Usually “Google Play”      |
```

Schema validation:
``` bash
\d banks;
\d reviews;
```
### 3. Data Insertion Using Python (psycopg2)
A dedicated insert pipeline was implemented using `Psycopg2`.

Steps completed:
- Loaded the cleaned dataset (reviews_processed.csv)
- Mapped each review's bank_code → bank_id
- Inserted bank metadata into the banks table
- Inserted 1,800+ reviews into the reviews table
- Committed all transactions safely
- Closed the connection

SQL checks:
```bash
SELECT COUNT(*) FROM reviews;

SELECT bank_name, COUNT(*)
FROM reviews r
JOIN banks b ON b.bank_id = r.bank_id
GROUP BY bank_name;

SELECT bank_name, AVG(rating)
FROM reviews r
JOIN banks b ON b.bank_id = r.bank_id
GROUP BY bank_name;
```
All tables were populated successfully.

### 4. Schema Export (SQL Dump)
A reproducible schema dump was generated and added to the repository:
`schema.sql`

Generated via:
```bash
"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U bank_user -d bank_reviews -s > schema.sql
```
This allows anyone to recreate the database structure exactly.

### 5. What Task 3 Enables

- Persistent storage for analysis or dashboards
- Ability to query reviews by rating, theme, sentiment, month, or bank
- Clean relationship structure through foreign keys

## Task 4 Overview
Task 4 focuses on generating insights and recommendations from the cleaned, enriched dataset (sentiment + themes).
The goal is to translate analytical outputs into business-relevant findings that help improve customer experience across the three banking apps.

This task consists of:
- Visual analysis
- Insights from sentiment and themes
- Drivers and pain points for each bank
- Ethical considerations
- Final actionable recommendations

### 1. Insights & Interpretation
After merging sentiment and themed review data, five key analyses were conducted:

#### A. Sentiment Distribution per Bank
A bar chart compares the count of positive vs negative reviews for each bank.
Key insight:
- Dashen has the highest positive share.
- BOA has the highest negative share.
- CBE sits in the middle with a slight positive tilt.

#### B. Theme Distribution per Bank
The frequency of each theme (e.g., login issues, performance problems, UI complaints) was Visualized.
Key insight:
- Positive Experience dominates for all banks.
- BOA has the highest Uncategorized + Performance Issues.
- CBE struggles most with Transaction Reliability.
- Dashen faces recurring UI/Usability issues.

#### C. Average Sentiment Score per Bank
Using BERT sentiment scores:
- Dashen → 0.41 (Most positive)
- CBE → 0.28
- BOA → -0.13 (Most negative)
Interpretation: BOA customers express the most dissatisfaction.

#### D. Word & Bigram Frequency
Using unigrams and bigrams from the processed text:
- Frequent positive terms: good, best, nice, super, amazing
- Frequent negative terms: doesn’t work, slow, not working, developer options
- Bigrams show app-specific issues (e.g., “mobile banking”, “doesn’t work”, “super app”).

#### E. Theme Examples
Each theme was backed by real review excerpts, e.g.:
- Account Access Issues: “asks me to disable developer options…”
- Performance Issues: “most of the time it is not working properly”
- UI Issues: “not user-friendly at all…”
These enrich the quantitative insights with real user voice.

### 2. Drivers & Pain Points
#### Commercial Bank of Ethiopia (CBE)
Drivers (Strengths):
- Many reviews highlight reliability: “very good”, “excellent service”.
- Smooth transaction experience when the app works properly.

Pain Points:
- More complaints about transaction delays than other banks.
- Occasional login or verification-related issues.

Recommendations:
- Optimize the transaction pipeline to reduce peak-time delays.
- Add clearer user feedback when a transaction is pending/failing.

#### Bank of Abyssinia (BOA)
Drivers (Strengths):
- Positive reviews appreciate BOA’s clean design and fast flow when it works.
- Users like recent updates improving navigation.

Pain Points:
- Highest negative sentiment overall.
- Most performance complaints: “doesn’t work”, “crashed again”, “not working properly”.
- Login failures and verification issues appear frequently.

Recommendations:
- Prioritize app stability — reduce crashes through crash analytics.
- Redesign login/system checks to eliminate false failures.
- Expand technical support within the app (live chat, help center).

#### Dashen Bank
Drivers (Strengths):
- Highest positive sentiment across all banks.
- Frequent praise for speed: “fast and easy to use”.
- Strong UX appreciation: “super app”, “everything I need in one place”.

Pain Points:
- UI and user-flow issues during specific tasks.
- Some users report forced settings changes (e.g., developer options warnings).

Recommendations:
- Improve error messaging when permissions/settings are required.
- Introduce guided tutorials for first-time users inside the app.

### 3. Visualizations

Task 4 includes 5 core visualizations:
- Sentiment distribution per bank
- Theme distribution per bank
- Sentiment score comparison
- Top keywords (unigrams/bigrams)
- Word clouds (optional)

All plots are:
- Clearly labeled
- Color-coded
- Interpreted inside the notebook

Notebook:
`notebooks/insights_and_visuals.ipynb`

### 4. Ethical Considerations

A short ethics note was added, acknowledging potential biases:
- App reviews tend to be emotionally polarized (5-star or 1-star spikes).
- Negative sentiment may be exaggerated due to frustration bias.
- Reviews do not represent users who are not active on the Play Store.
- Some issues (e.g., network connectivity) may not be app-related.

5. How the Code Works
Notebook: `insights_and_visuals.ipynb`

The notebook performs:
- Loading enriched dataset (sentiment + themes)
- Data merging & cleaning
- Visualizations (Matplotlib / Seaborn)
- Insights per bank
- Top keywords extraction
- Final recommendations

Required files:
```bash
data/processed/thematic_results.csv
data/processed/reviews_processed.csv
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
│   ├── reviews_processed.csv
│   └── thematic_results.csv
│
├── scripts/
│ ├── scraper.py
│ ├── insert_reviews.py
│ ├── preprocessing.py
│ ├── __init__.py
│ ├── sentiment_analysis.py      
│ ├── thematic_analysis.py 
│ └── README.md
│
├── notebooks/
│   ├── __init__.py
│   ├── README.md
│   ├── insert_bank_reviews.ipynb
│   ├── insights_and_visuals.ipynb    
│   ├── preprocessing_EDA.ipynb
│   ├── sentiment_EDA.ipynb    
│   └── thematic_analysis.ipynb
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
├── requirements.txt
└── schema.sql
```
