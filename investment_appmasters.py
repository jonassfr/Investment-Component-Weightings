import streamlit as st
import pandas as pd

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

# Main investment models with allocations (SUM must be exactly 1.00)
investment_models = {
    "Moderate": {
        "Moderate Full": {
            "Cash": 0.01, "Dividend": 0.09, "Fixed Individuals": 0.17, "Fixed Core Full": 0.17,
            "Gold": 0.03, "LargeCap": 0.07, "Real Estate": 0.08, "Sm/Md Cap Funds": 0.08, "Stock Core": 0.30
        },
        "Moderate Lite": {
            "Cash": 0.01, "Fixed Core Lite & Small": 0.34, "LargeCap": 0.25, 
            "Real Estate": 0.08, "Sm/Md Cap Funds": 0.14, "Stock Core Light": 0.15, "Gold": 0.03
        },
        "Moderate Small Account": {
            "Cash": 0.01, "AGG": 0.11, "IYR": 0.05, "PRUFX": 0.10, "PRRIX": 0.12,
            "SMDV": 0.10, "SPLG": 0.15, "VBK": 0.08, "VIG": 0.10, "ARGT": 0.07, "PFF": 0.11
        }
    },
    "Moderate Aggressive": {
        "Moderate Aggressive Full": {
            "Cash": 0.01, "Dividend": 0.10, "Fixed Core Full": 0.08, "Fixed Individuals": 0.08,
            "Gold": 0.05, "LargeCap": 0.09, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.10, "Stock Core": 0.39
        },
        "Moderate Aggressive Lite": {
            "Cash": 0.01, "Fixed Core Lite & Small": 0.16, "LargeCap": 0.30, "Real Estate": 0.10, 
            "Sm/Md Cap Funds": 0.23, "Stock Core Light": 0.15, "Gold": 0.05
        },
        "Moderate Aggressive Small Account": {
            "Cash": 0.01, "AGG": 0.06, "IYR": 0.07, "PRUFX": 0.13, "PRRIX": 0.06, "SMDV": 0.12, 
            "SPLG": 0.20, "VBK": 0.10, "VIG": 0.12, "ARGT": 0.07, "PFF": 0.06
        }
    },
    "Aggressive": {
        "Aggressive Full": {
            "Cash": 0.01, "Dividend": 0.10, "Fixed Core Lite & Small": 0.05, "Gold": 0.05, 
            "LargeCap": 0.12, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.13, "Stock Core": 0.44
        }
    }
}

# Subcategories (Fixed formatting and category naming)
sub_categories = {
    "Dividend": {
        "VZ": 0.12, "JNJ": 0.12, "MO": 0.12, "MRK": 0.12,
        "PG": 0.13, "T": 0.13, "CPB": 0.13, "C": 0.13
    },
    "Real Estate": {
        "ADC": 0.20, "IYR": 0.40, "SPG": 0.20, "WPC": 0.20
    },
    "LargeCap": {
        "SPLG": 0.23, "VIG": 0.23, "EWU": 0.13, "PRUFX": 0.18, "IAT": 0.10, "ARGT": 0.13
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
    "Stock Core": {
        "AAPL": 0.0208, "ABBV": 0.0208, "ABNB": 0.0208, "AMZN": 0.0625, "CHKP": 0.0208, 
        "COST": 0.0208, "CRWD": 0.0208, "CVX": 0.0208, "DOCS": 0.0208, "DOW": 0.0208, 
        "DVA": 0.0208, "PAYO": 0.0208, "FDX": 0.0208, "GOOGL": 0.0208, "GS": 0.0208,
        "JPM": 0.0208, "KO": 0.0208, "LLY": 0.0208, "LOW": 0.0208, "MA": 0.0208, 
        "MMM": 0.0208, "MSFT": 0.0208, "NFLX": 0.0208, "NTNX": 0.0208, "ODFL": 0.0208, 
        "QCOM": 0.0208, "REGN": 0.0208, "SBUX": 0.0208, "SPOT": 0.0208, "STLD": 0.0208, 
        "STZ": 0.0208, "TSLA": 0.0208, "T": 0.0417, "UL": 0.0208, "ULTA": 0.0208, "V": 0.0208, 
        "VZ": 0.0208, "INTC": 0.0208, "COM": 0.0625, "GNRC": 0.0208, "MP": 0.0208, 
        "MTN": 0.0208, "WFC": 0.0208
    },
    "Stock Core Light": {
        "AAPL": 0.0588, "AMZN": 0.1176, "COST": 0.0588, "CVX": 0.0588, "DOCS": 0.0588, "DOW": 0.0588, "FDX": 0.0588,
        "JPM": 0.0588, "LLY": 0.0588, "MMM": 0.0588, "SBUX": 0.0588, "TSLA": 0.0588, "T": 0.1176, "UL": 0.0588, "V": 0.0588
    }
}

# Streamlit App UI
st.title("💰 Investment Calculator")
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
