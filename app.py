import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import requests
# import database (Removed: Only API talks to DB now)
from fpdf import FPDF

# Page Config 
st.set_page_config(
    page_title="CarVal: Intelligent Car Valuation System",
    page_icon="⚡",
    layout="wide"
)

st.sidebar.title("CarVal Engine")

# Sidebar Navigation Header
st.sidebar.markdown("<h3 style='color: #94a3b8; font-size: 16px; margin-bottom: -10px;'>Navigation Menu</h3>", unsafe_allow_html=True)

# Sidebar Navigation
page = st.sidebar.radio("", [
    "❖ Overview",
    "⚡ Price Prediction",
    "🔍 Find My Car",
    "📊 Market Analytics",
    "⚖️ Vehicle Comparison",
    "🛡️ Admin Portal"
], label_visibility="collapsed")


# ==========================================
# 🎨 CUSTOM UI STYLING (CSS)
# We inject custom CSS to override Streamlit's default 
# simple look and give it a premium "Dark Mode" dashboard feel.
# ==========================================

st.markdown("""
<style>

/* -------- GLOBAL BACKGROUND -------- */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #020617);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* -------- HERO TITLE -------- */
.hero-title {
    font-size: 50px;
    font-weight: 800;
    line-height: 1.2;
    background: linear-gradient(90deg, #f8fafc, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    margin-top: 20px;
}

.hero-subtitle {
    font-size: 20px;
    color: #38bdf8;
    font-weight: 500;
    margin-bottom: 25px;
}

/* -------- GLASS CARD -------- */
.card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 18px;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.7);
}

/* -------- RESULT BOX -------- */
.result-box {
    background: linear-gradient(135deg, #2563eb, #38bdf8);
    padding: 25px;
    border-radius: 14px;
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    color: white;
    margin-top: 25px;
    box-shadow: 0 0 20px rgba(56,189,248,0.5);
}

/* -------- STATS BOX -------- */
.stat-box {
    text-align: center;
    padding: 20px;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #38bdf8;
}

.stat-label {
    font-size: 14px;
    color: #94a3b8;
}

/* -------- BUTTON -------- */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #6366f1);
    color: white;
    border-radius: 10px;
    padding: 0.6em 1.5em;
    font-weight: 600;
    border: none;
    width: 100%;
    transition: all 0.25s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(99,102,241,0.6);
}

/* -------- INPUT FIELDS -------- */
input, .stSelectbox, .stNumberInput {
    border-radius: 10px !important;
}

/* Fix Slider Visibility in Dark Mode */
div[data-baseweb="slider"] * {
    color: white !important;
}
.stSlider > div > div > div > div {
    color: white !important;
}

/* -------- REMOVE DEFAULT STREAMLIT SPACE -------- */
.block-container {
    padding-top: 3.5rem;
    padding-bottom: 2rem;
}


/* -------- IMAGE STYLING -------- */
img {
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

import os

# Define API URL (Dynamic for Cloud Deployment)
# On Render, we will set the API_URL environment variable to the URL of the backend.
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ==========================================
# 💾 DATA LOADING
# @st.cache_data ensures the CSV is only loaded once, making the app much faster!
# ==========================================
@st.cache_data
def load_data():
    data = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")
    # Extract the first word as the Brand (e.g. "Maruti Swift" -> "Maruti")
    data["brand"] = data["name"].apply(lambda x: str(x).split()[0])
    # Extract the second word as the Model (e.g. "Maruti Swift" -> "Swift")
    data["model"] = data["name"].apply(lambda x: x.split()[1] if len(x.split()) > 1 else "Unknown")
    return data

df = load_data()

# ---------- HOME ----------
if page == "❖ Overview":

    # HERO SECTION (Split Layout)
    col1, col2 = st.columns([0.9, 1.2], gap="large")

    with col1:
        st.markdown("<div class='hero-title'>CarVal</div>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Intelligent Car Valuation System</div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:16px; margin-top:-15px; margin-bottom:20px;'>Predict • Analyze • Compare</p>", unsafe_allow_html=True)

        st.markdown("""
        <div class='card'>
        <p style='font-size:16px; line-height:1.7'>
        This intelligent system uses <b>Machine Learning</b> to estimate true worth of your car based on:
        </p>
        <ul style='line-height:1.8'>
            <li>Brand & Model</li>
            <li>Fuel Type & Transmission</li>
            <li>Ownership History</li>
            <li>Car Age & Kilometers Driven</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=800&h=500&auto=format&fit=crop",
            use_container_width=True
        )

    # SPACING
    st.markdown("<br>", unsafe_allow_html=True)

    # DASHBOARD STATS (Premium Cards)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    avg_price = int(df['selling_price'].mean())
    max_price = int(df['selling_price'].max())
    min_price = int(df['selling_price'].min())

    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-value'>₹{avg_price:,.0f}</div>
            <div class='stat-label'>Average Price</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-value'>₹{max_price:,.0f}</div>
            <div class='stat-label'>Maximum Price</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-value'>₹{min_price:,.0f}</div>
            <div class='stat-label'>Minimum Price</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # EXTRA PREMIUM SECTION (Optional but powerful)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    <h3 style='margin-bottom:10px;'>System Capabilities</h3>
    <ul style='line-height:1.8'>
        <li>Real-time price prediction using trained ML model</li>
        <li>Data-driven market insights</li>
        <li>Interactive comparison of vehicles</li>
        <li>Clean and modern dashboard UI</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

 

