# Online Food Delivery — Survey Dashboard

**Author:** Sataraj
**Built with:** IBM Bob (AI-augmented IDE) + Streamlit
**Program:** AICTE & IBM SkillsBuild 6-Week Academic Internship in Data Analytics with AI — IBM Bob / Prompt Engineering session

## Project Description

An interactive Streamlit dashboard exploring a 388-respondent survey on online food delivery habits and preferences (Bangalore region). The dashboard was generated using IBM Bob's AI IDE from a single, fully-specified prompt (holistic prompt architecture, rather than many small back-and-forth prompts), then run and verified locally.

The dashboard shows respondent demographics, how people prefer to order (app, web, direct call), what meal they most commonly order, and which factors (convenience, time saving, discounts, food quality, easy payment) most influence their decision to use food delivery.

## Dataset

- **File:** `onlinedeliverydata.csv`
- **Source:** Public Kaggle dataset — "Online Food Delivery Preferences (Bangalore Region)"
- **Size:** 388 survey responses, 55 columns covering demographics, ordering medium/preferences, and Likert-scale ratings of purchase-driving and purchase-blocking factors.

## Key Findings (from the dashboard, unfiltered)

- **388** total respondents, average age **24.6**
- **92.3%** primarily order through food delivery apps (vs. web browser, direct call, or walk-in)
- **Snacks** is the most common top meal preference (124 respondents), followed by Lunch (120), Dinner (91), Breakfast (53)
- Occupation breakdown: Student (207), Employee (118), Self-Employed (54), House wife (9)
- Top purchase-driving factors by % Agree/Strongly Agree: Ease and convenient (77.8%), Time saving (66.5%), Easy Payment option (60.8%), More Offers and Discount (58.2%), Good Food quality (53.9%)

## Technologies Used

- Python 3.14
- pandas — data loading and aggregation
- Plotly Express — interactive bar, donut, and horizontal bar charts
- Streamlit — dashboard framework and UI
- IBM Bob — AI IDE used to generate the initial `app.py` from a single structured prompt

## Setup & Run Instructions

1. Make sure Python 3.10+ is installed and on PATH (`python --version` to check).
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Place `onlinedeliverydata.csv` in the same folder as `app.py`. (If the CSV is missing, the app automatically falls back to generated synthetic data with the same schema, so it still runs.)
4. Run the app:
   ```bash
   python -m streamlit run app.py
   ```
5. It opens automatically in your browser at `http://localhost:8501`. Use the sidebar to filter by Gender and Occupation — all KPIs and charts update live.

## Files in This Submission

| File | Description |
|---|---|
| `app.py` | Streamlit dashboard source code |
| `requirements.txt` | Python dependencies |
| `onlinedeliverydata.csv` | Source dataset |
| `Sataraj_FoodDeliveryDashboard_Report.docx` | Written project report |
| `README.md` | This file |
