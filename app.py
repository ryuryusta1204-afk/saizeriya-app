import streamlit as st

# 1. Menu Database with Image URLs
# Replace the placeholder URLs with your actual image links or local file paths (e.g., "images/doria.jpg")
MENU = {
    "BR01": {
        "name": "Milano-fu Doria (ミラノ風ドリア)", 
        "price": 300,
        "image": "https://unsplash.com" # Placeholder image
    },
    "AA01": {
        "name": "Popcorn Shrimp (ポップコーンシュリンプ)", 
        "price": 300,
        "image": "https://unsplash.com" # Placeholder image
    },
    "DG01": {
        "name": "Italian Gelato (イタリアンジェラート)", 
        "price": 250,
        "image": "https://unsplash.com" # Placeholder image
    },
}

st.title("🍕 Saizeriya Smart Order Slip with Photos")

# Initialize session state for the order
if "order_slip" not in st.session_state:
    st.session_state.order_slip = []

# --- SECTION 1: VISUAL MENU CATALOG ---
st.subheader("📖 Menu Catalog")
st.write("Click 'Add to Slip' directly under the photo:")

# Create a clean layout grid using columns
cols = st.columns(len(MENU))

for index, (code, info) in enumerate(MENU.items()):
    with cols[index]:
        # Display the photo
        st.image(info["image"], use_column_width=True)
        # Display details
        st.markdown(f"**[{code}]**\n{info['name']}\n### ¥{info['price']}")
        
        # Add button specific to this item
        if st.button("➕ Add", key=f"add_{code}"):
            st.session_state.order_slip.append({
                "code": code,
                "name": info["name"],
                "price": info["price"]
            })
            st.toast(f"Added {info['name']}!") # Quick temporary cloud notification
            st.rerun()

# --- SECTION 2: LIVE ORDER SLIP & CALCULATION ---
st.markdown("---")
st.subheader("📋 Your Digital Order Slip")

if not st.session_state.order_slip:
    st.info("Your order slip is empty. Click 'Add' on the menu items above!")
else:
    total_price = 0
    for idx, item in enumerate(st.session_state.order_slip):
        item_col1, item_col2 = st.columns([4, 1])
        with item_col1:
            st.write(f"**[{item['code']}]** {item['name']} — ¥{item['price']}")
            total_price += item['price']
        with item_col2:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.order_slip.pop(idx)
                st.rerun()
                
    st.markdown("---")
    st.markdown(f"### 💰 **Total Price: ¥{total_price}**")
    
    if st.button("Clear Entire Order"):
        st.session_state.order_slip = []
        st.rerun()
