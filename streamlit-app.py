import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Path to the Excel file from GitHub
file_path = "https://github.com/zenklinov/MLBB_PredictionWR/raw/main/Data_MPL.xlsx"

# Import data from Excel
df = pd.read_excel(file_path)

# Page configuration
st.set_page_config(
    page_title="Hello, Selamat datang di Matana University program studi Statistika",
    page_icon="👋",
)

# Image from URL (Matana University Logo)
url = "https://www.matanauniversity.ac.id/wp-content/uploads/2021/12/logo-Horizontal-white-newfooter.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
st.image(img, use_column_width=True)

st.title("Matana University")
st.markdown(
    """
    Selamat datang di Matana University! Bergabunglah dengan program studi Statistika kami, di mana lulusan kami telah sukses di ruang lingkup pemerintahan maupun swasta, di berbagai sektor seperti ekonomi, kebumian, agrikultur, kesehatan, informatika, dll. Anda juga dapat menjadi ahli dalam analisis data seperti dalam game Mobile Legends! Dengan kurikulum inovatif dan praktik langsung, Anda akan mempelajari cara mengolah serta menganalisis data untuk meningkatkan strategi permainan. Raih peluang karier menarik di industri game dan buktikan bahwa angka adalah senjata utama Anda!
    """
)

st.title("Mobile Legends Win Prediction")

# Video display
st.video("https://www.youtube.com/watch?v=wvtdrKZeLZ4")

st.markdown(
    """
    Source Video: https://www.youtube.com/watch?v=wvtdrKZeLZ4 (YT: akmj.mp4)
    
    Prediksi Kemenangan sebuah tim di atas kertas berdasarkan hero pool.
    
    (Data MPL ID Season 14, diambil pada 23 September 2024.)
    """
)

# Display statistics
st.subheader("Statistik")
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.dataframe(df)

if st.checkbox('Show Hero Statistics'):
    st.subheader('Statistik Hero')

    # Top Pick Heroes
    top_picks = [
        {"name": "Edith", "pick": df.loc[df["Hero"] == "Edith", "Pick"].values[0], "win_rate": df.loc[df["Hero"] == "Edith", "Win Rate"].values[0],
        "image_url": "https://i.pinimg.com/originals/f9/06/88/f906889db8c59dadb55f876e4618f5af.jpg"},
        {"name": "Roger", "pick": df.loc[df["Hero"] == "Roger", "Pick"].values[0], "win_rate": df.loc[df["Hero"] == "Roger", "Win Rate"].values[0],
        "image_url": "https://i.pinimg.com/originals/f7/e8/c7/f7e8c75bf879fc26d982b5b776202622.png"},
        {"name": "Harith", "pick": df.loc[df["Hero"] == "Harith", "Pick"].values[0], "win_rate": df.loc[df["Hero"] == "Harith", "Win Rate"].values[0],
        "image_url": "https://i.pinimg.com/originals/b5/27/0c/b5270c9a8e32501d38746f985f850fa4.jpg"},
    ]

    st.write("**Top Pick:**")
    for hero in top_picks:
        st.write(f"{hero['name']} (Pick: {hero['pick']}), win rate: {hero['win_rate'] * 100:.2f}%")
        st.image(hero['image_url'], width=100)

    # Top Ban Heroes
    top_bans = [
        {"name": "Chip", "ban": df.loc[df["Hero"] == "Chip", "Ban"].values[0], "win_rate": df.loc[df["Hero"] == "Chip", "Win Rate"].values[0],
        "image_url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhtOko5coR_0pPKhUxeloC9HCFaquwDc-BW308XmwkhtgAWOPRNKaKB9OJTqKIwkeS_MDRoB15f15UWsjHrMPcWgEAP2PL0QlvxgEsidE2nFrKE2G_fiPexlkZphA8XNO2g1u_a7yiRBW0g-Y4tB3gwOQwFt9d1o9Yd9E2tOMpEpCImKoZFSF8Bdrkv-g/s1920/new%20hero%20chip.jpg"},
        {"name": "Fanny", "ban": df.loc[df["Hero"] == "Fanny", "Ban"].values[0], "win_rate": df.loc[df["Hero"] == "Fanny", "Win Rate"].values[0],
        "image_url": "https://i.pinimg.com/originals/da/09/5d/da095d940052c99fad6449f119e3d4ec.jpg"},
        {"name": "Zhuxin", "ban": df.loc[df["Hero"] == "Zhuxin", "Ban"].values[0], "win_rate": df.loc[df["Hero"] == "Zhuxin", "Win Rate"].values[0],
        "image_url": "https://i.pinimg.com/originals/5b/6b/00/5b6b00814aa14b8a4aaf108b7cff3b0b.jpg"},
    ]

    st.write("**Top Ban:**")
    for hero in top_bans:
        st.write(f"{hero['name']} (Ban: {hero['ban']}), win rate: {hero['win_rate'] * 100:.2f}%")
        st.image(hero['image_url'], width=100)