# ---------- PREDICT ----------

elif page == "⚡ Price Prediction":
    st.markdown("<h1 style='text-align:center;'>Vehicle Price Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Enter your car details and get an instant price estimate</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("Brand", sorted(df["brand"].unique()))

        fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
        owner = st.selectbox("Owner", [
            "First Owner", "Second Owner", "Third Owner",
            "Fourth & Above Owner", "Test Drive Car"
        ])

    with col2:
        # Dynamic Model based on brand
        models_list = df[df["brand"] == brand]["model"].unique()
        # fallback if no models found (edge case)
        if len(models_list) == 0:
          models_list = df["model"].dropna().unique()
        model_name = st.selectbox("Model", sorted(models_list))


        year = st.slider("Year of Manufacture", min_value=1990, max_value=datetime.now().year, value=2015, step=1)
        km_driven = st.slider("Kilometers Driven", min_value=0, max_value=500000, value=30000, step=5000)
        seller_type = st.selectbox("Seller Type", ["Dealer", "Individual", "Trustmark Dealer"])

    if st.button("Calculate Valuation"):
        car_age = datetime.now().year - year
        km_driven_cap = min(km_driven, 500000)

        # ==========================================
        # 🤖 SEND DATA TO BACKEND AI ENGINE
        # Instead of doing the complex math here, we package the user's inputs
        # into a JSON 'payload' and send it to our FastAPI backend server.
        # ==========================================
        payload = {
            "brand": brand,
            "model": model_name,
            "year": year,
            "km_driven": km_driven,
            "fuel": fuel,
            "transmission": transmission,
            "seller_type": seller_type,
            "owner": owner
        }

        try:
            # Send HTTP POST request to the API
            response = requests.post(f"{API_URL}/predict", json=payload)
            response.raise_for_status()
            # Extract the predicted price from the API's response
            prediction = response.json()["predicted_price"]
        except Exception as e:
            st.error(f"Backend API Error: Make sure api.py is running! Details: {e}")
            prediction = 0

        # Category
        if prediction < 300000:
            category = "Budget Car"
        elif prediction < 800000:
            category = "Mid-range Car"
        else:
            category = "Premium Car"

        st.markdown(f"<div class='result-box'>₹ {prediction:,.0f}</div>", unsafe_allow_html=True)
        st.write("Category:", category)

        if prediction > 1000000:
            st.info("Luxury Segment Vehicle")
        elif prediction > 500000:
            st.info("Mid-range Segment Vehicle")
        else:
            st.info("Budget Segment Vehicle")

        if km_driven > 200000:
            st.warning("High kilometers driven may reduce accuracy")

        # --- WHY THIS PRICE SECTION ---
        with st.expander("Price Breakdown Analysis (Data-Driven Insights)"):
            st.markdown("### Price Breakdown Context")
            
            # Find similar cars in the dataset
            similar_cars = df[(df['brand'] == brand) & (df['model'] == model_name)]
            
            if len(similar_cars) < 3:
                st.write(f"We don't have enough historical data for the **{brand} {model_name}** to provide a detailed comparison. The price is based on general brand and market trends.")
            else:
                avg_model_price = similar_cars['selling_price'].mean()
                
                st.write(f"The average selling price for a **{brand} {model_name}** in our database is **₹{avg_model_price:,.0f}**.")
                
                diff = prediction - avg_model_price
                if diff > 0:
                    st.success(f"Your estimated value is **₹{diff:,.0f} higher** than the historical average. Here is why:")
                elif diff < 0:
                    st.error(f"Your estimated value is **₹{abs(diff):,.0f} lower** than the historical average. Here is why:")
                else:
                    st.info("Your estimated value matches the historical average exactly.")
                
                # Factor 1: Age / Year
                avg_year = similar_cars['year'].mean()
                if year > avg_year:
                    st.write(f"- 📈 **Age:** Your car is from **{year}**, which is newer than the average (around **{int(avg_year)}**). Newer cars retain more value.")
                elif year < avg_year:
                    st.write(f"- 📉 **Age:** Your car is from **{year}**, which is older than the average (around **{int(avg_year)}**). Depreciation lowers the value.")
                else:
                    st.write(f"- ➖ **Age:** Your car is right around the average age for this model.")
                
                # Factor 2: Kilometers Driven
                avg_km = similar_cars['km_driven'].mean()
                if km_driven < avg_km:
                    st.write(f"- 📈 **Kilometers Driven:** It has been driven **{km_driven:,} km**, which is less than the average **{int(avg_km):,} km**. Lower kilometers boost value.")
                elif km_driven > avg_km:
                    st.write(f"- 📉 **Kilometers Driven:** It has been driven **{km_driven:,} km**, which is more than the average **{int(avg_km):,} km**. Higher kilometers decrease value.")
                else:
                    st.write(f"- ➖ **Kilometers Driven:** The kilometers driven is very close to the average for this model.")
                
                # Factor 3: Transmission
                if transmission == "Automatic":
                    st.write("- 📈 **Transmission:** Automatic vehicles generally command a premium in the market compared to manual variants.")
                
                st.caption("Note: These insights compare your specific inputs against the historical dataset used to train the AI.")

        # --- PDF CERTIFICATE GENERATION ---
        st.markdown("---")
        st.subheader("Official Documents")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=24)
        pdf.cell(0, 20, txt="Vehicle Valuation Certificate", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='R')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 10, txt="Vehicle Specifications", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, txt=f"Brand: {brand}", ln=True)
        pdf.cell(0, 8, txt=f"Model: {model_name}", ln=True)
        pdf.cell(0, 8, txt=f"Year of Manufacture: {year}", ln=True)
        pdf.cell(0, 8, txt=f"Kilometers Driven: {km_driven:,.0f} km", ln=True)
        pdf.cell(0, 8, txt=f"Fuel Type: {fuel}", ln=True)
        pdf.cell(0, 8, txt=f"Transmission: {transmission}", ln=True)
        pdf.cell(0, 8, txt=f"Ownership: {owner}", ln=True)
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', size=18)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 15, txt=f"Estimated Market Value: INR {prediction:,.0f}", ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'I', size=10)
        pdf.ln(20)
        pdf.cell(0, 10, txt="This is an AI-generated estimate based on historical market data.", ln=True, align='C')
        pdf.cell(0, 10, txt="Powered by Car Valuation Engine", ln=True, align='C')
        
        pdf_bytes = pdf.output(dest="S")
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode('latin-1')
        else:
            pdf_bytes = bytes(pdf_bytes)

        st.download_button(
            label="📄 Download Official Valuation Certificate (PDF)",
            data=pdf_bytes,
            file_name=f"{brand}_{model_name}_Valuation.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
# ---------- FIND MY CAR ----------
elif page == "🔍 Find My Car":
    st.markdown("<h1 style='text-align:center;'>🔍 Find My Car</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Let AI find the perfect car for your budget and preferences</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        budget = st.slider("Max Budget (INR)", min_value=100000, max_value=5000000, value=500000, step=50000)
        pref_fuel = st.multiselect("Preferred Fuel", df["fuel"].unique(), default=["Petrol", "Diesel"])
    with col2:
        pref_trans = st.multiselect("Preferred Transmission", df["transmission"].unique(), default=["Manual", "Automatic"])
        max_km = st.slider("Max Kilometers Driven", min_value=10000, max_value=300000, value=80000, step=10000)

    if st.button("Search Vehicles"):
        mask = (df["selling_price"] <= budget) & (df["km_driven"] <= max_km)
        if pref_fuel:
            mask = mask & (df["fuel"].isin(pref_fuel))
        if pref_trans:
            mask = mask & (df["transmission"].isin(pref_trans))
            
        matches = df[mask].copy()
        
        if len(matches) == 0:
            st.warning("No cars found in this budget and preference. Try widening your criteria.")
        else:
            st.success(f"Found {len(matches)} matching cars! Here are the top recommendations (Best Value):")
            
            # Simple score: newer is better, lower km is better
            matches['score'] = matches['year'] - (matches['km_driven'] / 10000)
            best_matches = matches.sort_values('score', ascending=False).head(10)
            
            display_cols = ["name", "year", "selling_price", "km_driven", "fuel", "transmission"]
            st.dataframe(
                best_matches[display_cols].style.format({"selling_price": "₹{:,.0f}", "km_driven": "{:,.0f} km"}),
                hide_index=True,
                use_container_width=True
            )
            
            fig = px.scatter(best_matches, x="km_driven", y="selling_price", size="year", color="name", 
                             hover_name="name", template="plotly_dark", title="Top Recommendations: Price vs Kilometers Driven")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ANALYSIS ----------
elif page == "📊 Market Analytics":
    st.title("Market Analytics Dashboard")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # Filters
    fuel_options = ["All"] + list(df["fuel"].unique())
    fuel_filter = st.selectbox("Filter by Fuel", fuel_options)
    
    if fuel_filter == "All":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["fuel"] == fuel_filter]
    
    # Custom plotly template for dark mode
    plotly_template = "plotly_dark"

    # ================================
    # 📊 SECTION 1: MARKET TRENDS
    # ================================
    st.subheader("Price Trend Over Years")
    trend_df = filtered_df.groupby("year")["selling_price"].mean().reset_index()
    fig1 = px.line(trend_df, x="year", y="selling_price", markers=True, title=f"Average Price Trend ({fuel_filter})", template=plotly_template, color_discrete_sequence=["#38bdf8"])
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Insight: Car prices generally increase for newer models.")

    st.subheader("Number of Cars by Year")
    year_count = filtered_df["year"].value_counts().sort_index().reset_index()
    year_count.columns = ["year", "count"]
    fig2 = px.area(year_count, x="year", y="count", title="Market Supply by Year", template=plotly_template, color_discrete_sequence=["#6366f1"])
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Insight: Shows market supply trends over years.")

    # ================================
    # 📊 SECTION 2: PRICE FACTORS
    # ================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price by Owner Type")
        # Remove Test Drive Car and enforce logical sequence
        owner_df = filtered_df[filtered_df["owner"] != "Test Drive Car"]
        owner_price = owner_df.groupby("owner")["selling_price"].mean().reset_index()
        
        owner_order = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"]
        
        fig3 = px.bar(owner_price, x="owner", y="selling_price", color="owner", 
                      template=plotly_template, title="Average Price by Owner",
                      category_orders={"owner": owner_order})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("Transmission Impact")
        trans_price = filtered_df.groupby("transmission")["selling_price"].mean().reset_index()
        fig4 = px.pie(trans_price, names="transmission", values="selling_price", template=plotly_template, title="Price Distribution by Transmission", hole=0.4)
        st.plotly_chart(fig4, use_container_width=True)

    # ================================
    # 📊 SECTION 3: USAGE IMPACT
    # ================================
    st.subheader("Price vs Kilometers Driven")
    fig5 = px.scatter(filtered_df, x="km_driven", y="selling_price", color="transmission", opacity=0.6, template=plotly_template, title="Impact of Kilometers Driven on Price")
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("Insight: Higher kilometers driven reduces resale value.")

    # ================================
    # 📊 SECTION 4: MARKET INSIGHTS
    # ================================
    st.subheader("Top Brands by Listings")
    brand_count = filtered_df["brand"].value_counts().head(10).reset_index()
    brand_count.columns = ["brand", "count"]
    fig6 = px.bar(brand_count, x="brand", y="count", template=plotly_template, title="Most Popular Brands", color="count", color_continuous_scale="Blues")
    st.plotly_chart(fig6, use_container_width=True)

    # --- MARKET INSIGHTS MERGED HERE ---
    st.markdown("---")
    st.markdown("### Real Insights from the Market")
    
    # Dynamic calculations for Insights
    avg_petrol = df[df["fuel"] == "Petrol"]["selling_price"].mean()
    avg_diesel = df[df["fuel"] == "Diesel"]["selling_price"].mean()
    
    if pd.isna(avg_petrol) or pd.isna(avg_diesel) or min(avg_petrol, avg_diesel) == 0:
        fuel_diff = 0
        pricier_fuel = "Unknown"
    else:
        fuel_diff = abs(avg_diesel - avg_petrol) / min(avg_petrol, avg_diesel) * 100
        pricier_fuel = "Diesel" if avg_diesel > avg_petrol else "Petrol"
    
    avg_manual = df[df["transmission"] == "Manual"]["selling_price"].mean()
    avg_auto = df[df["transmission"] == "Automatic"]["selling_price"].mean()
    if pd.isna(avg_manual) or pd.isna(avg_auto) or avg_manual == 0:
        trans_diff = 0
    else:
        trans_diff = abs(avg_auto - avg_manual) / avg_manual * 100
    
    # FIX: Use actual max year in dataset instead of datetime.now() because the dataset is older
    max_year = df["year"].max()
    recent_cars = df[df["year"] >= max_year - 2]["selling_price"].mean()
    old_cars = df[df["year"] <= max_year - 10]["selling_price"].mean()
    
    recent_cars = 0 if pd.isna(recent_cars) else recent_cars

    # ==========================================
    # 🤖 SECTION 5: AI MODEL INSIGHTS (Feature Importances)
    # ==========================================
    st.markdown("---")
    st.subheader("🤖 AI Decision Intelligence")
    st.markdown("<p style='color:#94a3b8;'>Understanding how the AI Model weights different car features to estimate price.</p>", unsafe_allow_html=True)
    
    try:
        fi_response = requests.get(f"{API_URL}/feature_importances")
        if fi_response.status_code == 200:
            fi_data = fi_response.json()
            if "features" in fi_data:
                # Prepare data for plotting
                fi_df = pd.DataFrame({
                    "Feature": fi_data["features"],
                    "Importance": fi_data["importances"]
                }).sort_values("Importance", ascending=False).head(10) # Top 10 factors
                
                # Plot
                fig_fi = px.bar(
                    fi_df, 
                    x="Importance", 
                    y="Feature", 
                    orientation='h',
                    template=plotly_template,
                    title="Top 10 Price Determinants (AI Insights)",
                    color="Importance",
                    color_continuous_scale="Viridis"
                )
                fig_fi.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_fi, use_container_width=True)
                st.caption("Insight: This chart shows which features (Age, Kilometers, Brand, etc.) most influenced the AI's valuation logic.")
            else:
                st.info("Feature importance data is currently being calibrated.")
        else:
            st.info("AI Model telemetry is only available when the Backend API is active.")
    except:
        st.info("Connect to the live CarVal Engine to see AI decision transparency.")
    old_cars = 0 if pd.isna(old_cars) else old_cars
    
    col1, col2 = st.columns(2)
    with col1:
        if pricier_fuel != "Unknown":
            st.info(f"**Fuel Value:** {pricier_fuel} cars are generally **{fuel_diff:.0f}%** more expensive on average than their counterparts.")
        else:
            st.info("**Fuel Value:** Not enough data to compare fuel types.")
            
        if trans_diff > 0:
            st.info(f"**Transmission Premium:** Automatic cars command a **{trans_diff:.0f}%** premium over manual cars in the used market.")
        else:
            st.info("**Transmission Premium:** Not enough data to compare transmissions.")
            
    with col2:
        if old_cars > 0 and recent_cars > 0:
            st.warning(f"**Depreciation:** Cars older than 10 years cost on average **₹{old_cars:,.0f}**, compared to **₹{recent_cars:,.0f}** for cars under 2 years old.")
        else:
            st.warning("**Depreciation:** Need more year spread data for depreciation insights.")
            
        st.success(f"**Kilometers Driven:** For every additional 10,000 km driven, prices generally drop significantly across all segments.")

    # Feature Importance fetched from API
    try:
        res = requests.get(f"{API_URL}/feature_importances")
        data = res.json()
        if "features" in data and "importances" in data:
            st.markdown("### AI Feature Importance")
            st.write("What factors does our AI consider most important when predicting price?")
            
            # ==========================================
            # 🧠 EXPLAINABLE AI (XAI)
            # The AI model treats "Fuel_Petrol" and "Fuel_Diesel" as separate math variables.
            # This loop cleverly groups them back together so the chart shows the overall
            # importance of "Fuel" to human users.
            # ==========================================
            feature_dict = {}
            for i, f in enumerate(data["features"]):
                # Remove ugly technical prefixes added by the Machine Learning pipeline
                clean_f = f.replace('cat__', '').replace('num__', '')
                base_f = clean_f.split('_')[0].title()
                
                # Rename to human-readable labels
                if base_f == "Km": base_f = "Kilometers Driven"
                if base_f == "Car": base_f = "Car Age"
                if base_f == "Seller": base_f = "Seller Type"
                
                # Add up the importance scores for the group
                if base_f not in feature_dict:
                    feature_dict[base_f] = 0
                feature_dict[base_f] += data["importances"][i]
                
            imp_df = pd.DataFrame({
                "Feature": list(feature_dict.keys()), 
                "Importance": list(feature_dict.values())
            }).sort_values("Importance", ascending=False).head(5)
            
            fig = px.bar(imp_df, x="Importance", y="Feature", orientation='h', template="plotly_dark")
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        pass

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- COMPARE ----------

