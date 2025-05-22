# Streamlit-based CologneGPT Web App

import streamlit as st
import json
import matplotlib.pyplot as plt
from collections import defaultdict

class CologneGPT:
    def __init__(self, user_scents):
        self.user_scents = user_scents
        self.scent_db = self.build_scent_db()
        self.ratings_file = "combo_ratings.json"
        self.combo_ratings = self.load_combo_ratings()

    def build_scent_db(self):
        return {
            "Creed Aventus": {
                "profile": ["fruity", "smoky", "pineapple", "musk"],
                "category": "Bold",
                "occasion": ["events", "weekends"],
                "type": "Niche"
            },
            "Jean Lowe Immortel": {
                "profile": ["fresh", "spicy", "woody"],
                "category": "Versatile",
                "occasion": ["daily", "office"],
                "type": "Clone"
            },
            "Versace Eros Flame": {
                "profile": ["sweet", "spicy", "citrus"],
                "category": "Sensual",
                "occasion": ["dates", "night"],
                "type": "Designer"
            },
            "Dolce & Gabbana Light Blue": {
                "profile": ["citrus", "aquatic", "woody"],
                "category": "Fresh",
                "occasion": ["daytime", "summer"],
                "type": "Designer"
            },
            "Acqua di Gio Pour Homme": {
                "profile": ["marine", "citrus", "aromatic", "woody"],
                "category": "Aquatic",
                "occasion": ["daytime", "office"],
                "type": "Designer"
            },
            "Louis Vuitton Imagination": {
                "profile": ["citrus", "ginger", "tea", "amber"],
                "category": "Elegant",
                "occasion": ["night", "formal"],
                "type": "Designer"
            },
            "Amber Oud Aqua Dubai": {
                "profile": ["aquatic", "amber", "oud"],
                "category": "Signature",
                "occasion": ["daily", "hot weather"],
                "type": "Clone"
            },
            "YSL Tuxedo": {
                "profile": ["patchouli", "ambergris", "vanilla"],
                "category": "Luxury",
                "occasion": ["events", "evening"],
                "type": "Designer"
            },
            "YSL Y": {
                "profile": ["apple", "sage", "ambergris", "woody"],
                "category": "Youthful",
                "occasion": ["daily", "night out"],
                "type": "Designer"
            },
            "YSL Myslf": {
                "profile": ["bergamot", "orange blossom", "ambrette"],
                "category": "Modern Fresh",
                "occasion": ["daytime", "spring"],
                "type": "Designer"
            },
            "Dior Sauvage EDT": {
                "profile": ["bergamot", "pepper", "ambroxan"],
                "category": "Fresh Spicy",
                "occasion": ["versatile", "day and night"],
                "type": "Designer"
            },
            "Dior Sauvage EDP": {
                "profile": ["bergamot", "amber", "lavender", "spicy"],
                "category": "Modern",
                "occasion": ["daytime", "night out"],
                "type": "Designer"
            },
            "Clive Christian Blonde Amber": {
                "profile": ["amber", "musk", "woods"],
                "category": "Rich",
                "occasion": ["evening", "formal"],
                "type": "Niche"
            },
            "Xerjoff Naxos": {
                "profile": ["honey", "tobacco", "citrus", "spicy"],
                "category": "Opulent",
                "occasion": ["evening", "cool weather"],
                "type": "Niche"
            },
            "Maison Patek Rouge": {
                "profile": ["saffron", "amber", "airy"],
                "category": "Sweet",
                "occasion": ["year-round", "special"],
                "type": "Clone"
            },
            "Parfums de Marly Layton": {
                "profile": ["apple", "vanilla", "lavender", "cardamom", "sandalwood"],
                "category": "Warm & Spicy",
                "occasion": ["day", "night"],
                "type": "Niche"
            },
            "Parfums de Marly Herod": {
                "profile": ["tobacco", "vanilla", "cinnamon", "incense"],
                "category": "Warm & Spicy",
                "occasion": ["evening", "fall", "winter"],
                "type": "Niche"
            },
            "Parfums de Marly Percival": {
                "profile": ["bergamot", "lavender", "musk", "amber"],
                "category": "Fresh & Aromatic",
                "occasion": ["daytime", "office"],
                "type": "Niche"
            },
            "Parfums de Marly Sedley": {
                "profile": ["mint", "lemon", "lavender", "sandalwood"],
                "category": "Fresh & Citrus",
                "occasion": ["spring", "summer", "daytime"],
                "type": "Niche"
            },
            "Parfums de Marly Althaïr": {
                "profile": ["vanilla", "cinnamon", "cardamom", "amber"],
                "category": "Warm & Sweet",
                "occasion": ["evening", "special occasions"],
                "type": "Niche"
            }
        }

    def load_combo_ratings(self):
        try:
            with open(self.ratings_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def analyze_profile(self):
        note_counter = defaultdict(int)
        for scent in self.user_scents:
            scent_data = self.scent_db.get(scent)
            if scent_data:
                for note in scent_data["profile"]:
                    note_counter[note] += 1
        return dict(sorted(note_counter.items(), key=lambda x: x[1], reverse=True))


# --- Streamlit App Logic ---

st.title("CologneGPT: Personalized Fragrance Recommender")

user_input = st.sidebar.text_area("Enter your fragrances (one per line):")
user_scents = [s.strip() for s in user_input.strip().splitlines() if s.strip()]

st.sidebar.subheader("Filter & Search")
selected_type = st.sidebar.selectbox("Filter by Scent Type", ["All"] + sorted(set(s["type"] for s in CologneGPT([]).build_scent_db().values())))
search_query = st.sidebar.text_input("Search Fragrance Name")

cgpt = CologneGPT(user_scents)

if selected_type != "All" or search_query:
    filtered = {
        name: data for name, data in cgpt.scent_db.items()
        if (selected_type == "All" or data["type"] == selected_type)
        and (search_query.lower() in name.lower())
    }
    st.subheader("Matching Scents")
    for name, data in filtered.items():
        st.markdown(f"**{name}**\n- Profile: {', '.join(data['profile'])}\n- Category: {data['category']}\n- Occasion: {', '.join(data['occasion'])}\n- Type: {data['type']}")

if user_scents:
    profile = cgpt.analyze_profile()
    st.subheader("Your Scent Profile")
    st.write(profile)

    st.subheader("Smart Layering Suggestions")
    hybrid_suggestions = []
    for base in user_scents:
        for top in user_scents:
            if base != top:
                base_notes = set(cgpt.scent_db.get(base, {}).get("profile", []))
                top_notes = set(cgpt.scent_db.get(top, {}).get("profile", []))
                if base_notes and top_notes:
                    shared = base_notes.intersection(top_notes)
                    if shared:
                        hybrid_suggestions.append((base, top, list(shared)))
    for base, top, shared in hybrid_suggestions:
        combo_key = f"{base} + {top}"
        if "saved_hybrids" not in st.session_state:
            st.session_state.saved_hybrids = []
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.write(f"- {base} + {top} (Shared notes: {', '.join(shared)})")
        with col2:
            if st.button(f"💾 Save", key=f"save_{combo_key}"):
                if combo_key not in st.session_state.saved_hybrids:
                    st.session_state.saved_hybrids.append(combo_key)
                    st.success(f"Saved hybrid: {combo_key}")

    if st.session_state.get("saved_hybrids"):
        st.subheader("📦 Saved Hybrids for Custom Requests")
        for combo in st.session_state.saved_hybrids:
            st.markdown(f"- {combo}")
        with st.form("custom_request_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            notes = st.text_area("Additional Notes")
            submitted = st.form_submit_button("Submit Request")
            if submitted:
                with open("custom_requests_log.txt", "a") as log:
                    log.write(f"Name: {name}\nEmail: {email}\nHybrids: {st.session_state.saved_hybrids}\nNotes: {notes}\n\n")
                st.success("Your request has been logged. We'll reach out to you at byjayare@gmail.com.")
