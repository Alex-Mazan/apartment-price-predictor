import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Apartments Price Predictor",
    page_icon="🏠",
    layout="wide"
)

#####################
# Localization Dict
#####################

# --- Voivodeships (regions) and their main cities ---
REGIONS = {
    "dolnośląskie": ["Wrocław"],
    "kujawsko-pomorskie": ["Bydgoszcz", "Toruń"],
    "lubelskie": ["Lublin"],
    "lubuskie": ["Zielona Góra", "Gorzów Wielkopolski"],
    "łódzkie": ["Łódź"],
    "małopolskie": ["Kraków"],
    "mazowieckie": ["Warszawa"],
    "opolskie": ["Opole"],
    "podkarpackie": ["Rzeszów"],
    "podlaskie": ["Białystok"],
    "pomorskie": ["Gdańsk"],
    "śląskie": ["Katowice"],
    "świętokrzyskie": ["Kielce"],
    "warmińsko-mazurskie": ["Olsztyn"],
    "wielkopolskie": ["Poznań"],
    "zachodniopomorskie": ["Szczecin"]
}

# --- Major cities and their districts ---
WAW_DISTRICTS = [
    "Bemowo", "Białołęka", "Bielany", "Mokotów", "Ochota",
    "Praga-Południe", "Praga-Północ", "Rembertów", "Śródmieście",
    "Targówek", "Ursus", "Ursynów", "Wawer", "Wesoła",
    "Wilanów", "Włochy", "Wola", "Żoliborz"
]

KRA_DISTRICTS = [
    "Stare Miasto", "Grzegórzki", "Prądnik Czerwony", "Prądnik Biały",
    "Krowodrza", "Bronowice", "Zwierzyniec", "Dębniki",
    "Łagiewniki-Borek Fałęcki", "Swoszowice", "Podgórze Duchackie",
    "Bieżanów-Prokocim", "Podgórze", "Czyżyny", "Mistrzejowice",
    "Bieńczyce", "Wzgórza Krzesławickie"
]

BIA_DISTRICTS = [
    "Centrum", "Białostoczek", "Sienkiewicza", "Bojary", "Piaski",
    "Antoniuk", "Jaroszówka", "Wygoda", "Piasta I i II", "Wysoki Stoczek",
    "Dziesięciny I i II", "Bacieczki", "Starosielce", "Dojlidy"
]

BYD_DISTRICTS = [
    "Babia Wieś", "Bartodzieje", "Bielawy", "Błonie", "Bocianowo-Śródmieście-Stare Miasto",
    "Brdyujście", "Bydgoszcz Wschód-Siernieczek", "Czyżkówko", "Flisy",
    "Glinki-Rupienica", "Górzyskowo", "Jachcice", "Kapuściska", "Leśne",
    "Łęgnowo", "Łęgnowo Wieś", "Miedzyń-Prądy", "Nowy Fordon", "Okole",
    "Osowa Góra", "Piaski", "Smukała-Opławiec-Janowo", "Stary Fordon",
    "Szwederowo", "Tatrzańskie", "Terenów Nadwiślańskich", "Wilczak-Jary",
    "Wyżyny", "Wzgórze Wolności", "Zimne Wody–Czersko Polskie"
]

GDA_DISTRICTS = [
    "Aniołki", "Brętowo", "Brzeźno", "Chełm", "Jasień", "Kokoszki",
    "Krakowiec-Górki Zachodnie", "Letnica", "Matarnia", "Młyniska",
    "Nowy Port", "Oliwa", "Olszynka", "Orunia-Św. Wojciech-Lipce",
    "Orunia Górna-Gdańsk Południe", "Osowa", "Piecki-Migowo", "Przeróbka",
    "Przymorze Małe", "Przymorze Wielkie", "Rudniki", "Siedlce", "Stogi",
    "Suchanino", "Śródmieście", "Ujeścisko-Łostowice", "Wrzeszcz Dolny",
    "Wrzeszcz Górny", "Zaspa-Młyniec", "Zaspa-Rozstaje",
    "Żabianka-Wejhera-Jelitkowo-Tysiąclecia"
]