elif page == "⚖️ Vehicle Comparison":

    st.markdown("<h1 style='text-align:center;'>Vehicle Comparison</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Compare two cars using AI predictions</p>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # -------- CAR 1 --------
    with col1:
        st.subheader("Vehicle 1")

        brand1 = st.selectbox("Brand 1", sorted(df["name"].str.split().str[0].unique()), key="b1")
        models_list1 = df[df["brand"] == brand1]["model"].unique()
        if len(models_list1) == 0:
          models_list1 = df["model"].dropna().unique()
        model1 = st.selectbox("Model 1", sorted(models_list1), key="m1")
        year1 = st.slider("Year of Manufacture 1", 1990, datetime.now().year, 2018, step=1, key="y1")
        km1 = st.slider("Kilometers Driven 1", 0, 500000, 30000, step=5000, key="k1")
        fuel1 = st.selectbox("Fuel 1", ["Petrol", "Diesel", "CNG", "LPG", "Electric"], key="f1")
        trans1 = st.selectbox("Transmission 1", ["Manual", "Automatic"], key="t1")

    # -------- CAR 2 --------
    with col2:
        st.subheader("Vehicle 2")

        brand2 = st.selectbox("Brand 2", sorted(df["name"].str.split().str[0].unique()), key="b2")
        models_list2 = df[df["brand"] == brand2]["model"].unique()
        if len(models_list2) == 0:
          models_list2 = df["model"].dropna().unique()
        model2 = st.selectbox("Model 2", sorted(models_list2), key="m2")
        year2 = st.slider("Year of Manufacture 2", 1990, datetime.now().year, 2020, step=1, key="y2")
        km2 = st.slider("Kilometers Driven 2", 0, 500000, 20000, step=5000, key="k2")
        fuel2 = st.selectbox("Fuel 2", ["Petrol", "Diesel", "CNG", "LPG", "Electric"], key="f2")
        trans2 = st.selectbox("Transmission 2", ["Manual", "Automatic"], key="t2")

    if st.button("Run Comparison"):

        # Prepare API payloads
        payload1 = {
            "brand": brand1, "model": model1, "year": year1, "km_driven": km1,
            "fuel": fuel1, "transmission": trans1, "seller_type": "Individual", "owner": "First Owner"
        }
        payload2 = {
            "brand": brand2, "model": model2, "year": year2, "km_driven": km2,
            "fuel": fuel2, "transmission": trans2, "seller_type": "Individual", "owner": "First Owner"
        }

        try:
            res1 = requests.post(f"{API_URL}/predict", json=payload1)
            res2 = requests.post(f"{API_URL}/predict", json=payload2)
            price1 = res1.json().get("predicted_price", 0)
            price2 = res2.json().get("predicted_price", 0)
        except Exception as e:
            st.error(f"Backend API Error: {e}")
            price1, price2 = 0, 0

        # Show results
        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"<div class='result-box'>₹{price1:,.0f}</div>", unsafe_allow_html=True)

        with c2:
            st.markdown(f"<div class='result-box'>₹{price2:,.0f}</div>", unsafe_allow_html=True)

        # Winner Logic
        if price1 > price2:
            st.success(f" {brand1} {model1} has higher market value")
        elif price2 > price1:
            st.success(f" {brand2} {model2} has higher market value")
        else:
            st.info("Both cars have equal value")

        # Chart
        chart_df = pd.DataFrame({
            "Car": [f"{brand1} {model1}", f"{brand2} {model2}"],
            "Price": [price1, price2]
        })
        
        fig = px.bar(chart_df, x="Car", y="Price", text="Price", color="Car", template="plotly_dark", title="Value Comparison")
        fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ADMIN DASHBOARD ----------
