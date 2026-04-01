import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SOP Düzenleyici", layout="wide")
st.title("🏭 Profesyonel SOP Formatlayıcı")

# Sol tarafta API Key girişi
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Görseli Yükle")
        uploaded_file = st.file_uploader("İşlem fotoğrafı seç...", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file, caption='Referans Görsel')

    with col2:
        st.subheader("2. Adımları Yaz")
        user_steps = st.text_area("Buraya adımları alt alta yaz (Örn: 1. Kabloyu tak 2. Butona bas)", height=200)
        
        if st.button("Profesyonel SOP Tablosuna Dönüştür"):
            if user_steps:
                with st.spinner('Tablo oluşturuluyor...'):
                    prompt = f"""Aşağıdaki operasyon adımlarını profesyonel bir endüstriyel SOP tablosuna dönüştür. 
                    Adımlar: {user_steps}
                    Format: (Adım No | İşlem | Detaylı Açıklama | İSG/Risk Notu) içeren şık bir markdown tablosu yap."""
                    
                    response = model.generate_content(prompt)
                    st.success("SOP Tablosu Hazır!")
                    st.markdown(response.text)
            else:
                st.warning("Lütfen önce adımları yazın.")
else:
    st.info("Lütfen soldaki menüden API anahtarını girin.")
