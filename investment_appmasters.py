import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Lade Google Credentials aus Streamlit Secrets
creds_json = st.secrets["GOOGLE_CREDENTIALS"]
creds_dict = dict(st.secrets["GOOGLE_CREDENTIALS"])  # Stelle sicher, dass es ein Dictionary ist

# Authentifiziere mit Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
client = gspread.authorize(creds)

spreadsheet = client.open("MeineDaten")  # Name des Google Sheets
worksheet = spreadsheet.sheet1  # Erstes Arbeitsblatt auswählen

st.success("✅ Connection successful!")

def get_sheet(sheet_name):
    prefix = st.session_state.get("sheet_prefix", "")
    return client.open("MeineDaten").worksheet(prefix + sheet_name)

def insert_data(sheet_name, data):
    """Fügt eine neue Zeile in die Google Sheets-Tabelle ein"""
    sheet = get_sheet(sheet_name)
    sheet.append_row(data)

def get_data(sheet_name):
    """Lädt alle Daten aus Google Sheets und gibt sie als DataFrame zurück"""
    sheet = get_sheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data) if data else pd.DataFrame(columns=["Datum", "Kategorie", "Wert"])  # Fallback für leere Tabellen

def delete_row(sheet_name):
    """Löscht die letzte Zeile mit Daten (nicht Header) aus dem Sheet."""
    sheet = get_sheet(sheet_name)
    all_values = sheet.get_all_values()
    last_row = len(all_values)
    if last_row > 1:  # Nur löschen, wenn mehr als die Headerzeile vorhanden ist
        sheet.delete_rows(last_row)

# Nutzerverwaltung
USERS = {
    "bob": {"password": "B3ll@621", "role": "admin", "sheet_prefix": ""},
    "user1": {"password": "B3ll@621", "role": "user", "sheet_prefix": "D1_"},
    "user2": {"password": "B3ll@621", "role": "user", "sheet_prefix": "D2_"},
}

# Login-Funktion
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.session_state["sheet_prefix"] = user["sheet_prefix"]
            st.rerun() 
        else:
            st.error("❌ Incorrect username or password")
            
# Falls nicht eingeloggt, dann Login anzeigen und stoppen
if not st.session_state.get("logged_in"):
    login()
    st.stop()

# Streamlit App UI
st.title("📊 Management App")
st.markdown(f"👤 Logged in as: **{st.session_state['username']}** ({st.session_state['role']})")
# ⬅️ Logout Button oben platzieren
# ⬅️ Logout Button oben platzieren
if st.button("🚪 Logout", key="logout_top"):
    st.session_state.clear()
    st.rerun()

if st.session_state["role"] == "admin":
    main_selection = st.radio("Select an Option:", ["🧮 Calculator", "📁 Tables"])
else:
    main_selection = "📁 Tables"


# Main investment models with allocations (SUM must be exactly 1.00)
investment_models = {
    "Moderate": {
        "Moderate Full": {
            "Cash": 0.01, "Commodities": 0.06, "Dividend": 0.09, "Fixed Core": 0.17, "Fixed Individuals": 0.17, 
            "LargeCap": 0.07, "Real Estate": 0.08, "Sm/Md Cap Funds": 0.08, "Stock Core": 0.27
        },
        "Moderate Lite": {
            "Cash": 0.01, "Commodities": 0.06, "LargeCap": 0.23, "Fixed Core": 0.34,
            "Real Estate": 0.08, "Sm/Md Cap Funds": 0.13, "Stock Core Light": 0.15
        },
        "Moderate Small Account": {
            "ARGT": 0.07, "Cash": 0.01, "IYR": 0.05, "PRUFX": 0.10, 
            "SMDV": 0.10, "SPLG": 0.15, "VBK": 0.08, "VIG": 0.10, "Fixed Core": 0.34
        }
    },
    "Moderate Aggressive": {
        "Moderate Aggressive Full": {
            "Cash": 0.01, "Commodities": 0.10, "Dividend": 0.10, "Fixed Core": 0.08, "Fixed Individuals": 0.08,
            "LargeCap": 0.09, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.10, "Stock Core": 0.34
        },
        "Moderate Aggressive Lite": {
            "Cash": 0.01, "Commodities": 0.10, "Fixed Core": 0.16, "LargeCap": 0.27, "Real Estate": 0.10, 
            "Sm/Md Cap Funds": 0.21, "Stock Core Light": 0.15
        },
        "Moderate Aggressive Small Account": {
             "ARGT": 0.07, "Cash": 0.01, "Fixed Core": 0.18, "IYR": 0.07,"PRUFX": 0.13, 
            "SMDV": 0.12, "SPLG": 0.20, "VBK": 0.10, "VIG": 0.12
        }
    },
    "Aggressive": {
        "Aggressive Full": {
            "Cash": 0.01, "Commodities": 0.10, "Dividend": 0.10, "Fixed Core": 0.05,
            "LargeCap": 0.12, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.13, "Stock Core": 0.39
        }
    }
}