elif page == "🛡️ Admin Portal":
    st.markdown("<h1 style='text-align:center;'>Admin Analytics Portal</h1>", unsafe_allow_html=True)
    
    # Clean and simple Admin Authentication
    admin_col1, admin_col2, admin_col3 = st.columns([1, 2, 1])
    with admin_col2:
        st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
        st.write("### Secure Access")
        admin_password = st.text_input("Enter Admin Password:", type="password", help="Default is 'admin123'")
        st.markdown("</div>", unsafe_allow_html=True)

    if admin_password == "admin123":
        st.markdown("<p style='text-align:center; color:#38bdf8;'>Live telemetry of user searches from SQLite Database</p>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Fetch logs from Backend API
        try:
            response = requests.get(f"{API_URL}/logs")
            response.raise_for_status()
            logs = response.json()
        except Exception as e:
            st.error(f"Backend API Error: Unable to fetch telemetry. Details: {e}")
            logs = []
    
        if len(logs) == 0:
            st.info("No predictions logged yet. Try making some predictions in the 'Predict Price' tab!")
        else:
            logs_df = pd.DataFrame(logs)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Total Predictions Made")
                st.markdown(f"<div class='result-box'>{len(logs)}</div>", unsafe_allow_html=True)
                
            with col2:
                st.subheader("Average Predicted Value")
                avg_val = logs_df['predicted_price'].mean()
                st.markdown(f"<div class='result-box'>₹ {avg_val:,.0f}</div>", unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            col3, col4 = st.columns(2)
            with col3:
                st.subheader("Most Searched Brands")
                brand_counts = logs_df['brand'].value_counts().reset_index()
                brand_counts.columns = ['brand', 'count']
                fig_brands = px.bar(brand_counts.head(5), x='brand', y='count', template="plotly_dark")
                st.plotly_chart(fig_brands, use_container_width=True)
                
            with col4:
                st.subheader("Fuel Type Preference")
                fuel_counts = logs_df['fuel'].value_counts().reset_index()
                fuel_counts.columns = ['fuel', 'count']
                fig_fuel = px.pie(fuel_counts, names='fuel', values='count', template="plotly_dark", hole=0.4)
                st.plotly_chart(fig_fuel, use_container_width=True)
                
            st.subheader("Raw Telemetry Data")
            st.dataframe(logs_df, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)