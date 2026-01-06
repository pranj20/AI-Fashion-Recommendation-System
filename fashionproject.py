import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import plotly.express as px
from datetime import datetime

#OpenAI 
client = OpenAI(api_key="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")

 
BRAND_DATABASE = {
    "Zara": {"category": "Fast Fashion", "price_range": "$$", "style": "Trendy, European", "fit": "slim"},
    "H&M": {"category": "Fast Fashion", "price_range": "$", "style": "Affordable, Basic", "fit": "true_to_size"},
    "Uniqlo": {"category": "Fast Fashion", "price_range": "$", "style": "Minimal, Japanese", "fit": "asian"},
    "Gucci": {"category": "Luxury", "price_range": "$$$$$", "style": "Luxury, High-Fashion", "fit": "luxury"},
    "Louis Vuitton": {"category": "Luxury", "price_range": "$$$$$", "style": "Luxury, Heritage", "fit": "luxury"},
    "Nike": {"category": "Sportswear", "price_range": "$$", "style": "Sporty, Athletic", "fit": "athletic"},
    "Adidas": {"category": "Sportswear", "price_range": "$$", "style": "Sporty, Streetwear", "fit": "athletic"},
    "Lululemon": {"category": "Sportswear", "price_range": "$$$", "style": "Athletic, Premium", "fit": "athletic"},
    "Levi's": {"category": "Denim", "price_range": "$$", "style": "Classic, Denim", "fit": "true_to_size"},
    "Aritzia": {"category": "Contemporary", "price_range": "$$$", "style": "Minimal, Chic", "fit": "true_to_size"},
}

#Brand-specific Size Charts
BRAND_SIZE_CHARTS = {
    "Zara": {"XS": (0, 158), "S": (158, 165), "M": (165, 172), "L": (172, 180), "XL": (180, 190)},
    "H&M": {"XS": (0, 160), "S": (160, 165), "M": (165, 170), "L": (170, 175), "XL": (175, 180)},
    "Uniqlo": {"XS": (0, 157), "S": (157, 163), "M": (163, 170), "L": (170, 177), "XL": (177, 185)},
    "Gucci": {"XS": (0, 158), "S": (158, 164), "M": (164, 170), "L": (170, 176), "XL": (176, 182)},
    "Louis Vuitton": {"XS": (0, 158), "S": (158, 163), "M": (163, 168), "L": (168, 173), "XL": (173, 178)},
    "Nike": {"XS": (0, 160), "S": (160, 167), "M": (167, 174), "L": (174, 181), "XL": (181, 188)},
    "Adidas": {"XS": (0, 160), "S": (160, 167), "M": (167, 174), "L": (174, 181), "XL": (181, 188)},
    "Lululemon": {"XS": (0, 155), "S": (155, 160), "M": (160, 165), "L": (165, 170), "XL": (170, 175)},
    "Levi's": {"XS": (0, 160), "S": (160, 167), "M": (167, 174), "L": (174, 181), "XL": (181, 188)},
    "Aritzia": {"XS": (0, 158), "S": (158, 164), "M": (164, 170), "L": (170, 176), "XL": (176, 182)},
}


def init_state():
    if 'user' not in st.session_state: st.session_state.user = None
    if 'onboarding_step' not in st.session_state: st.session_state.onboarding_step = 0
    if 'user_profile' not in st.session_state: st.session_state.user_profile = {}
    if 'fashion_history' not in st.session_state: st.session_state.fashion_history = {}
    if 'current_outfit' not in st.session_state: st.session_state.current_outfit = None

init_state()


def next_step(): st.session_state.onboarding_step += 1
def previous_step(): st.session_state.onboarding_step -= 1


def generate_outfit(profile, occasion, weather, colors):
    prompt = f"""
    Create a detailed fashion outfit recommendation for a user with the following profile:
    {profile}
    Occasion: {occasion}, Weather: {weather}, Favorite colors: {colors}.
    Include outfit breakdown, brands, size guidance, styling tips, and budget considerations.
    """
    try:
        # --- Generate Outfit Text ---
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        outfit_text = response.choices[0].message.content.strip()

        # --- Generate Outfit Image ---
        img_prompt = f"A realistic fashion outfit based on: {outfit_text}"
        img_response = client.images.generate(
            model="gpt-image-1",
            prompt=img_prompt,
            size="1024x1024"
        )

        # Decode base64 image
        img_b64 = img_response.data[0].b64_json
        img = Image.open(BytesIO(base64.b64decode(img_b64)))

        return {"text": outfit_text, "image": img}

    except Exception as e:
        return {"text": f"Error generating outfit: {str(e)}", "image": None}