# Subcategories (Fixed formatting and category naming)
sub_categories = {
    "Dividend": {
        "C": 0.13, "CPB": 0.13, "DOW": 0.12, "JNJ": 0.12, "MRK": 0.12,
        "PG": 0.13, "T": 0.13, "VZ": 0.12
    },
    "Real Estate": {
        "ADC": 0.20, "IYR": 0.40, "SPG": 0.20, "WPC": 0.20
    },
    "LargeCap": {
        "ARGT": 0.13, "EWU": 0.13, "IAT": 0.10, "PRUFX": 0.18, "SPLG": 0.23, "VIG": 0.23
    },
    "Fixed Core": {
        "AGG": 0.333, "PFF": 0.333, "PRRIX": 0.334
    },
    "Sm/Md Cap Funds": {
        "SMDV": 0.33, "SPMD": 0.33, "VBK": 0.34
    },
    "Commodities": {
        "COM": 0.25, "GLD": 0.50, "URA": 0.25
    },
    "Stock Core": {
        "AAPL": 0.0213, "ABBV": 0.0213, "ABNB": 0.0213, "AMZN": 0.0638, "CHKP": 0.0213, 
        "COST": 0.0213, "CRWD": 0.0213, "CVX": 0.0213, "DOCS": 0.0213,  
        "DVA": 0.0213, "EXC": 0.0213, "FDX": 0.0213, "GNRC": 0.0213, "GOOGL": 0.0213, "GS": 0.0213, "INTC": 0.0213,
        "JPM": 0.0213, "KO": 0.0213, "LLY": 0.0213, "LOW": 0.0213, "MA": 0.0213, 
        "MMM": 0.0213, "MP": 0.0213, "MSFT": 0.0213, "MTN": 0.0426, "NFLX": 0.0213, "NTNX": 0.0213, "NVDA": 0.0213, "ODFL": 0.0213, "PAYO": 0.0213, 
        "QCOM": 0.0213, "REGN": 0.0213, "SBUX": 0.0213, "SPOT": 0.0213, "STLD": 0.0213, 
        "STZ": 0.0213, "TSLA": 0.0426, "T": 0.0213, "UL": 0.0213, "ULTA": 0.0213, "V": 0.0213, 
        "VZ": 0.0213, "WFC": 0.0213
    },
    "Stock Core Light": {
        "AAPL": 0.0625, "AMZN": 0.1250, "COST": 0.0625, "CVX": 0.0625, "DOCS": 0.0625, "FDX": 0.0625,
        "JPM": 0.0625, "LLY": 0.0625, "MMM": 0.0625, "SBUX": 0.0625, "TSLA": 0.1250, "T": 0.0625, "UL": 0.0625, "V": 0.0625
    }
}

if main_selection == "🧮 Calculator":
    st.subheader("💰 Investment Calculator")
    selected_category = st.selectbox("📌 Select Investment Category:", list(investment_models.keys()))
    selected_model = st.selectbox("📊 Select Investment Model:", list(investment_models[selected_category].keys()))
    amount = st.number_input("💵 Enter Investment Amount ($):", min_value=0.0, step=1000.0)

    if amount > 0:
        allocations = {category: round(amount * percent, 2) for category, percent in investment_models[selected_category][selected_model].items()}
        
        st.subheader("📊 Main Allocation Breakdown")
        df_main = pd.DataFrame(list(allocations.items()), columns=["Category", "Amount"])
        df_main["Amount"] = df_main["Amount"].apply(lambda x: f"${x:,.2f}")
        st.table(df_main)

        for main_category, main_amount in allocations.items():
            if main_category in sub_categories:
                st.subheader(f"🔹 {main_category} Breakdown")
                df_sub = pd.DataFrame([(sub, round(main_amount * percent, 2)) for sub, percent in sub_categories[main_category].items()], columns=["Sub-Category", "Amount"])
                df_sub["Amount"] = df_sub["Amount"].apply(lambda x: f"${x:,.2f}")
                st.table(df_sub)

        st.success("✅ Calculation saved.")

