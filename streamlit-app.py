import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# --- Functions to make the code cleaner ---

def load_data(url):
    """Loads data from a remote Excel file."""
    try:
        return pd.read_excel(url)
    except Exception as e:
        st.error(f"Error loading data file: {e}")
        return pd.DataFrame() # Return empty dataframe on error

def load_image_from_url(url):
    """Loads an image from a URL and returns a PIL Image object."""
    try:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.warning(f"Failed to retrieve image. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error loading image from URL: {e}")
        return None

# --- Main App Logic ---

# Path to the Excel file from GitHub
file_path = "https://github.com/zenklinov/MLBB_PredictionWR/raw/main/Data_MPL.xlsx"

# Page configuration
st.set_page_config(
    page_title="Matana University - MLBB Win Prediction",
    page_icon="👋",
    layout="wide"
)

# --- Header Section ---
# Updated and verified image URL for Matana University Logo
logo_url = "https://matanauniversity.ac.id/wp-content/uploads/2022/09/Logo-Matana-University-1.png"
logo_img = load_image_from_url(logo_url)

if logo_img:
    st.image(logo_img, width=300) # Set a more controlled width

st.title("Matana University")
st.markdown(
    """
    Selamat datang di Matana University! Bergabunglah dengan program studi Statistika kami, di mana lulusan kami telah sukses di ruang lingkup pemerintahan maupun swasta, di berbagai sektor seperti ekonomi, kebumian, agrikultur, kesehatan, informatika, dll. 
    
    Anda juga dapat menjadi ahli dalam analisis data seperti dalam game Mobile Legends! Dengan kurikulum inovatif dan praktik langsung, Anda akan mempelajari cara mengolah serta menganalisis data untuk meningkatkan strategi permainan. Raih peluang karier menarik di industri game dan buktikan bahwa angka adalah senjata utama Anda!
    """
)

st.divider()

# --- MLBB Prediction Section ---
st.title("Mobile Legends Win Prediction")

# Video display
st.video("https://www.youtube.com/watch?v=wvtdrKZeLZ4")

st.markdown(
    """
    *Source Video: [akmj.mp4 on YouTube](https://www.youtube.com/watch?v=wvtdrKZeLZ4)*
    
    Prediksi Kemenangan sebuah tim di atas kertas berdasarkan hero pool.
    
    *(Data MPL ID, perkiraan tanggal pengambilan 23 September 2024.)*
    """
)

# --- Data and Statistics Section ---
df = load_data(file_path)

if not df.empty:
    # Display statistics
    st.subheader("Statistik Hero")
    
    # Using columns for a cleaner layout
    col1, col2 = st.columns(2)

    with col1:
        if st.checkbox('Tampilkan Data Mentah (Raw Data)'):
            st.subheader('Raw Data')
            st.dataframe(df)

    with col2:
        if st.checkbox('Tampilkan Statistik Hero Teratas'):
            st.subheader('Hero Paling Sering di-Pick')
            top_picks = df.sort_values(by="Pick", ascending=False).head(3)
            st.dataframe(top_picks[["Hero", "Pick", "Win Rate"]])

            st.subheader('Hero Paling Sering di-Ban')
            top_bans = df.sort_values(by="Ban", ascending=False).head(3)
            st.dataframe(top_bans[["Hero", "Ban", "Win Rate"]])

    st.divider()

    # --- Hero Selection Section ---
    st.subheader("Bangun Komposisi Tim")
    
    all_heroes = sorted(df["Hero"].tolist())
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tim Anda")
        your_team = []
        # Use a list of roles to generate select boxes dynamically
        roles = ["Gold Lane", "Exp Lane", "Mid Lane", "Roamer", "Jungler"]
        
        # Keep track of selected heroes to prevent duplicates
        selected_heroes_your_team = []
        for role in roles:
            available_heroes = [h for h in all_heroes if h not in selected_heroes_your_team]
            hero = st.selectbox(f"{role}:", available_heroes, key=f"your_{role}")
            selected_heroes_your_team.append(hero)
        your_team = selected_heroes_your_team


    with col2:
        st.subheader("Tim Lawan")
        opponent_team = []
        
        # Keep track of selected heroes to prevent duplicates
        selected_heroes_opponent = []
        for role in roles:
            # Lawan tidak bisa memilih hero yang sudah dipilih tim Anda
            available_heroes = [h for h in all_heroes if h not in your_team and h not in selected_heroes_opponent]
            hero = st.selectbox(f"{role} (Lawan):", available_heroes, key=f"opp_{role}")
            selected_heroes_opponent.append(hero)
        opponent_team = selected_heroes_opponent


    # --- Prediction Logic ---
    if st.button("Lakukan Prediksi", use_container_width=True, type="primary"):
        # Check for duplicate heroes across both teams
        if len(set(your_team + opponent_team)) != 10:
            st.warning("Pastikan tidak ada hero yang sama di kedua tim dan semua role telah diisi!")
        else:
            # Calculate win rate for both teams based on the 'Win' column
            your_team_win_sum = df[df["Hero"].isin(your_team)]["Win"].sum()
            opponent_team_win_sum = df[df["Hero"].isin(opponent_team)]["Win"].sum()

            total_win_sum = your_team_win_sum + opponent_team_win_sum

            if total_win_sum == 0:
                st.error("Tidak dapat menghitung prediksi. Total kemungkinan menang adalah nol.")
            else:
                your_team_percentage = (your_team_win_sum / total_win_sum) * 100
                opponent_team_percentage = (opponent_team_win_sum / total_win_sum) * 100

                # Display the prediction result
                st.subheader("Hasil Prediksi")
                
                if your_team_win_sum > opponent_team_win_sum:
                    st.success(f"Tim Anda memiliki kemungkinan menang lebih tinggi: **{your_team_percentage:.2f}%**")
                elif opponent_team_win_sum > your_team_win_sum:
                     st.error(f"Tim Lawan memiliki kemungkinan menang lebih tinggi: **{opponent_team_percentage:.2f}%**")
                else:
                    st.info(f"Kekuatan kedua tim seimbang! Kemungkinan menang 50/50.")

                # Progress bar for visualization
                st.progress(your_team_percentage / 100)
                st.markdown(f"**Tim Anda ({your_team_percentage:.2f}%)** vs **Tim Lawan ({opponent_team_percentage:.2f}%)**")
else:
    st.error("Gagal memuat data hero. Aplikasi tidak dapat berjalan.")
