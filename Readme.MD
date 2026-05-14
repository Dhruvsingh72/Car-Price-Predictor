# CarVal: Intelligent Car Valuation System 🚗⚡

**CarVal** is a high-performance, industry-standard car price prediction and market analytics platform. Built for a final-year BCA project, it demonstrates a modern decoupled architecture using **FastAPI** for the backend and **Streamlit** for a premium user experience.

---

## 🏗️ Technical Architecture

The project is structured using a **Three-Tier Architecture**:

1.  **Backend (FastAPI)**: A high-performance REST API that serves the Machine Learning model. It handles data preprocessing, prediction logic, and interaction with the database.
2.  **Frontend (Streamlit)**: A premium "Glassmorphism" styled dashboard that interacts with the API. It provides a dynamic, responsive UI for car valuation and market insights.
3.  **Database (SQLite)**: A local relational database that logs every user prediction in real-time, enabling live telemetry and market trend analysis in the Admin Portal.

---

## 🚀 Key Features

-   **⚡ AI Price Prediction**: Uses a tuned **Random Forest** model to estimate car value with high precision based on 8+ parameters.
-   **📊 Market Analytics**: Interactive Plotly-powered charts showing price trends, supply distributions, and fuel-type preferences.
-   **🔍 Find My Car**: An AI-driven recommendation engine that suggests vehicles based on user budget and preferences.
-   **⚖️ Vehicle Comparison**: Side-by-side market value comparison between two different car models.
-   **🛡️ Admin Portal**: A secure dashboard for administrators to view live search telemetry and system usage statistics.
-   **📄 Official PDF Certificates**: Generate and download professional valuation reports for any car.

---

## 🛠️ Tech Stack

-   **Model**: Random Forest Regressor (Scikit-Learn)
-   **Backend**: FastAPI, Uvicorn, Pydantic
-   **Frontend**: Streamlit, Plotly (Data Viz), Custom CSS
-   **Database**: SQLite3
-   **Documentation**: FPDF2

---

## 💻 Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/car-price-predictor.git
cd car-price-predictor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You need to run **two** terminal windows:

**Window 1: Start the API**
```bash
uvicorn api:app --reload
```

**Window 2: Start the UI**
```bash
streamlit run app.py
```

---

## 🌐 Cloud Deployment (Render.com)

This project is configured for dynamic cloud deployment.

1.  **API Deployment**: Deploy `api.py` as a Web Service. Set the start command to:
    `uvicorn api:app --host 0.0.0.0 --port $PORT`
2.  **UI Deployment**: Deploy `app.py` as a Web Service.
    - Set start command to: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
    - Add an **Environment Variable** named `API_URL` with the value of your deployed API URL.

---

## 📈 Model Performance
The Random Forest model was selected for its robustness against non-linear depreciation patterns and outliers, achieving an **R² score of ~0.80** on the test dataset.

---
**Developed as a Final Year Project for BCA.**
