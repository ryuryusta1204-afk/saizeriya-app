import streamlit as st

# 1. メニューデータベース
MENU = {
    "BR01": {
        "name": "Milano-fu Doria (ミラノ風ドリア)", 
        "price": 300,
        "image": "https://unsplash.com"
    },
    "AA01": {
        "name": "Popcorn Shrimp (ポップコーンシュリンプ)", 
        "price": 300,
        "image": "https://unsplash.com"
    },
    "DG01": {
        "name": "Italian Gelato (イタリアンジェラート)", 
        "price": 250,
        "image": "https://unsplash.com"
    },
}

# --- 画面切り替えの仕組み（セッション状態） ---
if "page" not in st.session_state:
    st.session_state.page = "order"

if "order_slip" not in st.session_state:
    st.session_state.order_slip = []

if "final_order" not in st.session_state:
    st.session_state.final_order = []
if "final_total" not in st.session_state:
    st.session_state.final_total = 0


# ==========================================
# 状態A: 【注文完了画面 (done)】
# ==========================================
if st.session_state.page == "done":
    st.balloons() # 画面にお祝いの風船を飛ばす演出
    st.title("🎉 Order Completed!")
    st.success("ご注文が完了しました！厨房にデータが送信されました（風表示）。")
    
    st.subheader("📋 ご注文内容の確認")
    for item in st.session_state.final_order:
        st.write(f"- **[{item['code']}]** {item['name']} — ¥{item['price']}")
    
    st.markdown("---")
    st.markdown(f"### 💰 **合計金額: ¥{st.session_state.final_total}**")
    
    st.write("またのご利用をお待ちしております！")
    
    # 最初の注文画面に戻るボタン
    if st.button("トップに戻って新しく注文する", type="primary"):
        st.session_state.order_slip = [] 
        st.session_state.page = "order"   
        st.rerun()

# ==========================================
# 状態B: 【いつもの注文画面 (order)】
# ==========================================
else:
    st.title("🍕 Saizeriya Smart Order Slip")

    # --- 1. 番号で検索して追加 ---
    st.subheader("🔍 Search & Add by Code")
    col_input, col_btn = st.columns(2)

    with col_input:
        search_code = st.text_input("Enter 4-Digit Menu Code (e.g., BR01):", key="search_box").upper()
    with col_btn:
        st.write("##") 
        search_submitted = st.button("➕ Add Code", type="primary")

    if search_submitted and search_code:
        if search_code in MENU:
            st.session_state.order_slip.append({
                "code": search_code,
                "name": MENU[search_code]["name"],
                "price": MENU[search_code]["price"]
            })
            st.toast(f"Added {MENU[search_code]['name']}!")
            st.rerun()
        else:
            st.error("Item code not found. Please try again.")

    # --- 2. 写真付きメニューの一覧 ---
    st.markdown("---")
    st.subheader("📖 Menu Catalog")
    
    cols = st.columns(len(MENU))
    for index, (code, info) in enumerate(MENU.items()):
        with cols[index]:
            # 💡 エラー原因になりやすい設定を、最も安全な昔ながらの書き方（use_column_width=True）に変更しました
            st.image(info["image"], use_column_width=True)
            st.markdown(f"**[{code}]**\n{info['name']}\n### ¥{info['price']}")
            
            if st.button("➕ Add", key=f"catalog_add_{code}"):
                st.session_state.order_slip.append({
                    "code": code,
                    "name": info["name"],
                    "price": info["price"]
                })
                st.toast(f"Added {info['name']}!")
                st.rerun()

    # --- 3. 注文伝票と合計金額 ---
    st.markdown("---")
    st.subheader("📋 Your Digital Order Slip")

    if not st.session_state.order_slip:
        st.info("Your order slip is empty.")
    else:
        total_price = 0
        for idx, item in enumerate(st.session_state.order_slip):
            item_col1, item_col2 = st.columns(2)
            with item_col1:
                st.write(f"**[{item['code']}]** {item['name']} — ¥{item['price']}")
                total_price += item['price']
            with item_col2:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.order_slip.pop(idx)
                    st.rerun()
                    
        st.markdown("---")
        st.markdown(f"### 💰 **Total Price: ¥{total_price}**")
        
        col_clear, col_submit = st.columns(2)
        
        with col_clear:
            if st.button("Clear Entire Order", use_container_width=True):
                st.session_state.order_slip = []
                st.rerun()
                
        with col_submit:
            if st.button("🚀 注文を確定する", type="primary", use_container_width=True):
                st.session_state.final_order = st.session_state.order_slip.copy()
                st.session_state.final_total = total_price
                st.session_state.page = "done"
                st.rerun()
