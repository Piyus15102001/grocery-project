import streamlit as st
import sqlite3
from datetime import datetime
import qrcode
from io import BytesIO
from PIL import Image

# Connect to SQLite DB
conn = sqlite3.connect("grocery_orders.db", check_same_thread=False)
c = conn.cursor()

# Create tables if not exist
c.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    item TEXT,
    quantity INTEGER,
    price REAL,
    order_time TEXT
)''')
conn.commit()

# Expanded product data (100 products with single price per unit)
PRODUCTS = [
    {"name": "Sugar", "emoji": "\U0001F9C2", "category": "Essentials", "price": 50,
     "image": "https://via.placeholder.com/150?text=Sugar"},
    {"name": "Thums Up", "emoji": "\U0001F964", "category": "Drinks", "price": 40,
     "image": "https://via.placeholder.com/150?text=Thums+Up"},
    {"name": "Sprite", "emoji": "\U0001F964", "category": "Drinks", "price": 38,
     "image": "https://via.placeholder.com/150?text=Sprite"},
    {"name": "Maaza Mango Drink", "emoji": "\U0001F96D", "category": "Drinks", "price": 60,
     "image": "https://via.placeholder.com/150?text=Maaza"},
    {"name": "Good Life Sunflower Oil", "emoji": "\U0001F6E2\uFE0F", "category": "Oils", "price": 130,
     "image": "https://via.placeholder.com/150?text=Sunflower+Oil"},
    {"name": "Mirinda Orange", "emoji": "\U0001F9C3", "category": "Drinks", "price": 70,
     "image": "https://via.placeholder.com/150?text=Mirinda"},
    {"name": "Basmati Rice", "emoji": "\U0001F33E", "category": "Essentials", "price": 80,
     "image": "https://via.placeholder.com/150?text=Rice"},
    {"name": "Wheat Flour", "emoji": "\U0001F33E", "category": "Essentials", "price": 40,
     "image": "https://via.placeholder.com/150?text=Wheat+Flour"},
    {"name": "Dettol Soap", "emoji": "\U0001F9FC", "category": "Personal Care", "price": 30,
     "image": "https://via.placeholder.com/150?text=Dettol+Soap"},
    {"name": "Colgate Toothpaste", "emoji": "\U0001F9B7", "category": "Personal Care", "price": 50,
     "image": "https://via.placeholder.com/150?text=Colgate"},
    {"name": "Durex Condoms", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 80,
     "image": "https://via.placeholder.com/150?text=Durex"},
    {"name": "Parle-G Biscuits", "emoji": "\U0001F36A", "category": "Snacks", "price": 20,
     "image": "https://via.placeholder.com/150?text=Parle-G"},
    {"name": "Lays Chips", "emoji": "\U0001F35F", "category": "Snacks", "price": 20,
     "image": "https://via.placeholder.com/150?text=Lays"},
    {"name": "Maggi Noodles", "emoji": "\U0001F35C", "category": "Essentials", "price": 12,
     "image": "https://via.placeholder.com/150?text=Maggi"},
    {"name": "Coca-Cola", "emoji": "\U0001F964", "category": "Drinks", "price": 40,
     "image": "https://via.placeholder.com/150?text=Coca-Cola"},
    {"name": "Amul Butter", "emoji": "\U0001F9C8", "category": "Dairy", "price": 50,
     "image": "https://via.placeholder.com/150?text=Amul+Butter"},
    {"name": "Amul Milk", "emoji": "\U0001F95B", "category": "Dairy", "price": 25,
     "image": "https://via.placeholder.com/150?text=Amul+Milk"},
    {"name": "Nescafe Coffee", "emoji": "\U0001F375", "category": "Beverages", "price": 100,
     "image": "https://via.placeholder.com/150?text=Nescafe"},
    {"name": "Tata Tea", "emoji": "\U0001F375", "category": "Beverages", "price": 80,
     "image": "https://via.placeholder.com/150?text=Tata+Tea"},
    {"name": "Durex Lubricant", "emoji": "\U0001F9F4", "category": "Personal Care", "price": 200,
     "image": "https://via.placeholder.com/150?text=Durex+Lubricant"},
    {"name": "Haldiram's Namkeen", "emoji": "\U0001F35F", "category": "Snacks", "price": 50,
     "image": "https://via.placeholder.com/150?text=Haldiram"},
    {"name": "Durex Massage Gel", "emoji": "\U0001F9F4", "category": "Personal Care", "price": 350,
     "image": "https://via.placeholder.com/150?text=Massage+Gel"},
    {"name": "Patanjali Honey", "emoji": "\U0001F36F", "category": "Essentials", "price": 70,
     "image": "https://via.placeholder.com/150?text=Honey"},
    {"name": "Saffola Oil", "emoji": "\U0001F6E2\uFE0F", "category": "Oils", "price": 150,
     "image": "https://via.placeholder.com/150?text=Saffola+Oil"},
    {"name": "Fortune Mustard Oil", "emoji": "\U0001F6E2\uFE0F", "category": "Oils", "price": 120,
     "image": "https://via.placeholder.com/150?text=Mustard+Oil"},
    {"name": "Durex Condoms Extra Thin", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Extra+Thin"},
    {"name": "Kissan Jam", "emoji": "\U0001F9C7", "category": "Essentials", "price": 60,
     "image": "https://via.placeholder.com/150?text=Kissan+Jam"},
    {"name": "Britannia Biscuits", "emoji": "\U0001F36A", "category": "Snacks", "price": 25,
     "image": "https://via.placeholder.com/150?text=Britannia"},
    {"name": "Horlicks", "emoji": "\U0001F95B", "category": "Beverages", "price": 200,
     "image": "https://via.placeholder.com/150?text=Horlicks"},
    {"name": "Cadbury Dairy Milk", "emoji": "\U0001F36B", "category": "Snacks", "price": 40,
     "image": "https://via.placeholder.com/150?text=Dairy+Milk"},
    {"name": "Amul Cheese", "emoji": "\U0001F9C0", "category": "Dairy", "price": 80,
     "image": "https://via.placeholder.com/150?text=Amul+Cheese"},
    {"name": "Surf Excel Detergent", "emoji": "\U0001F9FC", "category": "Household", "price": 150,
     "image": "https://via.placeholder.com/150?text=Surf+Excel"},
    {"name": "Harpic Toilet Cleaner", "emoji": "\U0001F9F9", "category": "Household", "price": 90,
     "image": "https://via.placeholder.com/150?text=Harpic"},
    {"name": "Lizol Floor Cleaner", "emoji": "\U0001F9F9", "category": "Household", "price": 100,
     "image": "https://via.placeholder.com/150?text=Lizol"},
    {"name": "Durex Condoms Ribbed", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 85,
     "image": "https://via.placeholder.com/150?text=Durex+Ribbed"},
    {"name": "Ponds Face Cream", "emoji": "\U0001F9F4", "category": "Personal Care", "price": 120,
     "image": "https://via.placeholder.com/150?text=Ponds"},
    {"name": "Durex Condoms Flavored", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 95,
     "image": "https://via.placeholder.com/150?text=Durex+Flavored"},
    {"name": "Tropicana Juice", "emoji": "\U0001F9C3", "category": "Drinks", "price": 100,
     "image": "https://via.placeholder.com/150?text=Tropicana"},
    {"name": "Real Juice", "emoji": "\U0001F9C3", "category": "Drinks", "price": 90,
     "image": "https://via.placeholder.com/150?text=Real+Juice"},
    {"name": "Durex Condoms Extra Time", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 100,
     "image": "https://via.placeholder.com/150?text=Durex+Extra+Time"},
    {"name": "Amul Curd", "emoji": "\U0001F95B", "category": "Dairy", "price": 30,
     "image": "https://via.placeholder.com/150?text=Amul+Curd"},
    {"name": "Mother Dairy Milk", "emoji": "\U0001F95B", "category": "Dairy", "price": 48,
     "image": "https://via.placeholder.com/150?text=Mother+Dairy"},
    {"name": "Durex Condoms Dotted", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Dotted"},
    {"name": "Patanjali Ghee", "emoji": "\U0001F9C8", "category": "Essentials", "price": 300,
     "image": "https://via.placeholder.com/150?text=Patanjali+Ghee"},
    {"name": "Durex Massage Oil", "emoji": "\U0001F9F4", "category": "Personal Care", "price": 250,
     "image": "https://via.placeholder.com/150?text=Massage+Oil"},
    {"name": "Bournvita", "emoji": "\U0001F95B", "category": "Beverages", "price": 220,
     "image": "https://via.placeholder.com/150?text=Bournvita"},
    {"name": "Durex Condoms Ultra Thin", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 95,
     "image": "https://via.placeholder.com/150?text=Durex+Ultra+Thin"},
    {"name": "Durex Lubricant Gel", "emoji": "\U0001F9F4", "category": "Personal Care", "price": 220,
     "image": "https://via.placeholder.com/150?text=Durex+Gel"},
    {"name": "Durex Condoms Real Feel", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 100,
     "image": "https://via.placeholder.com/150?text=Durex+Real+Feel"},
    {"name": "Durex Condoms Pleasure Me", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Pleasure+Me"},
    {"name": "Durex Condoms Extended Pleasure", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 95,
     "image": "https://via.placeholder.com/150?text=Durex+Extended"},
    {"name": "Tata Salt", "emoji": "\U0001F9C2", "category": "Essentials", "price": 20,
     "image": "https://via.placeholder.com/150?text=Tata+Salt"},
    {"name": "Durex Condoms Mutual Climax", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 100,
     "image": "https://via.placeholder.com/150?text=Durex+Mutual+Climax"},
    {"name": "Durex Condoms Intense", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 95,
     "image": "https://via.placeholder.com/150?text=Durex+Intense"},
    {"name": "Durex Condoms Extra Ribbed", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Extra+Ribbed"},
    {"name": "Durex Condoms Tingle", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 95,
     "image": "https://via.placeholder.com/150?text=Durex+Tingle"},
    {"name": "Durex Condoms Strawberry", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Strawberry"},
    {"name": "Durex Condoms Chocolate", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Chocolate"},
    {"name": "Durex Condoms Bubblegum", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Bubblegum"},
    {"name": "Durex Condoms Orange", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Orange"},
    {"name": "Durex Condoms Banana", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Banana"},
    {"name": "Durex Condoms Mint", "emoji": "\U0001F9F9", "category": "Personal Care", "price": 90,
     "image": "https://via.placeholder.com/150?text=Durex+Mint"},
    {"name": "Turmeric Powder", "emoji": "\U0001F33F", "category": "Spices", "price": 20,
     "image": "https://via.placeholder.com/150?text=Turmeric"},
    {"name": "Cumin Seeds", "emoji": "\U0001F33F", "category": "Spices", "price": 30,
     "image": "https://via.placeholder.com/150?text=Cumin"},
    {"name": "Coriander Powder", "emoji": "\U0001F33F", "category": "Spices", "price": 25,
     "image": "https://via.placeholder.com/150?text=Coriander"},
    {"name": "Red Chili Powder", "emoji": "\U0001F33F", "category": "Spices", "price": 28,
     "image": "https://via.placeholder.com/150?text=Chili+Powder"},
    {"name": "Lentils (Masoor Dal)", "emoji": "\U0001F33E", "category": "Pulses", "price": 70,
     "image": "https://via.placeholder.com/150?text=Lentils"},
    {"name": "Chickpeas", "emoji": "\U0001F33E", "category": "Pulses", "price": 60,
     "image": "https://via.placeholder.com/150?text=Chickpeas"},
    {"name": "Kidney Beans", "emoji": "\U0001F33E", "category": "Pulses", "price": 80,
     "image": "https://via.placeholder.com/150?text=Kidney+Beans"},
    {"name": "Black Gram", "emoji": "\U0001F33E", "category": "Pulses", "price": 90,
     "image": "https://via.placeholder.com/150?text=Black+Gram"},
    {"name": "Apples", "emoji": "\U0001F34E", "category": "Fruits", "price": 100,
     "image": "https://via.placeholder.com/150?text=Apples"},
    {"name": "Bananas", "emoji": "\U0001F34C", "category": "Fruits", "price": 40,
     "image": "https://via.placeholder.com/150?text=Bananas"},
    {"name": "Oranges", "emoji": "\U0001F34A", "category": "Fruits", "price": 60,
     "image": "https://via.placeholder.com/150?text=Oranges"},
    {"name": "Mangoes", "emoji": "\U0001F96D", "category": "Fruits", "price": 120,
     "image": "https://via.placeholder.com/150?text=Mangoes"},
    {"name": "Potatoes", "emoji": "\U0001F954", "category": "Vegetables", "price": 30,
     "image": "https://via.placeholder.com/150?text=Potatoes"},
    {"name": "Onions", "emoji": "\U0001F9C5", "category": "Vegetables", "price": 25,
     "image": "https://via.placeholder.com/150?text=Onions"},
    {"name": "Tomatoes", "emoji": "\U0001F345", "category": "Vegetables", "price": 35,
     "image": "https://via.placeholder.com/150?text=Tomatoes"},
    {"name": "Carrots", "emoji": "\U0001F955", "category": "Vegetables", "price": 40,
     "image": "https://via.placeholder.com/150?text=Carrots"},
    {"name": "Kurkure", "emoji": "\U0001F35F", "category": "Snacks", "price": 20,
     "image": "https://via.placeholder.com/150?text=Kurkure"},
    {"name": "Bingo Chips", "emoji": "\U0001F35F", "category": "Snacks", "price": 20,
     "image": "https://via.placeholder.com/150?text=Bingo"},
    {"name": "Uncle Chipps", "emoji": "\U0001F35F", "category": "Snacks", "price": 20,
     "image": "https://via.placeholder.com/150?text=Uncle+Chipps"},
    {"name": "Balaji Wafers", "emoji": "\U0001F35F", "category": "Snacks", "price": 20,
     "image": "https://via.placeholder.com/150?text=Balaji+Wafers"},
    {"name": "Lipton Tea", "emoji": "\U0001F375", "category": "Beverages", "price": 90,
     "image": "https://via.placeholder.com/150?text=Lipton+Tea"},
    {"name": "Bru Coffee", "emoji": "\U0001F375", "category": "Beverages", "price": 110,
     "image": "https://via.placeholder.com/150?text=Bru+Coffee"},
    {"name": "Red Bull", "emoji": "\U0001F964", "category": "Drinks", "price": 125,
     "image": "https://via.placeholder.com/150?text=Red+Bull"},
    {"name": "Pepsi", "emoji": "\U0001F964", "category": "Drinks", "price": 40,
     "image": "https://via.placeholder.com/150?text=Pepsi"},
    {"name": "Vim Dishwash", "emoji": "\U0001F9FC", "category": "Household", "price": 70,
     "image": "https://via.placeholder.com/150?text=Vim+Dishwash"},
    {"name": "Pril Liquid", "emoji": "\U0001F9FC", "category": "Household", "price": 80,
     "image": "https://via.placeholder.com/150?text=Pril+Liquid"},
    {"name": "Odonil Air Freshener", "emoji": "\U0001F9F9", "category": "Household", "price": 50,
     "image": "https://via.placeholder.com/150?text=Odonil"},
    {"name": "Durex Cleaning Wipes", "emoji": "\U0001F9F9", "category": "Household", "price": 60,
     "image": "https://via.placeholder.com/150?text=Cleaning+Wipes"},
    {"name": "Moong Dal", "emoji": "\U0001F33E", "category": "Pulses", "price": 75,
     "image": "https://via.placeholder.com/150?text=Moong+Dal"},
    {"name": "Toor Dal", "emoji": "\U0001F33E", "category": "Pulses", "price": 80,
     "image": "https://via.placeholder.com/150?text=Toor+Dal"},
    {"name": "Chana Dal", "emoji": "\U0001F33E", "category": "Pulses", "price": 65,
     "image": "https://via.placeholder.com/150?text=Chana+Dal"},
    {"name": "Garam Masala", "emoji": "\U0001F33F", "category": "Spices", "price": 35,
     "image": "https://via.placeholder.com/150?text=Garam+Masala"},
    {"name": "Pav Bhaji Masala", "emoji": "\U0001F33F", "category": "Spices", "price": 30,
     "image": "https://via.placeholder.com/150?text=Pav+Bhaji+Masala"},
    {"name": "Black Pepper", "emoji": "\U0001F33F", "category": "Spices", "price": 50,
     "image": "https://via.placeholder.com/150?text=Black+Pepper"},
    {"name": "Pomegranate", "emoji": "\U0001F352", "category": "Fruits", "price": 150,
     "image": "https://via.placeholder.com/150?text=Pomegranate"},
    {"name": "Spinach", "emoji": "\U0001F96C", "category": "Vegetables", "price": 20,
     "image": "https://via.placeholder.com/150?text=Spinach"},
    {"name": "Broccoli", "emoji": "\U0001F966", "category": "Vegetables", "price": 60,
     "image": "https://via.placeholder.com/150?text=Broccoli"},
    {"name": "Cabbage", "emoji": "\U0001F966", "category": "Vegetables", "price": 25,
     "image": "https://via.placeholder.com/150?text=Cabbage"},
    {"name": "Amul Ice Cream", "emoji": "\U0001F368", "category": "Dairy", "price": 100,
     "image": "https://via.placeholder.com/150?text=Amul+Ice+Cream"},
    {"name": "Yippee Noodles", "emoji": "\U0001F35C", "category": "Essentials", "price": 15,
     "image": "https://via.placeholder.com/150?text=Yippee+Noodles"}
]

# Session state for cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# Title
st.set_page_config(page_title="Piyush Grocery", layout="wide")
st.title("\U0001F34E Welcome to Piyush Grocery")
st.markdown("Your one-stop shop for groceries – JioMart Style!")

# Tabs
page = st.sidebar.selectbox("Select Page", ["Shop", "Cart", "Admin Dashboard"])

if page == "Shop":
    st.header("\U0001F6D2 Browse Products")
    categories = sorted(set(p['category'] for p in PRODUCTS))
    selected_cat = st.selectbox("Select Category", categories)

    # Use columns for a grid layout
    cols = st.columns(3)  # 3 products per row
    for i, product in enumerate(PRODUCTS):
        if product['category'] == selected_cat:
            with cols[i % 3]:
                try:
                    st.image(product['image'], width=100)  # Display product image
                except:
                    st.image("https://via.placeholder.com/150?text=No+Image", width=100)
                st.markdown(f"### {product['emoji']} {product['name']}")
                qty = st.number_input(f"Quantity for {product['name']}", min_value=1, value=1, step=1,
                                      key=f"qty_{product['name']}")
                if st.button(f"Add to Cart - Rs.{product['price']} each", key=f"add_{product['name']}"):
                    st.session_state.cart.append({
                        "item": product['name'],
                        "quantity": qty,
                        "price": product['price'] * qty,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.success(f"Added {qty} {product['name']} to cart")

elif page == "Cart":
    st.header("\U0001F6CD Your Shopping Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty")
    else:
        total = 0
        for i, item in enumerate(st.session_state.cart):
            st.write(f"{item['item']} - {item['quantity']} units - Rs.{item['price']}")
            total += item['price']
        st.markdown(f"### Total: Rs.{total}")

        # Payment method selection
        payment_method = st.selectbox("Select Payment Method", ["QR Code", "Credit Card", "Net Banking"])

        if payment_method == "QR Code":
            # Generate QR code for payment (simulated)
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"Pay Rs.{total} to Piyush Grocery")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            st.image(buf, caption="Scan this QR code to pay", width=200)

        elif payment_method == "Credit Card":
            with st.form("credit_card_form"):
                card_number = st.text_input("Card Number", max_chars=16)
                expiry = st.text_input("Expiry Date (MM/YY)", max_chars=5)
                cvv = st.text_input("CVV", max_chars=3, type="password")
                submitted = st.form_submit_button("Pay Now")
                if submitted:
                    if card_number and expiry and cvv:
                        st.success("Credit card payment processed (simulated)!")
                    else:
                        st.error("Please fill all fields")

        elif payment_method == "Net Banking":
            banks = ["SBI", "HDFC", "ICICI", "Axis", "Kotak"]
            bank = st.selectbox("Select Bank", banks)
            if st.button("Proceed to Net Banking"):
                st.success(f"Redirecting to {bank} net banking (simulated)!")

        if st.button("Confirm Payment and Checkout"):
            for item in st.session_state.cart:
                c.execute("INSERT INTO orders (user, item, quantity, price, order_time) VALUES (?, ?, ?, ?, ?)",
                          ("Guest", item['item'], item['quantity'], item['price'], item['time']))
            conn.commit()
            st.success(f"Order placed successfully via {payment_method}!")
            st.session_state.cart.clear()

elif page == "Admin Dashboard":
    st.header("\U0001F4CA Admin Dashboard")
    c.execute("SELECT * FROM orders ORDER BY order_time DESC")
    rows = c.fetchall()
    if rows:
        st.dataframe(rows, use_container_width=True, column_config={
            "0": "Order ID",
            "1": "User",
            "2": "Item",
            "3": "Quantity",
            "4": "Price",
            "5": "Order Time"
        })
    else:
        st.info("No orders yet.")