GOR_DISTRICTS = [
    "Baczyna", "Chróścik", "Chwalęcice", "Górczyn", "Janice", "Karnin",
    "Małyszyn Wielki", "Małyszyn Mały", "Nowy Dwór", "Piaski", "Sady",
    "Śródmieście", "Zakanale"
]

KIE_DISTRICTS = [
    "Baranówek", "Barwinek", "Białogon", "Biesak", "Bocianek", "Bukówka",
    "Cedro-Mazur", "Cegielnia", "Centrum", "Chęcińskie", "Czarnów",
    "Dąbrowa", "Dobromyśl", "Domaszowice Wikaryjskie", "Dyminy-Wieś",
    "Głęboczka", "Herby", "Jagiellońskie", "Karczówka", "Łazy", "Malików",
    "Na Stoku", "Nowy Folwark", "Niewachlów I", "Niewachlów II",
    "Osiedle Jana Czarnockiego", "Osiedle Jana Kochanowskiego", "Ostra Górka",
    "Pakosz", "Panorama", "Piaski", "Pietraszki", "Pod Dalnią", "Podhale",
    "Podkarczówka", "Pod Telegrafem", "Posłowice", "Sady", "Sandomierskie",
    "Sieje", "Sitkówka", "Skrzetle", "Słoneczne Wzgórze", "Słowik",
    "Szydłówek", "Ślichowice", "Świętokrzyskie", "Uroczysko", "Wielkopole",
    "Wietrznia", "Zacisze", "Zalesie", "Zagórska Południe",
    "Zagórska Północ", "Zagórze", "Związkowiec"
]

KAT_DISTRICTS = [
    "Śródmieście", "Koszutka", "Bogucice", "Osiedle Paderewskiego – Muchowiec",
    "Załęże", "Osiedle Wincentego Witosa", "Osiedle Tysiąclecia", "Dąb",
    "Wełnowiec-Józefowiec", "Ligota-Panewniki", "Brynów-Osiedle Zgrzebnioka",
    "Załęska Hałda-Brynów", "Piotrowice-Ochojec", "Szopienice-Burowiec",
    "Murkowice", "Kostuchna", "Piotrowice", "Ochojec", "Zarzecze",
    "Dąbrówka Mała", "Stare Bogucice", "Nowe Bogucice"
]

LUB_DISTRICTS = [
    "Abramowice", "Bronowice", "Czechów Południowy", "Czechów Północny",
    "Czuby Południowe", "Czuby Północne", "Dziesiąta", "Felin", "Głusk",
    "Hajdów-Zadębie", "Kalinowszczyzna", "Konstantynów", "Kośminek",
    "Ponikwoda", "Rury", "Sławin", "Sławinek", "Stare Miasto", "Szerokie",
    "Śródmieście", "Tatary", "Węglin Południowy", "Węglin Północny",
    "Wieniawa", "Wrotków", "Za Cukrownią", "Zemborzyce"
]

LOD_DISTRICTS = ["Bałuty", "Górna", "Polesie", "Śródmieście", "Widzew"]

OLS_DISTRICTS = [
    "Brzeziny", "Dajtki", "Generałów", "Grunwaldzkie", "Gutkowo", "Jaroty",
    "Kętrzyńskiego", "Kormoran", "Kortowo", "Kościuszki", "Likusy",
    "Mazurskie", "Mleczna", "Nad Jeziorem Długim", "Nagórki", "Pieczewo",
    "Podgrodzie", "Podleśna", "Pojezierze", "Redykajny", "Śródmieście",
    "Wojska Polskiego", "Zatorze", "Zielona Górka"
]

OPO_DISTRICTS = [
    "Borki", "Brzezie", "Czarnowąsy", "Świerkle", "Krzanowice",
    "Wróblin", "Zakrzów", "Chabry", "Armii Krajowej", "Gosławice",
    "Malinka", "Nowa Wieś Królewska", "Półwieś"
]

