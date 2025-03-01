import streamlit as st
import pandas as pd

# Backend Logic
def load_data(file_path):
    data = pd.read_csv(file_path)
    data['specific_category'] = data['category'].apply(lambda x: str(x).split('|')[-1] if pd.notnull(x) else 'Unknown')
    #data['discounted_price']=data['discounted_price'].str.replace('₹','')
    #data['discounted_price']=data['discounted_price'].str.replace(',','')
   # data['discounted_price']=data['discounted_price'].astype('float')
    data['discounted_price'] = pd.to_numeric(data['discounted_price'], errors='coerce')
    data['rating'] = pd.to_numeric(data['rating'], errors='coerce')
    return data

def filter_by_category(data, category):
    return data[data['specific_category'] == category]

def get_top_products(data, top_n=5):
    sorted_data = data.sort_values(by=['rating', 'discounted_price'], ascending=[False, True])
    return sorted_data.head(top_n)

def fetch_product_details(data):
    product_details = []
    for _, row in data.iterrows():
        details = {
            "product_name": row['product_name'],
            "price": row['discounted_price'],
            "rating": row['rating'],
            "review": row['review_content'][:150] if isinstance(row['review_content'], str) else "No review available",
            "sentiment":row['sentiment'],
            "image_url": row.get('img-link','No image available'),
            "product_url":row.get('product_link',"No link avalable"),
        }
        product_details.append(details)
    return product_details

# Load the Dataset
file_path = 'amazon_new.csv'  # Update with the correct file path
data = load_data(file_path)

# Streamlit UI
st.title("Personalized Shopping Experience")

# Category Selection
categories = sorted(data['specific_category'].unique())
selected_category = st.selectbox("Select a Product Category", categories)

# Filter and Display Recommendations
if st.button("Show Recommendations"):
    filtered_data = filter_by_category(data, selected_category)
    top_products = get_top_products(filtered_data)
    recommendations = fetch_product_details(top_products)
    
    st.subheader(f"Top Products in {selected_category}")
    if recommendations:
        for product in recommendations:
            st.write(f"**Product Name:** {product['product_name']}")
            st.write(f"**Price:** ₹{product['price']}")
            st.write(f"**Rating:** {product['rating']}")
            st.write(f"**Review Snippet:** {product['review']}")
            st.write(f"**Customer's Overall Review:** {product['sentiment']}")

            if product['image_url'] != 'No image available':
                st.image(product['image_url'], width=200)  # Adjust width as needed
            
            if product['product_url'] != 'No link available':
                st.markdown(f"[View Product]({product['product_url']})")
            st.markdown("---")
    else:
        st.write("No products found in this category.")

# Footer
st.sidebar.info("Enhancing Personalized Shopping Experience with AI.")
