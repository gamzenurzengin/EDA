import streamlit as st

import bq


@st.cache
def minmax():
    return bq.run_sql("""
    select max(price) - min(price) rng from `analytics-bootcamp-323516.week2.mercari`
    """)['rng'][0]


@st.cache
def mad():
    return bq.run_sql("""
    select avg(abs(price - median)) mad from
(SELECT
  price, percentile_cont(price,
    0.5) OVER() median
FROM
  `analytics-bootcamp-323516.week2.mercari`)
    """)['mad'][0]


@st.cache
def var():
    return bq.run_sql("""
select VAR_POP(fare_amount) var_pop,  VAR_SAMP(fare_amount) var_sample
        from `analytics-bootcamp-323516.week2.mercari`;
    """)


@st.cache
def sd():
    return bq.run_sql("""
        select STDDEV_POP(fare_amount) sd_pop,  STDDEV_SAMP(fare_amount) sd_sample
        from `analytics-bootcamp-323516.week2.mercari`
    """)


@st.cache
def iqr():
    return bq.run_sql("""
    select q[offset(25)] q25, q[offset(75)]       q75 from
(select approx_quantiles(price, 100) q from `analytics-bootcamp-323516.week2.mercari` )
    """).assign(iqr=lambda x: x.q75 - x.q25)

@st.cache
def iqr2():
    return bq.run_sql("""
   select q[offset(1)] q25, q[offset(3)]       q75 from
(select approx_quantiles(price, 4) q from `analytics-bootcamp-323516.week2.mercari` )
    """).assign(iqr=lambda x: x.q75 - x.q25)


def render():
    st.title("Estimates of Variability")

    st.write(minmax())

    st.header("Mean Absolute Deviation (L1/Manhattan Norm)")

    st.write(mad())

    st.header("Variance (MSE)")

    st.write(var())

    st.header("Standard Deviation")

    st.write(sd())

    st.info("""
    `n` vs `n-1` (degrees of freedom) at denominator defines biased(population)/unbiased(sample) estimation.
    """)

    st.header("Inter Quartile Range (IQR)")
    df = iqr()

    st.dataframe(df)
    st.dataframe(iqr2())