# Select heroes for your team
st.subheader("Pilih Hero untuk Tim Anda")
gold_lane = st.selectbox("Gold Lane:", df["Hero"].tolist())
exp_lane = st.selectbox("Exp Lane:", [hero for hero in df["Hero"] if hero != gold_lane])
mid_lane = st.selectbox("Mid Lane:", [hero for hero in df["Hero"] if hero not in [gold_lane, exp_lane]])
roamer = st.selectbox("Roamer:", [hero for hero in df["Hero"] if hero not in [gold_lane, exp_lane, mid_lane]])
jungler = st.selectbox("Jungler:", [hero for hero in df["Hero"] if hero not in [gold_lane, exp_lane, mid_lane, roamer]])

your_team = [gold_lane, exp_lane, mid_lane, roamer, jungler]

# Select heroes for the opponent team
st.subheader("Pilih Hero untuk Tim Lawan")
opponent_gold_lane = st.selectbox("Gold Lane (Lawan):", [hero for hero in df["Hero"] if hero not in your_team])
opponent_exp_lane = st.selectbox("Exp Lane (Lawan):", [hero for hero in df["Hero"] if hero not in your_team + [opponent_gold_lane]])
opponent_mid_lane = st.selectbox("Mid Lane (Lawan):", [hero for hero in df["Hero"] if hero not in your_team + [opponent_gold_lane, opponent_exp_lane]])
opponent_roamer = st.selectbox("Roamer (Lawan):", [hero for hero in df["Hero"] if hero not in your_team + [opponent_gold_lane, opponent_exp_lane, opponent_mid_lane]])
opponent_jungler = st.selectbox("Jungler (Lawan):", [hero for hero in df["Hero"] if hero not in your_team + [opponent_gold_lane, opponent_exp_lane, opponent_mid_lane, opponent_roamer]])

opponent_team = [opponent_gold_lane, opponent_exp_lane, opponent_mid_lane, opponent_roamer, opponent_jungler]

# Prediction button
if st.button("Lakukan Prediksi"):
    if all(hero != "Choose an option" for hero in your_team + opponent_team):
        # Calculate win rate for both teams
        your_team_winrate = average(df[df["Hero"].isin(your_team)]["Win"])
        opponent_team_winrate = average(df[df["Hero"].isin(opponent_team)]["Win"])

        # Predict the winner
        if your_team_winrate > opponent_team_winrate:
            winner = "Tim Anda"
            winning_percentage = (your_team_winrate / (your_team_winrate + opponent_team_winrate)) * 100
        else:
            winner = "Tim Lawan"
            winning_percentage = (opponent_team_winrate / (your_team_winrate + opponent_team_winrate)) * 100

        # Display the prediction result
        st.subheader("Hasil Prediksi")
        st.write(f"Menang: {winner} dengan kemungkinan {winning_percentage:.2f}%")
    else:
        st.warning("Pastikan semua role telah diisi!")
