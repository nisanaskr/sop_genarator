import streamlit as st
import google.generativeai as genai

# Arayüz Ayarları
st.set_page_config(page_title="Fabrika SOP Oluşturucu", layout="wide")
st.title("🏭 Akıllı SOP Oluşturma Portalı")
st.markdown("Görseli yükleyin, operatör talimatını saniyeler içinde alın.")

# API Key Girişi (Bunu arkadaşlarına vermene gerek kalmayacak, sisteme gömeceğiz)
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("Bir operasyon fotoğrafı yükleyin...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        st.image(uploaded_file, caption='Yüklenen Görsel', use_column_width=True)
        
        if st.button("SOP Oluştur"):
            with st.spinner('Analiz ediliyor...'):
                img = genai.Image.load_from_bytes(uploaded_file.getvalue())
                prompt = "Bu görseldeki işlemi analiz et ve (Adım No | İşlem | Açıklama | Risk) içeren profesyonel bir SOP tablosu oluştur."
                response = model.generate_content([prompt, img])
                st.success("SOP Hazır!")
                st.markdown(response.text)
else:
    st.info("Lütfen soldaki menüden API anahtarını girin.")
