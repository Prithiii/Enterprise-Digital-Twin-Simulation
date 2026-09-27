from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Enterprise Digital Twin",
    page_icon="🏢",
    layout="wide"
)

# =====================================
# CONFIG
# =====================================

MODEL_DIR = Path(__file__).resolve().parent

FEATURES = [
    "Marketing_Budget",
    "Employee_Count",
    "Customer_Count",
    "Inventory_Level",
    "Warehouse_Capacity",
]

SCENARIO_FILE = MODEL_DIR / "scenario_history.csv"

# =====================================
# LOAD MODELS
# =====================================

try:

    revenue_model = joblib.load(
        MODEL_DIR / "revenue_model.pkl"
    )

    profit_model = joblib.load(
        MODEL_DIR / "profit_model.pkl"
    )

except Exception as exc:

    st.error(
        "Unable to load revenue_model.pkl or profit_model.pkl"
    )

    st.exception(exc)
    st.stop()

# =====================================
# TITLE
# =====================================

st.title("🏢 Enterprise Digital Twin")
st.caption(
    "Decision Intelligence Platform for Enterprise Scenario Simulation"
)

# =====================================
# SIDEBAR INPUTS
# =====================================

st.sidebar.header("Business Drivers")

marketing_budget = st.sidebar.slider(
    "Marketing Budget",
    20000,
    500000,
    100000
)

employee_count = st.sidebar.slider(
    "Employee Count",
    50,
    1000,
    150
)

customer_count = st.sidebar.slider(
    "Customer Count",
    1000,
    150000,
    25000
)

inventory_level = st.sidebar.slider(
    "Inventory Level",
    1000,
    100000,
    20000
)

warehouse_capacity = st.sidebar.slider(
    "Warehouse Capacity",
    5000,
    200000,
    50000
)

# =====================================
# RUN SIMULATION
# =====================================

if st.sidebar.button("Run Simulation"):

    values = {
        "Marketing_Budget": marketing_budget,
        "Employee_Count": employee_count,
        "Customer_Count": customer_count,
        "Inventory_Level": inventory_level,
        "Warehouse_Capacity": warehouse_capacity
    }

    inputs_df = pd.DataFrame(
        [values],
        columns=FEATURES
    )

    predicted_revenue = float(
        revenue_model.predict(inputs_df)[0]
    )

    predicted_profit = float(
        profit_model.predict(inputs_df)[0]
    )

    profit_margin = (
        predicted_profit
        /
        predicted_revenue
    ) * 100

    # =====================================
    # ENTERPRISE SCORE
    # =====================================

    baseline_revenue = 1000000

    growth = (
        (
            predicted_revenue
            - baseline_revenue
        )
        /
        baseline_revenue
    ) * 100

    enterprise_score = 0

    if profit_margin > 25:
        enterprise_score += 40

    if growth > 10:
        enterprise_score += 30

    if predicted_revenue > 1000000:
        enterprise_score += 30

    # =====================================
    # RISK
    # =====================================

    if profit_margin < 10:
        risk_level = "🔴 High"

    elif profit_margin < 20:
        risk_level = "🟡 Medium"

    else:
        risk_level = "🟢 Low"

    # =====================================
    # KPI SECTION
    # =====================================

    st.subheader("Executive Summary")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Revenue",
        f"${predicted_revenue:,.0f}"
    )

    col2.metric(
        "Profit",
        f"${predicted_profit:,.0f}"
    )

    col3.metric(
        "Margin %",
        f"{profit_margin:.2f}%"
    )

    col4.metric(
        "Growth %",
        f"{growth:.2f}%"
    )

    col5.metric(
        "Enterprise Score",
        f"{enterprise_score}/100"
    )

    st.metric(
        "Risk Level",
        risk_level
    )

    # =====================================
    # HEALTH STATUS
    # =====================================

    st.subheader("Enterprise Health")

    if profit_margin > 25:

        st.success(
            "Enterprise is operating efficiently."
        )

    elif profit_margin > 10:

        st.warning(
            "Enterprise is stable but can be optimized."
        )

    else:

        st.error(
            "Low profitability detected."
        )

    # =====================================
    # RECOMMENDATIONS
    # =====================================

    st.subheader(
        "Strategic Recommendations"
    )

    recommendations = []

    if marketing_budget < 50000:

        recommendations.append(
            "Increase marketing investment."
        )

    if employee_count < 100:

        recommendations.append(
            "Expand workforce capacity."
        )

    if profit_margin < 15:

        recommendations.append(
            "Reduce operational expenses."
        )

    if customer_count < 10000:

        recommendations.append(
            "Focus on customer acquisition."
        )

    if not recommendations:

        recommendations.append(
            "Current strategy appears healthy."
        )

    for rec in recommendations:

        st.write(
            "✅",
            rec
        )

    # =====================================
    # CURRENT VS FUTURE
    # =====================================

    current_revenue = 1000000
    current_profit = 200000

    comparison = pd.DataFrame(
        {
            "Current": [
                current_revenue,
                current_profit
            ],

            "Predicted": [
                predicted_revenue,
                predicted_profit
            ]
        },

        index=[
            "Revenue",
            "Profit"
        ]
    )

    st.subheader(
        "Current vs Future Enterprise State"
    )

    st.dataframe(
        comparison,
        use_container_width=True
    )

    # =====================================
    # REVENUE VS PROFIT
    # =====================================

    chart_df = pd.DataFrame(
        {
            "Metric": [
                "Revenue",
                "Profit"
            ],

            "Value": [
                predicted_revenue,
                predicted_profit
            ]
        }
    )

    col_a, col_b = st.columns(2)

    with col_a:

        fig_bar = px.bar(
            chart_df,
            x="Metric",
            y="Value",
            title="Revenue vs Profit"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col_b:

        fig_pie = px.pie(
            chart_df,
            names="Metric",
            values="Value",
            title="Revenue Distribution"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    # =====================================
    # FEATURE IMPORTANCE
    # =====================================

    st.subheader(
        "Business Driver Importance"
    )

    try:

        importance_df = pd.DataFrame({
            "Feature": FEATURES,
            "Importance":
            revenue_model.feature_importances_
        })

        st.dataframe(
            importance_df.sort_values(
                "Importance",
                ascending=False
            ),
            use_container_width=True
        )

        st.bar_chart(
            importance_df.set_index(
                "Feature"
            )
        )

    except Exception:

        st.info(
            "Feature importance unavailable."
        )

    # =====================================
    # SAVE SCENARIO
    # =====================================

    scenario_df = pd.DataFrame(
        [{
            **values,
            "Revenue": predicted_revenue,
            "Profit": predicted_profit,
            "Profit_Margin": profit_margin,
            "Growth": growth
        }]
    )

    if SCENARIO_FILE.exists():

        scenario_df.to_csv(
            SCENARIO_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        scenario_df.to_csv(
            SCENARIO_FILE,
            index=False
        )

    # =====================================
    # SIMULATION DETAILS
    # =====================================

    st.subheader(
        "Simulation Details"
    )

    st.dataframe(
        scenario_df,
        use_container_width=True
    )

# =====================================
# HISTORY
# =====================================

if SCENARIO_FILE.exists():

    st.subheader(
        "Previous Simulations"
    )

    history = pd.read_csv(
        SCENARIO_FILE
    )

    st.dataframe(
        history.tail(10),
        use_container_width=True
    )