POZ_DISTRICTS = [
    "Antoninek-Zieliniec-Kobylepole", "Chartowo", "Fabianowo-Kotowo",
    "Główna", "Głuszyna", "Górczyn", "Grunwald Północ", "Grunwald Południe",
    "Jeżyce", "Junikowo", "Kiekrz", "Krzesiny-Pokrzywno-Garaszewo",
    "Krzyżowniki-Smochowice", "Kwiatowe", "Ławica", "Morasko-Radojewo",
    "Naramowice", "Nowe Winogrady Południe", "Nowe Winogrady Północ",
    "Nowe Winogrady Wschód", "Ogrody", "Ostrów Tumski-Śródka-Zawady-Komandoria",
    "Piątkowo", "Podolany", "Rataje", "Sołacz", "Stare Miasto",
    "Starołęka-Minikowo-Marlewo", "Strzeszyn", "Szczepankowo-Spławie-Krzesinki",
    "Stare Winogrady", "Świerczewo", "Św. Łazarz", "Umultowo", "Wilda",
    "Warszawskie-Pomet-Maltańskie", "Winiary", "Wola", "Żegrze", "Zielony Dębiec"
]

RZE_DISTRICTS = [
    "1000-Lecia", "Baranówka", "Biała", "Budziwój", "Bzianka", "Dąbrowskiego",
    "Drabinianka", "Franciszka Kotuli", "Generała Grota Roweckiego",
    "Generała Władysława Andersa", "Kmity", "Krakowska – Południe",
    "Króla Stanisława Augusta", "Matysówka", "Mieszka I", "Miłocin – św. Huberta",
    "Miłocin", "Nowe Miasto", "Paderewskiego", "Piastów", "Pobitno",
    "Pogwizdów Nowy", "Pułaskiego", "Przybyszówka", "Staromieście",
    "Śródmieście", "Wilkowyja", "Zalesie", "Zawiszy Czarnego", "Zwięczyca"
]

SZC_DISTRICTS = [
    "Arkońskie-Niemierzyn", "Bukowe-Klęskowo", "Bukowo", "Centrum",
    "Dąbie", "Drzetowo-Grabowo", "Głębokie-Pilchowo", "Golęcino-Gocław",
    "Gumieńce", "Kijewo", "Krzekowo-Bezrzecze", "Łękno", "Majowe",
    "Międzyodrze-Wyspa Pucka", "Niebuszewo", "Niebuszewo-Bolinko",
    "Nowe Miasto", "Osów", "Płonia-Śmierdnica-Jezierzyce", "Podjuchy",
    "Pogodno", "Pomorzany", "Skolwin", "Słoneczne", "Stare Miasto",
    "Stołczyn", "Śródmieście-Północ", "Śródmieście-Zachód", "Świerczewo",
    "Turzyn", "Załom", "Zawadzkiego", "Zdroje", "Złocień"
]

TOR_DISTRICTS = [
    "Barbarka", "Bielany", "Bielawy", "Bydgoskie Przedmieście",
    "Chełmińskie Przedmieście", "Czerniewice", "Glinki", "Grębocin nad Strugą",
    "Jakubskie Przedmieście", "Kaszczorek", "Katarzynka", "Koniuchy",
    "Mokre", "Na Skarpie", "Piaski", "Podgórz", "Rubinkowo", "Rudak",
    "Rybaki", "Stare Miasto", "Starotoruńskie Przedmieście", "Stawki",
    "Winnica", "Wrzosy"
]

ZIE_DISTRICTS = [
    "Barcikowice", "Drzonków", "Jany", "Jarogniewice", "Jeleniów", "Kiełpin",
    "Krępa", "Łężyca", "Ługowo", "Nowy Kisielin", "Ochla", "Przylep", "Racula",
    "Raculka", "Sucha", "Zatonie", "Zawada", "Zielona Góra",
    "Zielona Góra – Centrum", "Zielona Góra – Północ", "Zielona Góra – Południe",
    "Zielona Góra – Wschód", "Zielona Góra – Zachód",
    "Zielona Góra – Osiedle Młodych", "Zielona Góra – Osiedle Piastowskie",
    "Zielona Góra – Osiedle Słowiańskie", "Zielona Góra – Osiedle Zawiszy Czarnego",
    "Zielona Góra – Osiedle Wyszyńskiego", "Zielona Góra – Osiedle Wrocławskie"
]

