# 👗 AI-Driven Cross-Brand Fashion Fit & Outfit Recommendation System

Personalized, cross-brand outfit and size-fit recommendations using **Generative AI** and an interactive **Streamlit dashboard**.

---

## 🧠 Application Overview

This application is a **Generative AI–powered fashion recommendation system** that helps users:

* Get **personalized outfit suggestions**
* Handle **size and fit variations across different brands**
* Compare brand-specific sizing visually
* Generate **AI-based outfit descriptions and images** based on occasion, weather, and preferences

The system is designed as a **guided onboarding experience** followed by a **multi-tab dashboard**, making it suitable for real-world fashion retail use cases as well as academic evaluation.

---

## ⚙️ How the App Works (Flow)

1. User logs in or uses demo mode
2. Step-by-step onboarding collects:

   * Personal details
   * Body measurements
   * Style preferences
   * Preferred brands
   * Occasion & weather
3. System calculates **cross-brand size recommendations**
4. Generative AI creates:

   * Detailed outfit text
   * AI-generated outfit image
5. Results are shown in a Streamlit dashboard with history and insights

---

## ▶️ How to Run the Application (Streamlit)

### ✅ Prerequisites

* Python **3.8 or above**
* Internet connection (for OpenAI API)
* OpenAI API key

### 📦 Required Libraries

Install all required dependencies using:

```bash
pip install streamlit openai pillow pandas plotly
```

### ▶️ Run the App

```bash
streamlit run app.py
```

The app will open automatically in your browser.

---

## 🧠 Core Technologies Used

* **Frontend:** Streamlit
* **Language:** Python
* **AI Models:**

  * GPT-4o-mini (text-based outfit generation)
  * GPT Image Model (outfit visualization)
* **Visualization:** Plotly
* **State Management:** Streamlit Session State

---

## 🧩 Key Functional Modules

### 👤 User Onboarding

* Multi-step guided form
* Personal info, body measurements, style & brand preferences

### 📏 Cross-Brand Size Intelligence

* Brand-specific size charts
* Automatic size mapping based on height
* Visual size comparison using bar charts

### 👗 Generative AI Outfit Engine

* Prompt-based outfit generation
* Occasion & weather-aware styling
* AI-generated fashion images

### 📊 Interactive Dashboard Tabs

* Quick Outfit Generator
* Outfit History
* Brand Size Table
* Size Comparison Chart
* User Profile Viewer

---

## 🖼️ Application Screenshots

### 🏠 Home & User Input Dashboard

<img src="ss_fashionapp/Screenshot 2025-12-01 160625.png" width="900"/>

### 👗 Outfit Recommendation Results
<img src="ss_fashionapp/Screenshot 2025-12-01 161303.png" width="900"/>


### 📊 Brand Comparison & Fit Insights
<img src="ss_fashionapp/Screenshot 2025-12-01 160756.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 160809.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 160858.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 160921.png" width="900"/>

### ⚙️ Additional Features & UI Flow

<img src="ss_fashionapp/Screenshot 2025-12-01 160947.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 161001.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 161212.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 161231.png" width="900"/>
<img src="ss_fashionapp/Screenshot 2025-12-01 161251.png" width="900"/>

---

## 🔐 Privacy & Ethics

* No permanent user data storage
* Session-based personalization only
* API key managed locally by user
* Designed for non-sensitive fashion recommendations

---

## 🌱 Future Enhancements

* Image-based user input for outfit matching
* Body-measurement prediction using ML
* User accounts & cloud storage
* E-commerce platform integration
* Trend and seasonal analytics

---

## 👨‍💻 Author

**Pranjal Nilesh Belalekar**
MCA Student | AI & Data Science Enthusiast

---

## 📜 License

This project is licensed under the **MIT License**.

---

⭐ If you find this project useful, consider starring the repository!
