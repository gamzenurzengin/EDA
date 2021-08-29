import streamlit as st
import bq


@st.cache
def mean():
    return bq.run_sql("select avg(price) mean from `analytics-bootcamp-323516.week2.mercari`")['mean'][0]


@st.cache
def weighted_mean():
    return bq.run_sql("""
    SELECT
  SUM(w*price)/SUM(w) AS wmean
FROM (
  SELECT
    EXP(-DATE_DIFF(last_pickup_datetime, pickup_datetime, DAY)) w,
    DATE_DIFF(last_pickup_datetime, pickup_datetime, DAY) delta,
    price
  FROM (
    SELECT
      pickup_datetime,
      MAX(pickup_datetime ) OVER() last_pickup_datetime,
      price
    FROM
      `analytics-bootcamp-323516.week2.mercari` ) )
    """)['wmean'][0]


@st.cache
def truncated_mean(p):
    return bq.run_sql(f"""
    select avg(price) tmean from 
(select price, cume_dist() over(order by price) p 
from `analytics-bootcamp-323516.week2.mercari` )
where p between {p} and {1 - p}
    """)['tmean'][0]


@st.cache
def median():
    return bq.run_sql(
        "select  percentile_cont(price, 0.5) over() median from `analytics-bootcamp-323516.week2.mercari` limit 1")[
        'median'][0]


def render():
    st.title("Estimates of Location")

    st.header("Average/Mean")

    st.write(mean())

    st.markdown("""
    * Center of Mass
    * Not a robust estimate for central tendency
    """)

    st.header("Median/50th Percentile")
    st.write(median())

    st.header("Trimmed/Truncated Mean")
    tmean = truncated_mean(0.1)
    st.write(tmean)

    st.header("Weigted Mean/Average")

    wmean = weighted_mean()
    st.write(wmean)