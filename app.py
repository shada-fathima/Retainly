from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Retainly",
    page_icon=None,
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"


@st.cache_data
def load_data():
    customers = pd.read_csv(
        DATA_DIR / "customer_rfm.csv",
        dtype={"Customer ID": "string", "RFM_code": "string"},
        parse_dates=["last_purchase"],
    )

    segments = pd.read_csv(
        DATA_DIR / "segment_summary.csv",
        index_col=0,
    )

    retention = pd.read_csv(
        DATA_DIR / "retention_summary.csv"
    )

    return customers, segments, retention


customers, segments, retention = load_data()

st.title("Retainly")
st.caption("Customer segmentation and repeat-purchase analytics")

st.info(
    "Historical analysis: December 2009–December 2011. "
    "RFM snapshot: 10 December 2011. "
    "Sales value excludes refunds; segment labels are "
    "rule-based, not churn predictions."
)

col1, col2, col3 = st.columns(3)

col1.metric("Paying customers", f"{len(customers):,}")

col2.metric(
    "Positive-sales value",
    f"{customers['monetary_value'].sum():,.2f}",
)

col3.metric(
    "At-risk valuable customers",
    f"{customers['segment'].eq('At-risk valuable customers').sum():,}",
)

tab1, tab2, tab3 = st.tabs([
    "Segment overview",
    "Customer explorer",
    "Repeat purchasing",
])

with tab1:
    st.subheader("Customer share versus positive-sales value share")

    chart_data = segments[[
        "customer_share_pct",
        "sales_share_pct",
    ]].rename(columns={
        "customer_share_pct": "Customer share (%)",
        "sales_share_pct": "Positive-sales value share (%)",
    })

    st.bar_chart(chart_data)
    st.dataframe(segments.round(2), use_container_width=True)

with tab2:
    selected_segments = st.multiselect(
        "Choose customer segments",
        options=sorted(customers["segment"].unique()),
        default=sorted(customers["segment"].unique()),
    )

    filtered = customers.loc[
        customers["segment"].isin(selected_segments)
    ].copy()

    st.write(f"Showing {len(filtered):,} customers")

    st.dataframe(
        filtered.sort_values(
            "monetary_value",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="Download selected customers",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="retail_customer_segments.csv",
        mime="text/csv",
    )

with tab3:
    st.subheader("Paid repeat-purchase rates")

    st.dataframe(
        retention.round(2),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Each rate measures purchasing in one specific follow-up "
        "calendar month, not cumulative repeat purchasing. "
        "Eligible cohorts differ across follow-up months. "
        "The December 2009 boundary cohort and incomplete "
        "December 2011 period are excluded."
    )

    heatmap = (
        BASE_DIR
        / "reports"
        / "figures"
        / "monthly_cohort_retention.png"
    )

    if heatmap.exists():
        st.image(str(heatmap))