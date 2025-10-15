import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# --- Functions to make the code cleaner ---

def load_data(url):
    """Loads data from a remote Excel file."""
    try:
        # Cache the data loading to prevent re-downloading on every interaction
        @st.cache_data
        def get_data(url):
            return pd.read_excel(url)
        return get_data(url)
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

def reset_selections():
    """Clears the hero selections from the session state."""
    roles = ["Gold Lane", "Exp Lane", "Mid Lane", "Roamer", "Jungler"]
    for role in roles:
        st.session_state[f'team_a_{role}'] = None
        st.session_state[f'team_b_{role}'] = None


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
    Selamat datang di Matana University! Bergabunglah dengan program studi Data Science dan Aktuaria kami, di mana lulusan kami telah sukses di ruang lingkup pemerintahan maupun swasta, di berbagai sektor seperti ekonomi, kebumian, agrikultur, kesehatan, informatika, dll. 
    
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
    roles = ["Gold Lane", "Exp Lane", "Mid Lane", "Roamer", "Jungler"]
    
    # Initialize session state for selections
    for role in roles:
        if f'team_a_{role}' not in st.session_state:
            st.session_state[f'team_a_{role}'] = None
        if f'team_b_{role}' not in st.session_state:
            st.session_state[f'team_b_{role}'] = None

    team_a_heroes = []
    team_b_heroes = []

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tim A")
        # Keep track of selected heroes to prevent duplicates
        selected_heroes_a = []
        for role in roles:
            # Get heroes that are not yet selected in this team
            available_heroes = [h for h in all_heroes if h not in selected_heroes_a]
            hero = st.selectbox(f"{role}:", available_heroes, key=f"team_a_{role}", index=None, placeholder="Pilih hero...")
            if hero:
                selected_heroes_a.append(hero)
        team_a_heroes = selected_heroes_a


    with col2:
        st.subheader("Tim B")
        # Keep track of selected heroes to prevent duplicates
        selected_heroes_b = []
        for role in roles:
            # Team B cannot pick heroes already chosen by Team A or by other roles in Team B
            available_heroes = [h for h in all_heroes if h not in team_a_heroes and h not in selected_heroes_b]
            hero = st.selectbox(f"{role}:", available_heroes, key=f"team_b_{role}", index=None, placeholder="Pilih hero...")
            if hero:
                selected_heroes_b.append(hero)
        team_b_heroes = selected_heroes_b

    # --- Action Buttons ---
    pred_col, reset_col = st.columns(2)
    
    predict_button = pred_col.button("Lakukan Prediksi", use_container_width=True, type="primary")
    reset_button = reset_col.button("Reset Pilihan Hero", use_container_width=True, on_click=reset_selections)


    # --- Prediction Logic ---
    if predict_button:
        # Check if all roles are filled
        if len(team_a_heroes) != 5 or len(team_b_heroes) != 5:
            st.warning("Pastikan semua role di Tim A dan Tim B telah diisi!")
        else:
            # Calculate win rate for both teams based on the 'Win' column
            team_a_win_sum = df[df["Hero"].isin(team_a_heroes)]["Win"].sum()
            team_b_win_sum = df[df["Hero"].isin(team_b_heroes)]["Win"].sum()

            total_win_sum = team_a_win_sum + team_b_win_sum

            if total_win_sum == 0:
                st.error("Tidak dapat menghitung prediksi. Total kemungkinan menang adalah nol.")
            else:
                team_a_percentage = (team_a_win_sum / total_win_sum) * 100
                team_b_percentage = (team_b_win_sum / total_win_sum) * 100

                # Display the prediction result
                st.subheader("Hasil Prediksi")
                
                if team_a_win_sum > team_b_win_sum:
                    st.success(f"Tim A memiliki kemungkinan menang lebih tinggi: **{team_a_percentage:.2f}%**")
                elif team_b_win_sum > team_a_win_sum:
                     st.error(f"Tim B memiliki kemungkinan menang lebih tinggi: **{team_b_percentage:.2f}%**")
                else:
                    st.info(f"Kekuatan kedua tim seimbang! Kemungkinan menang 50/50.")

                # Progress bar for visualization
                st.progress(team_a_percentage / 100)
                st.markdown(f"**Tim A ({team_a_percentage:.2f}%)** vs **Tim B ({team_b_percentage:.2f}%)**")
else:
    st.error("Gagal memuat data hero. Aplikasi tidak dapat berjalan.")
