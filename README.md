

```markdown
# Market Sentiment Bitcoin News Aggregator

It uses multiple language models from Amazon Bedrock to gather diverse opinions (the **Hexen Round Table**) and stores results in a PostgreSQL database.
---

## ✨ Features

- Periodic fetching and analysis of market news headlines from www.forexlive.com.
- Multiple models (Llama, Mistral, Sonnet) for sentiment assessment.
- Results stored for later review and analysis.
- Django frontend to display and manage collected insights.
- I display only the last 24 hours of data. A green indicator means the news is not impacting Bitcoin, while a red indicator shows it is impacting Bitcoin.

![alt text](sample_screenshot.png)
---

## 🧠 Prompt Used for Evaluation

Before any news headline is analyzed, the following prompt is sent to each model:

```

Please answer with “Yes” or “No” only. Do not provide any analysis or explanation.

Question:
Is the following statement a red flag indicating that investors should temporarily sell Bitcoin until the downtrend ends, and then buy again?

Statement:

```

---

## 🗂️ Project Structure Overview

```

Django\_Spielplatz/
├── Market\_Sentiment/                 # Python module for sentiment analysis and ingestion
│   ├── Database\_Engine.py            # Database handling (PostgreSQL insertions)
│   ├── Get\_Latest\_Headlines\_Forexlive.py  # Web scraping ForexLive headlines
│   ├── Hexen\_Round\_Table.py          # Orchestrates model-based sentiment voting
│   └── LLM\_Judging.py                # Interfaces with Amazon Bedrock LLMs
├── Weisse\_Eule/                      # Django project
│   ├── accounts/                     # User authentication (login, registration)
│   ├── trade\_augur/                  # Display sentiment-annotated headlines
│   └── Weisse\_Eule/                  # Core Django settings
├── main.py                           # Background script to run sentiment cycles
├── manage.py                         # Django CLI entry point
└── .Django\_Spielplatz.code-workspace # VS Code workspace configuration
└──config\config.ini

````

---

## ⚙️ How It Works

1. **main.py** runs in the background:
   - Periodically fetches ForexLive headlines.
   - Calls `HexenRoundTable` to get LLM assessments.
   - Stores results in PostgreSQL via `DatabaseEngine`.

2. **Django frontend** (`Weisse_Eule` project):
   - Displays stored headlines with sentiment verdicts.
   - Provides user login and management.

3. **Market_Sentiment** acts as the data ingestion and machine learning layer.

---

## 🐍 Technology Stack

### Backend
- Python 3.x
- Django (web framework)
- SQLAlchemy (database ORM)

### Database
- PostgreSQL (AWS RDS)

### Cloud AI Services
- Amazon Bedrock (multiple LLMs)
- Boto3 SDK (Bedrock integration)

### Web Scraping
- Requests
- BeautifulSoup

### Frontend
- HTML5/CSS3 (Django templates)

### Developer Tools
- Visual Studio Code
- Python virtual environments

---

## 🛠️ Key Components Overview

### 1️⃣ `Database_Engine.py`
Handles storing results in PostgreSQL via SQLAlchemy.

- **`__init__`**: Initializes the connection to the RDS instance.
- **`load_to_database()`**: Inserts records into `trade_augur_news_healines`.

---

### 2️⃣ `Get_Latest_Headlines_Forexlive.py`
Fetches and parses recent ForexLive news headlines.

- Downloads and parses the webpage.
- Extracts article metadata and filters by publish time.
- Cleans HTML content.

---

### 3️⃣ `Hexen_Round_Table.py`
Coordinates multiple LLMs to reach a sentiment consensus.

- Fetches fresh headlines.
- Sends each headline to all configured models.
- Collects “Yes”/“No” opinions for storage.

---

### 4️⃣ `LLM_Judging.py`
Handles querying Amazon Bedrock LLMs.

- Locates the model ARN by partial name.
- Sends the prompt and retrieves the answer.

---

## 🚀 packages needed

Django>=4.0
sqlalchemy>=2.0
psycopg2-binary
boto3
requests
beautifulsoup4
````

**To connect to DB:**
Be sure to put your RDS database connections in config.ini

**To Run Django server:**

   ```bash
   python manage.py runserver
   ```

**To Start background sentiment collection:**

   ```bash
   python main.py
   ```

---

## ✍️ Author

Created by [Fady Mahrous](https://github.com/fadymahrous). Contributions welcome!

---

## ⚠️ Disclaimer

This project is a **technical demonstration** of development, automation, and data processing skills.  
It is **not intended for real-life trading or investment decisions**.  
Any use of this project or its outputs is entirely **at your own risk and responsibility**.  
The author assumes **no liability** for any losses or damages resulting from the use of this code.

```
