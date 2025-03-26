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
    """Verbindet mit einem bestimmten Tabellenblatt in Google Sheets"""
    return client.open("MeineDaten").worksheet(sheet_name)

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

# Passwortschutz
PASSWORD = "FickDich123"  # Ändere das Passwort hier

def check_password():
    """Prüft das Passwort und zeigt die App nur bei korrektem Passwort an."""
    entered_password = st.text_input("🔒 Enter Password:", type="password")
    if entered_password == PASSWORD:
        return True
    elif entered_password:
        st.error("❌ Password incorrect!")
        return False
    return False

# Falls Passwort nicht korrekt → Keine App anzeigen
if not check_password():
    st.stop()

# Streamlit App UI
st.title("📊 Bob's Management App")
main_selection = st.radio("Select an Option:", ["🧮 Calculator", "📁 Tables"])

# Main investment models with allocations (SUM must be exactly 1.00)
investment_models = {
    "Moderate": {
        "Moderate Full": {
            "Cash": 0.01, "Commodities": 0.06, "Dividend": 0.09, "Fixed Core Full": 0.17, "Fixed Individuals": 0.17, 
            "LargeCap": 0.07, "Real Estate": 0.08, "Sm/Md Cap Funds": 0.08, "Stock Core": 0.27
        },
        "Moderate Lite": {
            "Cash": 0.01, "Commodities": 0.06, "Fixed Core Lite & Small": 0.34, "LargeCap": 0.23, 
            "Real Estate": 0.08, "Sm/Md Cap Funds": 0.13, "Stock Core Light": 0.15
        },
        "Moderate Small Account": {
            "AGG": 0.11, "ARGT": 0.07, "Cash": 0.01, "IYR": 0.05, "PFF": 0.11, "PRRIX": 0.12, "PRUFX": 0.10, 
            "SMDV": 0.10, "SPLG": 0.15, "VBK": 0.08, "VIG": 0.10
        }
    },
    "Moderate Aggressive": {
        "Moderate Aggressive Full": {
            "Cash": 0.01, "Commodities": 0.10, "Dividend": 0.10, "Fixed Core Full": 0.08, "Fixed Individuals": 0.08,
            "LargeCap": 0.09, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.10, "Stock Core": 0.34
        },
        "Moderate Aggressive Lite": {
            "Cash": 0.01, "Commodities": 0.10, "Fixed Core Lite & Small": 0.16, "LargeCap": 0.27, "Real Estate": 0.10, 
            "Sm/Md Cap Funds": 0.21, "Stock Core Light": 0.15
        },
        "Moderate Aggressive Small Account": {
             "AGG": 0.06, "ARGT": 0.07, "Cash": 0.01, "IYR": 0.07, "PFF": 0.06, "PRRIX": 0.06, "PRUFX": 0.13, 
            "SMDV": 0.12, "SPLG": 0.20, "VBK": 0.10, "VIG": 0.12
        }
    },
    "Aggressive": {
        "Aggressive Full": {
            "Cash": 0.01, "Commodities": 0.10, "Dividend": 0.10, "Fixed Core Lite & Small": 0.05, 
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
    "Fixed Core Lite & Small": {
        "PRRIX": 1.00
    },
    "Fixed Core Full": {
        "AGG": 0.333, "PFF": 0.333, "PRRIX": 0.334
    },
    "Sm/Md Cap Funds": {
        "SMDV": 0.33, "SPMD": 0.33, "VBK": 0.34
    },
    "Commodities": {
        "COM": 0.25, "GLD": 0.50, "URA": 0.25
    },
    "Stock Core": {
        "AAPL": 0.0217, "ABBV": 0.0217, "ABNB": 0.0217, "AMZN": 0.0652, "CHKP": 0.0217, 
        "COST": 0.0217, "CRWD": 0.0217, "CVX": 0.0217, "DOCS": 0.0217,  
        "DVA": 0.0217, "EXC": 0.0217, "FDX": 0.0217, "GNRC": 0.0217, "GOOGL": 0.0217, "GS": 0.0217, "INTC": 0.0217,
        "JPM": 0.0217, "KO": 0.0217, "LLY": 0.0217, "LOW": 0.0217, "MA": 0.0217, 
        "MMM": 0.0217, "MP": 0.0217, "MSFT": 0.0217, "MTN": 0.0217, "NFLX": 0.0217, "NTNX": 0.0217, "NVDA": 0.0217, "ODFL": 0.0217, "PAYO": 0.0217, 
        "QCOM": 0.0217, "REGN": 0.0217, "SBUX": 0.0217, "SPOT": 0.0217, "STLD": 0.0217, 
        "STZ": 0.0217, "TSLA": 0.0435, "T": 0.0217, "UL": 0.0217, "ULTA": 0.0217, "V": 0.0217, 
        "VZ": 0.0217, "WFC": 0.0217
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
    sub_selection = st.radio("Select a Table:", ["🚗 Cars", "🩸 Blood Pressure Incident", "💊 Medication Rx", "🏥 G/I"])

    if sub_selection == "🚗 Cars":
        st.subheader("🚗 Cars")
        datum = st.date_input("Date")
        modell = st.selectbox("Car Model", ["Bea's Honda CRV", "Nik Honda Acorde", "Bob's Mitsubishi", "Bri's Jeep", "Dad's Kia"])
        service_center = st.text_input("Service Center")
        service_art = st.selectbox("Service Category", ["Breaks", "Battery", "Tires", "Alignment"])
        kosten = st.number_input("Costs ($)", min_value=0.0, step=10.0)
        notes = st.text_input("Notes")

        if st.button("➕ Add entry"):
            insert_data("AutoFuhrpark", [datum.strftime("%Y-%m-%d"), modell, service_center, service_art, kosten, notes])
            st.success("✅ Entry saved!")

        df = get_data("AutoFuhrpark")
        st.table(df)

        if st.button("❌ Delete last entry"):
            delete_row("AutoFuhrpark")
            st.success("🗑️ Last entry deleted!")

    elif sub_selection == "🩸 Blood Pressure Incident":
        st.subheader("🩸 Blood Pressure Incident")
        bp_diag = st.text_input("BP DIAG.")
        s_st = st.text_input("S/S.T.")
        datum = st.date_input("Date")
        time = st.time_input("Time")
        location = st.text_input("Location")
        monitor = st.text_input("Monitor/Device")
        notes = st.text_input("Notes")

        if st.button("➕ Add entry"):
            insert_data("Health", [bp_diag, s_st, datum.strftime("%Y-%m-%d"), time.strftime("%H:%M"), location, monitor, notes])
            st.success("✅ Entry saved!")

        df = get_data("Health")
        st.table(df)

        if st.button("❌ Delete last entry"):
            delete_row("Health")
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

        if st.button("➕ Add entry"):
            insert_data("DaughterExpenses", [name_prescriber, name_medication, dosage, frequency, datum.strftime("%Y-%m-%d"), prescribed, purpose, status])
            st.success("✅ Entry saved!")

        df = get_data("DaughterExpenses")
        df.index = df.index+1

        if not df.empty:
            st.markdown("### 📋 Medication Entries")

            # Zeige Tabelle zur Übersicht
            st.dataframe(df, use_container_width=True, height=300)
        
            # Aktionen pro Zeile separat (Löschen & Status ändern)
            for i, row in df.iterrows():
                with st.expander(f"📝 Edit entry {i}: {row.get('Medication name', '')}"):
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
            insert_data("GI", [datum.strftime("%Y-%m-%d"), time.strftime("%H:%M"), type, volume, notes])
            st.success("✅ Entry saved!")

        df = get_data("GI")
        st.table(df)

        if st.button("❌ Delete last entry"):
            delete_row("GI")
            st.success("🗑️ Last entry deleted!")