# --- All supported cities ---
CITIES = [
    "Warszawa", "Kraków", "Białystok", "Bydgoszcz", "Gdańsk",
    "Gorzów Wielkopolski", "Kielce", "Katowice", "Lublin", "Łódź",
    "Olsztyn", "Opole", "Poznań", "Szczecin", "Rzeszów",
    "Toruń", "Wrocław", "Zielona Góra"
]

# --- Mapping cities to their districts ---
CITY_TO_DISTRICTS = {
    "Warszawa": WAW_DISTRICTS,
    "Kraków": KRA_DISTRICTS,
    "Białystok": BIA_DISTRICTS,
    "Bydgoszcz": BYD_DISTRICTS,
    "Gdańsk": GDA_DISTRICTS,
    "Gorzów Wielkopolski": GOR_DISTRICTS,
    "Kielce": KIE_DISTRICTS,
    "Katowice": KAT_DISTRICTS,
    "Lublin": LUB_DISTRICTS,
    "Łódź": LOD_DISTRICTS,
    "Olsztyn": OLS_DISTRICTS,
    "Opole": OPO_DISTRICTS,
    "Poznań": POZ_DISTRICTS,
    "Szczecin": SZC_DISTRICTS,
    "Rzeszów": RZE_DISTRICTS,
    "Toruń": TOR_DISTRICTS,
    "Wrocław": WAW_DISTRICTS,  # Example placeholder — update with real districts if needed
    "Zielona Góra": ZIE_DISTRICTS
}

#####################
# Application
#####################

st.title("🏠 Apartments Price Predictor")

# --------------------
# Inputs
# --------------------
# tworzymy CITY_TO_REGION
CITY_TO_REGION = {city: region for region, cities in REGIONS.items() for city in cities}

col1, col2, col3, col4 = st.columns(4)

with col1:
    t_area = st.number_input("Area [m²]", min_value=10, max_value=500, value=50)
    df = pd.read_csv("cities_data/otodom_apartments_demo.csv", sep=";", encoding="utf-8-sig")
    t_price_per_m2 = st.number_input("Price per m²", min_value=0.0, value=float(df["price_per_m2"].mean()))

with col2:
    t_rooms = st.number_input("Amount of rooms", min_value=1, max_value=10, value=2)
    t_floor = st.number_input("Floor", min_value=0, max_value=50, value=2)

with col3:
    t_city = st.selectbox("City", CITIES)
    districts_for_city = CITY_TO_DISTRICTS.get(t_city, ["unknown"])
    t_district = st.selectbox("District", districts_for_city)

with col4:
    t_region = CITY_TO_REGION.get(t_city, "unknown")
    st.text_input("Region", t_region, disabled=True)
    t_type = st.selectbox("Type of seller", ["Private", "Estate Agency"])

# --------------------
# Load model
# --------------------
model = joblib.load("models/rf_model.pkl")
encoders = joblib.load("models/encoders.pkl")

# --------------------
# Prepare input
# --------------------
input_df = pd.DataFrame({
    "price_per_m2": [t_price_per_m2],
    "type": [t_type],
    "rooms": [t_rooms],
    "area": [t_area],
    "floor": [t_floor],
    "district": [t_district],
    "city": [t_city]
})

# Encode categorical
for col, le in encoders.items():
    if col in input_df.columns:
        val = input_df[col].iloc[0]
        if val not in le.classes_:
            le.classes_ = np.append(le.classes_, "unknown")
            val = "unknown"
        input_df[col] = le.transform([val])

# --------------------
# Prediction
# --------------------
predicted_price = model.predict(input_df)[0]

st.success(f"Predicted price of your dream apartment: {predicted_price:,.0f} PLN")