def calculate_sizes(height, weight, gender, body_type):
    brand_sizes = {}
    for brand, chart in BRAND_SIZE_CHARTS.items():
        assigned = False
        for size, (min_h, max_h) in chart.items():
            if min_h <= height <= max_h:
                brand_sizes[brand] = size
                assigned = True
                break
        if not assigned:
            brand_sizes[brand] = "M"
    return brand_sizes


def show_login():
    st.title("👗 FashionAI Pro")
    st.markdown("Sign in to your account or try the demo")
    col1,col2 = st.columns([2,2])
    with col1:
        st.subheader("Sign In")
        email = st.text_input("Enter Email")
        if st.button("Sign In"):
            if email.strip():
                st.session_state.user = {"name": email}
                if email not in st.session_state.fashion_history:
                    st.session_state.fashion_history[email] = []
                st.session_state.onboarding_step = 1
                st.rerun()
    with col2:
        st.subheader("Demo Login")
        if st.button("Demo Login"):
            st.session_state.user = {"name": "Demo User"}
            if "Demo User" not in st.session_state.fashion_history:
                st.session_state.fashion_history["Demo User"] = []
            st.session_state.onboarding_step = 1
            st.rerun()

def show_onboarding():
    step = st.session_state.onboarding_step
    st.progress((step/6))
    if step ==1: step_personal_info()
    elif step==2: step_body_measurements()
    elif step==3: step_style_preferences()
    elif step==4: step_brand_selection()
    elif step==5: step_occasion_setup()
    elif step==6: step_complete_profile()


def step_personal_info():
    st.subheader("👤 Personal Info")
    with st.form("personal_info"):
        name = st.text_input("Name", value=st.session_state.user.get('name',''))
        gender = st.radio("Gender", ["Women","Men","Non-binary"])
        age_group = st.selectbox("Age Group", ["18-24","25-34","35-44","45+"])
        if st.form_submit_button("Next"):
            st.session_state.user_profile.update({'name':name,'gender':gender,'age_group':age_group})
            next_step()
            st.rerun()

def step_body_measurements():
    st.subheader("📏 Body Measurements")
    with st.form("body_measurements"):
        height = st.number_input("Height (cm)",140,220,165)
        weight = st.number_input("Weight (kg)",40,150,60)
        body_type = st.selectbox("Body Type", ["Hourglass","Pear","Apple","Rectangle"])
        if st.form_submit_button("Next"):
            st.session_state.user_profile.update({'height':height,'weight':weight,'body_type':body_type})
            st.session_state.user_profile['brand_sizes'] = calculate_sizes(height, weight, st.session_state.user_profile['gender'], body_type)
            next_step()
            st.rerun()

def step_style_preferences():
    st.subheader("🎨 Style Preferences")
    with st.form("style_preferences"):
        style = st.selectbox("Primary Style", ["Minimal","Classic","Trendy","Streetwear"])
        colors = st.multiselect("Favorite Colors", ["Black","White","Blue","Red"], default=["Black","Blue"])
        budget = st.select_slider("Budget", ["Budget-Friendly","Moderate","Premium"], value="Moderate")
        if st.form_submit_button("Next"):
            st.session_state.user_profile.update({'style_preference': style,'favorite_colors': colors,'budget': budget})
            next_step()
            st.rerun()

def step_brand_selection():
    st.subheader("🏪 Brand Selection")
    brands = list(BRAND_DATABASE.keys())
    selected = st.multiselect("Select Your Favorite Brands", brands)
    if st.button("Next"):
        st.session_state.user_profile['preferred_brands'] = selected
        next_step()
        st.rerun()

def step_occasion_setup():
    st.subheader("🎯 Occasion Setup")
    with st.form("occasion_setup"):
        occasion = st.selectbox("Main Occasion", ["Work","Casual","Date Night"])
        weather = st.selectbox("Weather", ["Sunny","Cold","Rainy"])
        if st.form_submit_button("Next"):
            st.session_state.user_profile.update({'main_occasion': occasion,'weather': weather})
            next_step()
            st.rerun()

