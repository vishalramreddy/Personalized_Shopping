import streamlit as st
import pandas as pd
from PIL import Image

# Ensure set_page_config is the first Streamlit command
st.set_page_config(page_title="Personalized Shopping", layout="wide")

# Load Data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['specific_category'] = data['category'].apply(lambda x: str(x).split('|')[-1] if pd.notnull(x) else 'Unknown')
    data['discounted_price'] = pd.to_numeric(data['discounted_price'], errors='coerce')
    data['rating'] = pd.to_numeric(data['rating'], errors='coerce')
    return data

# Filtering & Sorting
def filter_by_category(data, category):
    return data[data['specific_category'] == category]

def get_top_products(data, top_n=5, sort_by='rating'):
    if sort_by == 'price':
        return data.nsmallest(top_n, 'discounted_price')
    return data.nlargest(top_n, 'rating')

def fetch_product_details(data):
    product_details = []
    for _, row in data.iterrows():
        details = {
            "product_name": row['product_name'],
            "price": row['discounted_price'],
            "rating": row['rating'],
            "review": row['review_content'][:150] if isinstance(row['review_content'], str) else "No review available",
            "sentiment": row['sentiment'],
            "image_url": row.get('img-link', 'No image available'),
            "product_url": row.get('product_link', "No link available"),
        }
        product_details.append(details)
    return product_details

# Load Data
file_path = 'Final_Year_Project_Codes/amazon_new.csv'
data = load_data(file_path)



# UI
#st.set_page_config(page_title="Personalized Shopping", layout="wide")
st.title("🛍️ Personalized Shopping Experience")

# Sidebar Filters
categories = sorted(data['specific_category'].unique())
selected_category = st.sidebar.selectbox("Select a Category", categories)
sort_by = st.sidebar.radio("Sort by", ["rating", "price"], index=0)
max_price = st.sidebar.slider("Max Price", float(data['discounted_price'].min()), float(data['discounted_price'].max()), float(data['discounted_price'].max()))

# Show Recommendations
if st.sidebar.button("Show Recommendations"):
    filtered_data = filter_by_category(data, selected_category)
    filtered_data = filtered_data[filtered_data['discounted_price'] <= max_price]
    top_products = get_top_products(filtered_data, sort_by=sort_by)
    recommendations = fetch_product_details(top_products)
    
    st.subheader(f"Top {len(recommendations)} Products in {selected_category}")
    
    # Display in columns
    cols = st.columns(2)
    
    for i, product in enumerate(recommendations):
        with cols[i % 2]:
            st.markdown(f"**{product['product_name']}**")
            #st.image(product['image_url'], width=200) if product['image_url'] != 'No image available' #else st.text("No Image")
            st.write(f"**Price:** ₹{product['price']}")
            st.write(f"**Rating:** {'⭐' * int(product['rating']) if not pd.isna(product['rating']) else 'No rating'}")
            st.write(f"**Review:** {product['review']}")
            st.write(f"**Sentiment:** {product['sentiment']}")
            st.markdown(f"[🔗 View Product]({product['product_url']})")
            st.markdown("---")

# Footer
st.sidebar.info("🚀 Enhancing Personalized Shopping Experience with AI.")
