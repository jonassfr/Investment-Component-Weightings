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
            "Commodities": 0.06, "LargeCap": 0.07, "Real Estate": 0.08, "Sm/Md Cap Funds": 0.08, "Stock Core": 0.27
        },
        "Moderate Lite": {
            "Cash": 0.01, "Fixed Core Lite & Small": 0.34, "LargeCap": 0.23, 
            "Real Estate": 0.08, "Sm/Md Cap Funds": 0.13, "Stock Core Light": 0.15, "Commodities": 0.06
        },
        "Moderate Small Account": {
            "Cash": 0.01, "AGG": 0.11, "IYR": 0.05, "PRUFX": 0.10, "PRRIX": 0.12,
            "SMDV": 0.10, "SPLG": 0.15, "VBK": 0.08, "VIG": 0.10, "ARGT": 0.07, "PFF": 0.11
        }
    },
    "Moderate Aggressive": {
        "Moderate Aggressive Full": {
            "Cash": 0.01, "Dividend": 0.10, "Fixed Core Full": 0.08, "Fixed Individuals": 0.08,
            "Commodities": 0.10, "LargeCap": 0.09, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.10, "Stock Core": 0.34
        },
        "Moderate Aggressive Lite": {
            "Cash": 0.01, "Fixed Core Lite & Small": 0.16, "LargeCap": 0.27, "Real Estate": 0.10, 
            "Sm/Md Cap Funds": 0.21, "Stock Core Light": 0.15, "Commodities": 0.10
        },
        "Moderate Aggressive Small Account": {
            "Cash": 0.01, "AGG": 0.06, "IYR": 0.07, "PRUFX": 0.13, "PRRIX": 0.06, "SMDV": 0.12, 
            "SPLG": 0.20, "VBK": 0.10, "VIG": 0.12, "ARGT": 0.07, "PFF": 0.06
        }
    },
    "Aggressive": {
        "Aggressive Full": {
            "Cash": 0.01, "Dividend": 0.10, "Fixed Core Lite & Small": 0.05, "Commodities": 0.10, 
            "LargeCap": 0.12, "Real Estate": 0.10, "Sm/Md Cap Funds": 0.13, "Stock Core": 0.39
        }
    }
}

# Subcategories (Fixed formatting and category naming)
sub_categories = {
    "Dividend": {
        "VZ": 0.12, "JNJ": 0.12, "DOW": 0.12, "MRK": 0.12,
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
    "Commodities": {
        "URA": 0.25, "COM": 0.25, "GLD": 0.50
    },
    "Stock Core": {
        "AAPL": 0.0217, "ABBV": 0.0217, "ABNB": 0.0217, "AMZN": 0.0652, "CHKP": 0.0217, 
        "COST": 0.0217, "CRWD": 0.0217, "CVX": 0.0217, "DOCS": 0.0217, "NVDA": 0.0217, 
        "DVA": 0.0217, "PAYO": 0.0217, "FDX": 0.0217, "GOOGL": 0.0217, "GS": 0.0217,
        "JPM": 0.0217, "KO": 0.0217, "LLY": 0.0217, "LOW": 0.0217, "MA": 0.0217, 
        "MMM": 0.0217, "MSFT": 0.0217, "NFLX": 0.0217, "NTNX": 0.0217, "ODFL": 0.0217, 
        "QCOM": 0.0217, "REGN": 0.0217, "SBUX": 0.0217, "SPOT": 0.0217, "STLD": 0.0217, 
        "STZ": 0.0217, "TSLA": 0.0435, "T": 0.0217, "UL": 0.0217, "ULTA": 0.0217, "V": 0.0217, 
        "VZ": 0.0217, "INTC": 0.0217, "EXC": 0.0217, "GNRC": 0.0217, "MP": 0.0217, 
        "MTN": 0.0217, "WFC": 0.0217
    },
    "Stock Core Light": {
        "AAPL": 0.0625, "AMZN": 0.1250, "COST": 0.0625, "CVX": 0.0625, "DOCS": 0.0625, "FDX": 0.0625,
        "JPM": 0.0625, "LLY": 0.0625, "MMM": 0.0625, "SBUX": 0.0625, "TSLA": 0.1250, "T": 0.0625, "UL": 0.0625, "V": 0.0625
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