def step_complete_profile():
    st.success("🎉 Profile Complete!")
    if st.button("Generate Outfit"):
        outfit = generate_outfit(
            st.session_state.user_profile,
            st.session_state.user_profile.get('main_occasion'),
            st.session_state.user_profile.get('weather'),
            st.session_state.user_profile.get('favorite_colors',[])
        )
        st.session_state.current_outfit = outfit
        user_key = st.session_state.user.get('name')
        st.session_state.fashion_history[user_key].append({
            'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M"),
            'outfit': outfit['text']
        })
        next_step()
        st.rerun()

# --- Dashboard ---
def show_dashboard():
    st.subheader(f"👋 Welcome, {st.session_state.user.get('name')}")
    tabs = st.tabs(["Quick Outfit","History","Brand Sizes","Size Chart","Profile"])
    with tabs[0]: dashboard_quick_outfit()
    with tabs[1]: dashboard_history()
    with tabs[2]: dashboard_brand_sizes()
    with tabs[3]: dashboard_size_chart()
    with tabs[4]: dashboard_profile()

def dashboard_quick_outfit():
    st.markdown("### Generate a New Outfit")
    cols = st.columns(2)
    occasion = cols[0].selectbox("Occasion", ["Work","Casual","Date Night"])
    weather = cols[1].selectbox("Weather", ["Sunny","Cold","Rainy"])
    if st.button("Generate Outfit"):
        outfit = generate_outfit(st.session_state.user_profile, occasion, weather, st.session_state.user_profile.get('favorite_colors',[]))
        st.session_state.current_outfit = outfit
        user_key = st.session_state.user.get('name')
        st.session_state.fashion_history[user_key].append({
            'timestamp':datetime.now().strftime("%Y-%m-%d %H:%M"),
            'outfit': outfit['text']
        })
        st.success("✨ Outfit Generated!")
    if st.session_state.current_outfit:
        st.info(st.session_state.current_outfit['text'])
        if st.session_state.current_outfit.get('image'):
            st.image(st.session_state.current_outfit['image'], caption="Generated Outfit", use_column_width=True)

def dashboard_history():
    st.markdown("### Outfit History")
    user_key = st.session_state.user.get('name')
    history = st.session_state.fashion_history.get(user_key, [])
    if not history:
        st.info("No outfit history yet")
        return
    if st.button("Delete History"):
        st.session_state.fashion_history[user_key] = []
        st.success("History Deleted")
    for h in reversed(history):
        st.markdown(f"**{h['timestamp']}**: {h['outfit']}")

def dashboard_brand_sizes():
    st.markdown("### Recommended Brand Sizes")
    brand_sizes = st.session_state.user_profile.get('brand_sizes', {})
    if not brand_sizes:
        st.info("Sizes will appear after onboarding")
        return
    df = pd.DataFrame([{'Brand':b,'Recommended Size':s} for b,s in brand_sizes.items() if b in st.session_state.user_profile.get('preferred_brands',[])] )
    st.table(df)

def dashboard_size_chart():
    st.markdown("### Cross-Brand Size Comparison")
    brand_sizes = st.session_state.user_profile.get('brand_sizes', {})
    if not brand_sizes:
        st.info("Size chart will appear after onboarding")
        return
    df = pd.DataFrame([{"Brand": b, "Size": s} for b,s in brand_sizes.items() if b in st.session_state.user_profile.get('preferred_brands',[])] )
    size_map = {'XS':1,'S':2,'M':3,'L':4,'XL':5,'XXL':6}
    df['SizeValue'] = df['Size'].map(size_map)
    fig = px.bar(df, x='Brand', y='SizeValue', text='Size',
                 color='Size', color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(yaxis=dict(title="Size"), xaxis=dict(title="Brand"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def dashboard_profile():
    st.markdown("### Your Profile")
    profile = st.session_state.user_profile
    st.json(profile)


if __name__=="__main__":
    st.set_page_config(page_title="FashionAI Pro", layout="wide")
    if not st.session_state.user: 
        show_login()
    else:
        if st.session_state.onboarding_step<7: 
            show_onboarding()
        else: 
            show_dashboard()
