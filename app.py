import streamlit as st

# 1. メニューデータベース（本物の画像リンクと価格を設定）
MENU = {
    "BR01": {
        "name": "Milano-fu Doria (ミラノ風ドリア)", 
        "price": 300,
        "image": "https://unsplash.com" # ドリア風ピザ・グラタンイメージ
    },
    "AA01": {
        "name": "Popcorn Shrimp (ポップコーンシュリンプ)", 
        "price": 300,
        "image": "https://unsplash.com" # エビフライ・シュリンプイメージ
    },
    "DG01": {
        "name": "Italian Gelato (イタリアンジェラート)", 
        "price": 250,
        "image": "https://unsplash.com" # ジェラート・アイスイメージ
    },
}

st.title("🍕 Saizeriya Smart Order Slip")

# 注文データの記憶エリア（セッション状態）を初期化
if "order_slip" not in st.session_state:
    st.session_state.order_slip = []

# --- 新機能：【番号で検索して追加する場所】 ---
st.subheader("🔍 Search & Add by Code")
col_input, col_btn = st.columns([3, 1])

with col_input:
    # ユーザーが自由に4桁の番号を打ち込めるテキストボックス
    search_code = st.text_input("Enter 4-Digit Menu Code (e.g., BR01):", key="search_box").upper()

with col_btn:
    st.write("##") # 位置調整用の空白
    search_submitted = st.button("➕ Add Code", type="primary")

# 検索ボタンが押された時の処理
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

# --- 修正・改善：【写真付きメニューの一覧】 ---
st.markdown("---")
st.subheader("📖 Menu Catalog")
st.write("Click 'Add' directly under the photo to order:")

# メニューを横並びにするグリッド
cols = st.columns(len(MENU))

for index, (code, info) in enumerate(MENU.items()):
    with cols[index]:
        # Web上の本物の画像URLを表示（枠線にフィットさせる設定）
        st.image(info["image"], use_container_width=True)
        # メニュー名と価格
        st.markdown(f"**[{code}]**\n{info['name']}\n### ¥{info['price']}")
        
        # 写真の下の追加ボタン
        if st.button("➕ Add", key=f"catalog_add_{code}"):
            st.session_state.order_slip.append({
                "code": code,
                "name": info["name"],
                "price": info["price"]
            })
            st.toast(f"Added {info['name']}!")
            st.rerun()

# --- 注文伝票と合計金額の計算 ---
st.markdown("---")
st.subheader("📋 Your Digital Order Slip")

if not st.session_state.order_slip:
    st.info("Your order slip is empty.")
else:
    total_price = 0
    for idx, item in enumerate(st.session_state.order_slip):
        item_col1, item_col2 = st.columns([5, 1])
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
