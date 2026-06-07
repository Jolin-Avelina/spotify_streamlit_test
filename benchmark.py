import streamlit as st
from vega_datasets import data
from time import time
import pandas as pd


@st.cache
def load_data():
    return pd.concat((data.airports() for _ in range(100)))


@st.cache
def select_rows(dataset, nrows):
    return dataset.head(nrows)


@st.cache
def describe(dataset):
    return dataset.describe()


rows = st.slider("Rows", min_value=100, max_value=3300 * 100, step=10000)

start_uncached = time()
dataset_uncached = pd.concat((data.airports() for _ in range(100)))
load_uncached = time()
dataset_sample_uncached = dataset_uncached.head(rows)
select_uncached = time()
describe_uncached_dataset = dataset_sample_uncached.describe()
finish_uncached = time()
benchmark_uncached = (
    f"Cached. Total: {finish_uncached - start_uncached:.2f}s"
    f" Load: {load_uncached - start_uncached:.2f}"
    f" Select: {select_uncached - load_uncached:.2f}"
    f" Describe: {finish_uncached - select_uncached:.2f}"
)

st.text(benchmark_uncached)
st.write(describe_uncached_dataset)

start_cached = time()
dataset_cached = load_data()
load_cached = time()
dataset_sample_cached = select_rows(dataset_cached, rows)
select_cached = time()
describe_cached_dataset = describe(dataset_sample_cached)
finish_cached = time()

benchmark_cached = (
    f"Cached. Total: {finish_cached - start_cached:.2f}s"
    f" Load: {load_cached - start_cached:.2f}"
    f" Select: {select_cached - load_cached:.2f}"
    f" Describe: {finish_cached - select_cached:.2f}"
)
st.text(benchmark_cached)
st.write(describe_cached_dataset)
