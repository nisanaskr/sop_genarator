import streamlit as st
import google.generativeai as genai

# Sayfa ayarları
st.set_page_config(page_title="SOP Oluşturucu", layout="wide")
st.title("🏭 Profesyonel SOP Formatlayıcı")

# Sol menüden API Key alalım
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Model ismini en güncel ve stabil olanla değiştirdik
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("1. Referans Görsel")
            uploaded_file = st.file_uploader("Operasyon fotoğrafını yükle...", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, use_column_width=True)

        with col2:
            st.subheader("2. Operasyon Detayları")
            user_input = st.text_area("Adımları buraya yazın...", height=250, placeholder="Örn: 1. Parçayı hatta yerleştir. 2. Sensörün okumasını bekle.")
            
            if st.button("SOP Tablosunu Oluştur"):
                if user_input:
                    with st.spinner('SOP hazırlanıyor...'):
                        # Senin Canvas'taki o meşhur profesyonel komutun:
                        prompt = f"""Bir Endüstri Mühendisi gibi davranarak aşağıdaki adımları profesyonel bir SOP (Standart Operasyon Prosedürü) tablosuna dönüştür.
                        Girdi adımları: {user_input}
                        
                        Tablo şunları içermeli:
                        - Adım No
                        - Operasyon Adımı
                        - Uygulama Detayı (Profesyonelce genişletilmiş)
                        - İSG ve Kalite Kritik Noktaları
                        
                        Dilin teknik ve net olsun."""
                        
                        response = model.generate_content(prompt)
                        st.success("İşlem Tamamlandı!")
                        st.markdown(response.text)
                else:
                    st.error("Lütfen önce operasyon adımlarını yazın!")
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Lütfen soldaki menüden Gemini API anahtarını girin.")
