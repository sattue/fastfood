import io
import random
import textwrap

import pandas as pd
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Online Food Delivery – Survey Dashboard",
    page_icon="🍔",
    layout="wide",
)

CSV_PATH = "onlinedeliverydata.csv"

LIKERT = ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]
AGREE_SET = {"Strongly agree", "Agree"}

FACTOR_COLS = [
    "Ease and convenient",
    "Time saving",
    "More Offers and Discount",
    "Good Food quality",
    "Easy Payment option",
]

MEDIUM_COL = "Medium (P1)"
MEAL_COL = "Meal(P1)"


def _synthetic_fallback(n: int = 100) -> pd.DataFrame:
    rng = random.Random(42)
    genders = ["Male", "Female"]
    occupations = ["Student", "Employee", "Self Employeed", "House wife"]
    incomes = ["No Income", "Below Rs.10000", "10001 to 25000", "25001 to 50000", "More than 50000"]
    edu = ["Graduate", "Post Graduate", "Ph.D", "School"]
    mediums_raw = ["Food delivery apps", "Food delivery apps, Web browser", "Food delivery apps, Direct call", "Web browser", "Direct call"]
    meals_raw = ["Breakfast", "Lunch", "Dinner", "Snacks", "Breakfast, Lunch", "Lunch, Snacks"]
    prefs_raw = ["Non Veg foods (Lunch / Dinner)", "Veg foods (Breakfast / Lunch / Dinner)", "Bakery items (snacks)", "Beverages (Cold/hot)"]
    order_times = ["Anytime (Mon-Sun)", "Weekdays (Mon-Fri)", "Weekend (Sat & Sun)", "Night (8PM-12PM)"]
    wait_times = ["30 minutes", "45 minutes", "60 minutes", "More than an hour"]
    rows = []
    for _ in range(n):
        row = {
            "Age": rng.randint(18, 55), "Gender": rng.choice(genders), "Marital Status": rng.choice(["Single", "Married"]),
            "Occupation": rng.choice(occupations), "Monthly Income": rng.choice(incomes),
            "Educational Qualifications": rng.choice(edu), "Family size": rng.randint(1, 6),
            "latitude": 12.9 + rng.random() * 0.2, "longitude": 77.5 + rng.random() * 0.3,
            "Pin code": rng.randint(560001, 560100), MEDIUM_COL: rng.choice(mediums_raw),
            "Medium (P2)": rng.choice(mediums_raw), MEAL_COL: rng.choice(meals_raw), "Meal(P2)": rng.choice(meals_raw),
            "Perference(P1)": rng.choice(prefs_raw), "Perference(P2)": rng.choice(prefs_raw),
        }
        for col in ["Ease and convenient", "Time saving", "More restaurant choices", "Easy Payment option",
                     "More Offers and Discount", "Good Food quality", "Good Tracking system", "Self Cooking",
                     "Health Concern", "Late Delivery", "Poor Hygiene", "Bad past experience", "Unavailability",
                     "Unaffordable", "Long delivery time", "Delay of delivery person getting assigned",
                     "Delay of delivery person picking up food", "Wrong order delivered", "Missing item",
                     "Order placed by mistake"]:
            row[col] = rng.choice(LIKERT)
        row["Influence of time"] = rng.choice(["Yes", "No"])
        row["Order Time"] = rng.choice(order_times)
        row["Maximum wait time"] = rng.choice(wait_times)
        row["Output"] = rng.choice(["Yes", "No"])
        row["Reviews"] = ""
        rows.append(row)
    return pd.DataFrame(rows)


@st.cache_data(show_spinner="Loading survey data…")
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except FileNotFoundError:
        st.warning("⚠️ `onlinedeliverydata.csv` not found – using synthetic fallback data.", icon="⚠️")
        return _synthetic_fallback()


def _first_token(series: pd.Series) -> pd.Series:
    return series.astype(str).str.split(",").str[0].str.strip()


def _pct_agree(series: pd.Series) -> float:
    total = len(series.dropna())
    if total == 0:
        return 0.0
    agreed = series.isin(AGREE_SET).sum()
    return round(agreed / total * 100, 1)


def _medium_label(raw: str) -> str:
    first = str(raw).split(",")[0].strip()
    mapping = {"Food delivery apps": "Delivery App", "Web browser": "Web Browser", "Direct call": "Direct Call"}
    return mapping.get(first, first)


