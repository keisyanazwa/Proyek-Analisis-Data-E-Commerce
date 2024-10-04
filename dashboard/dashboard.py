import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

st.title("E-Commerce Public Dataset")

# Load dataset
order_items_df = pd.read_csv('olist_order_items_dataset.csv')
products_df = pd.read_csv('olist_products_dataset.csv')
order_items_products_df = pd.merge(
    left=order_items_df,
    right=products_df,
    how="left",
    left_on="product_id",
    right_on="product_id"
)

order_items_products_df.head()
order_items_products_df.groupby(by="product_category_name").agg({
    "product_id": "nunique",
    "price": ["min", "max"]
})
order_items_products = order_items_products_df.groupby(by="product_category_name").agg(
    num_of_order=('product_id', 'count'), sum_order_value=('price', 'sum')
).reset_index()
order_items_products.sort_values(by=['num_of_order', 'sum_order_value'], ascending=False).head(10)

# Create tabs
tab1, tab2 = st.tabs(["Pertanyaan 1", "Pertanyaan 2"])

# Tab 1: Most and least ordered products
with tab1:
    st.subheader("Produk apa saja kah yang paling banyak dipesan dan produk apa saja kah yang paling sedikit dipesan?")
    
    # Create a separate figure for tab 1
    fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    
    colors = ["#3187d4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4", "#b3bcc4"]
    
    # Plot for most ordered products
    sns.barplot(
        x="num_of_order",
        y="product_category_name",
        data=order_items_products.sort_values(by=['num_of_order', 'sum_order_value'], ascending=False).head(10),
        palette=colors,
        ax=ax1[0]
    )
    ax1[0].set_ylabel(None)
    ax1[0].set_xlabel(None)
    ax1[0].set_title("Paling Banyak Dipesan", loc="center", fontsize=15)
    ax1[0].tick_params(axis='y', labelsize=12)
    
    # Plot for least ordered products
    sns.barplot(
        x="num_of_order",
        y="product_category_name",
        data=order_items_products.sort_values(by=['num_of_order', 'sum_order_value'], ascending=True).head(10),
        palette=colors,
        ax=ax1[1]  # Make sure to use ax1[1] for the second plot
    )
    ax1[1].set_ylabel(None)
    ax1[1].set_xlabel(None)
    ax1[1].invert_xaxis()
    ax1[1].yaxis.set_label_position("right")
    ax1[1].yaxis.tick_right()
    ax1[1].set_title("Paling Sedikit Dipesan", loc="center", fontsize=15)
    ax1[1].tick_params(axis='y', labelsize=12)
    
    plt.suptitle("Kategori Produk yang Paling Banyak dan Paling Sedikit Dipesan", fontsize=20)
    st.pyplot(fig1)

# Tab 2: Sellers distribution by city and state
sellers_df = pd.read_csv('olist_sellers_dataset.csv')
sellers_in_cities = sellers_df.groupby(by="seller_city").seller_id.nunique().sort_values(ascending=False).reset_index()
sellers_in_states = sellers_df.groupby(by="seller_state").seller_id.nunique().sort_values(ascending=False).reset_index()

with tab2:
    st.subheader("Bagaimana penyebaran dari penjual berdasarkan kota dan negara bagian?")
    
    # Create a separate figure for tab 2
    fig2, ax2 = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    
    # Plot for sellers by city
    sns.barplot(x="seller_city", y="seller_id", data=sellers_in_cities.head(10), palette=colors, ax=ax2[0])
    ax2[0].set_ylabel(None)
    ax2[0].set_xlabel(None)
    ax2[0].tick_params(axis='x', labelrotation=45)
    ax2[0].set_title("Berdasarkan Kota", loc="center", fontsize=18)
    ax2[0].tick_params(axis='y', labelsize=15)
    
    # Plot for sellers by state
    sns.barplot(x="seller_state", y="seller_id", data=sellers_in_states.head(10), palette=colors, ax=ax2[1])
    ax2[1].set_ylabel(None)
    ax2[1].set_xlabel(None)
    ax2[1].tick_params(axis='x', labelrotation=45)
    ax2[1].set_title("Berdasarkan Negara Bagian", loc="center", fontsize=18)
    ax2[1].tick_params(axis='y', labelsize=15)
    
    plt.suptitle("Persebaran Jumlah Penjual Berdasarkan Kota dan Negara Bagian", fontsize=20)
    st.pyplot(fig2)

   