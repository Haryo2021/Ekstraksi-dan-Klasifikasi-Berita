import streamlit as st

def render_header():
    with st.expander("⚠️⚠️⚠️⚠️⚠️⚠️ PERINGATAN!!! ⚠️⚠️⚠️⚠️⚠️⚠️"):
        st.markdown(
            """
            <div style="text-align: center;">
                <p style="font-size:18px; font-weight:600;">
                Untuk mode link pada aplikasi ini saat ini hanya mendukung pengambilan artikel dari
                <br><b>Tempo, Detik, dan Kompas</b>.
                </p>
                <p style="font-size:18px; font-weight:600;">
                Artikel dari media lain akan segera di-update.
                </p>
                <p style="font-size:18px; font-weight:600;">
                Untuk Mode manual bisa digunakan untuk semua artikel berita.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