def main() -> None:
    df_raw = load_data()

    with st.sidebar:
        st.title("🍔 Food Delivery Survey")
        st.markdown("---")
        all_genders = sorted(df_raw["Gender"].dropna().unique().tolist())
        sel_gender = st.multiselect("Gender", options=all_genders, default=all_genders)
        all_occupations = sorted(df_raw["Occupation"].dropna().unique().tolist())
        sel_occupation = st.multiselect("Occupation", options=all_occupations, default=all_occupations)
        st.markdown("---")
        st.caption("Filters apply to all charts and KPIs.")

    mask = df_raw["Gender"].isin(sel_gender) & df_raw["Occupation"].isin(sel_occupation)
    df = df_raw[mask].copy()

    st.title("Online Food Delivery – Survey Dashboard")
    st.caption(f"Showing **{len(df):,}** of **{len(df_raw):,}** respondents after applying sidebar filters.")

    k1, k2, k3, k4 = st.columns(4)
    total = len(df)
    avg_age = round(df["Age"].mean(), 1) if total else 0
    medium_primary = _first_token(df[MEDIUM_COL])
    pct_app = round((medium_primary == "Food delivery apps").sum() / max(total, 1) * 100, 1)
    meal_primary = _first_token(df[MEAL_COL])
    top_meal = meal_primary.mode()[0] if total else "—"
    top_meal_short = textwrap.shorten(top_meal, width=22, placeholder="…")

    k1.metric("👥 Total Respondents", f"{total:,}")
    k2.metric("🎂 Average Age", f"{avg_age} yrs")
    k3.metric("📱 Use Delivery Apps", f"{pct_app}%")
    k4.metric("🍽️ Top Meal Preference", top_meal_short)

    st.markdown("---")
    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.subheader("Respondents by Occupation")
        occ_counts = df["Occupation"].value_counts().reset_index()
        occ_counts.columns = ["Occupation", "Count"]
        fig_occ = px.bar(occ_counts, x="Occupation", y="Count", color="Occupation",
                          color_discrete_sequence=px.colors.qualitative.Pastel, text="Count")
        fig_occ.update_traces(textposition="outside", showlegend=False)
        fig_occ.update_layout(margin=dict(t=20, b=10), xaxis_title=None, yaxis_title="Respondents", plot_bgcolor="white")
        st.plotly_chart(fig_occ, use_container_width=True)

    with col_right:
        st.subheader("Ordering Medium (Primary)")
        medium_mapped = df[MEDIUM_COL].map(_medium_label)
        med_counts = medium_mapped.value_counts().reset_index()
        med_counts.columns = ["Medium", "Count"]
        fig_med = px.pie(med_counts, names="Medium", values="Count", hole=0.55,
                          color_discrete_sequence=px.colors.qualitative.Set2)
        fig_med.update_traces(textposition="outside", textinfo="percent+label")
        fig_med.update_layout(margin=dict(t=20, b=10), showlegend=False)
        st.plotly_chart(fig_med, use_container_width=True)

    st.subheader("Top Purchase-Driving Factors (% Agree or Strongly Agree)")
    available_factors = [c for c in FACTOR_COLS if c in df.columns]
    factor_pcts = [{"Factor": col, "% Agree / Strongly Agree": _pct_agree(df[col])} for col in available_factors]
    factor_df = pd.DataFrame(factor_pcts).sort_values("% Agree / Strongly Agree", ascending=True)
    fig_fac = px.bar(factor_df, x="% Agree / Strongly Agree", y="Factor", orientation="h",
                      color="% Agree / Strongly Agree", color_continuous_scale="Blues", text="% Agree / Strongly Agree")
    fig_fac.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_fac.update_layout(margin=dict(t=20, b=10, l=10), xaxis=dict(range=[0, 110], title="% Respondents"),
                           yaxis_title=None, coloraxis_showscale=False, plot_bgcolor="white", height=320)
    st.plotly_chart(fig_fac, use_container_width=True)

    st.markdown("---")
    with st.expander("🔍 Raw Data Preview", expanded=False):
        st.dataframe(df, use_container_width=True, height=350)
        csv_bytes = df.to_csv(index=False).encode()
        st.download_button(label="⬇️ Download filtered data as CSV", data=csv_bytes,
                            file_name="filtered_survey_data.csv", mime="text/csv")


if __name__ == "__main__":
    main()