elif main_selection == "📁 Tables":
    sub_selection = st.radio("Select a Table:", ["🩸 Blood Pressure Incident", "💊 Medication Rx", "🏥 G/I"])

    if sub_selection == "🩸 Blood Pressure Incident":
        st.subheader("🩸 Blood Pressure Incident")
        bp_diag = st.text_input("BP DIAG.")
        s_st = st.text_input("S/S.T.")
        datum = st.date_input("Date")
        time = st.time_input("Time")
        location = st.text_input("Location")
        monitor = st.text_input("Monitor/Device")
        pulse = st.text_input("Pulse")
        ox = st.text_input("Ox")
        notes = st.text_input("Notes")

        if st.button("➕ Add entry"):
            insert_data("Health", [bp_diag, s_st, datum.strftime("%m/%d/%Y"), time.strftime("%H:%M"), location, monitor, pulse, ox, notes])
            st.success("✅ Entry saved!")

        df = get_data("Health")
        df.index = df.index+1

        if not df.empty:
            st.markdown("### 📋 Blood Pressure Entries")

            # Zeige Tabelle zur Übersicht
            st.dataframe(df, use_container_width=True, height=300)
        
            # Aktionen pro Zeile separat (Löschen & Status ändern)
            for i, row in df.iterrows():
                with st.expander(f"📝 Edit entry {i}: {row.get('Date', '')} | {row.get('Location', '')}"):
                    col1, col2 = st.columns([4, 1])

                    # Eintrag löschen
                    if col2.button("🗑️ Delete entry", key=f"delete_{i}"):
                        sheet = get_sheet("Health")
                        sheet.delete_rows(i + 1)
                        st.success("✅ Entry deleted.")
                        st.rerun()

        else:
            st.info("No entries found.")

        if st.button("❌ Delete last entry"):
            delete_row("DaughterExpenses")
            st.success("🗑️ Last entry deleted!")

    elif sub_selection == "💊 Medication Rx":
        st.subheader("💊 Medication Rx")
        name_prescriber = st.text_input("Prescriber name")
        name_medication = st.text_input("Medication name")
        dosage = st.text_input("Dosage")
        frequency = st.text_input("Frequency")
        datum = st.date_input("Start Date")
        prescribed = st.text_input("Prescribed")
        purpose = st.text_input("Purpose")
        status = st.selectbox("Status", ["active", "paused", "finished"])
        notes = st.text_input("Notes")

        if st.button("➕ Add entry"):
            insert_data("DaughterExpenses", [name_prescriber, name_medication, dosage, frequency, datum.strftime("%m/%d/%Y"), prescribed, purpose, status, notes])
            st.success("✅ Entry saved!")

        df = get_data("DaughterExpenses")
        df.index = df.index+1

        if not df.empty:
            st.markdown("### 📋 Medication Entries")

            # Zeige Tabelle zur Übersicht
            st.dataframe(df, use_container_width=True, height=300)
        
            # Aktionen pro Zeile separat (Löschen & Status ändern)
            for i, row in df.iterrows():
                with st.expander(f"📝 Edit entry {i}: {row.get('Start Date', '')} | {row.get('Medication', '')}"):
                    col1, col2 = st.columns([4, 1])
        
                    # Status ändern
                    current_status = row.get("Status", "active")
                    new_status = col1.selectbox(
                        "Status",
                        ["active", "paused", "finished"],
                        index=["active", "paused", "finished"].index(current_status),
                        key=f"status_{i}"
                    )
        
                    # Status speichern
                    if new_status != current_status:
                        sheet = get_sheet("DaughterExpenses")
                        sheet.update_cell(i + 1, df.columns.get_loc("Status") + 1, new_status)
                        st.success("🔄 Status updated.")
                        st.rerun()

                    # Eintrag löschen
                    if col2.button("🗑️ Delete entry", key=f"delete_{i}"):
                        sheet = get_sheet("DaughterExpenses")
                        sheet.delete_rows(i + 1)
                        st.success("✅ Entry deleted.")
                        st.rerun()



        else:
            st.info("No entries found.")

        if st.button("❌ Delete last entry"):
            delete_row("DaughterExpenses")
            st.success("🗑️ Last entry deleted!")
            
    elif sub_selection == "🏥 G/I":
        st.subheader("🏥 G/I")
        datum = st.date_input("Date")
        time = st.time_input("Time")
        type = st.selectbox("Type", ["1", "2", "3", "4", "5"])
        volume = st.selectbox("Volume",["Low", "Med", "High"])
        notes = st.text_input("Notes")

        if st.button("➕ Add entry"):
            insert_data("GI", [datum.strftime("%m/%d/%Y"), time.strftime("%H:%M"), type, volume, notes])
            st.success("✅ Entry saved!")

        df = get_data("GI")
        df.index = df.index+1

        if not df.empty:
            st.markdown("### 📋 G/I Entries")

            # Zeige Tabelle zur Übersicht
            st.dataframe(df, use_container_width=True, height=300)
        
            # Aktionen pro Zeile separat (Löschen & Status ändern)
            for i, row in df.iterrows():
                with st.expander(f"📝 Edit entry {i}: {row.get('Date', '')} | {row.get('Time', '')}"):
                    col1, col2 = st.columns([4, 1])
                    
                    # Eintrag löschen
                    if col2.button("🗑️ Delete entry", key=f"delete_{i}"):
                        sheet = get_sheet("GI")
                        sheet.delete_rows(i + 1)
                        st.success("✅ Entry deleted.")
                        st.rerun()
if st.button("🚪 Logout", key="button_top"):
    st.session_state.clear()
    st.rerun()



