import streamlit as st

SINGLE = "single"
MARRIED = "married"
HOH = "head of household"

STANDARD_DEDUCTION = {
    SINGLE: 16100,
    (MARRIED, "yes"): 32200,
    (MARRIED, "no"): 16100,
    HOH: 24150,
}

STANDARD_MILEAGE_RATE = 0.725

CHILD_TAX_CREDIT_PER_CHILD = 2200
CTC_PHASEOUT_START = {
    SINGLE: 200000,
    MARRIED: 400000,
    HOH: 200000,
}
CTC_PHASEOUT_RATE = 50

ADOPTION_CREDIT_AMOUNT = 17670
ADOPTION_PHASEOUT_START = 216660
ADOPTION_REFUNDABLE_PORTION = 5000

SAVERS_CREDIT_RATE = {0.50, 0.20, 0.10, 0.0}

BRACKETS = { # 2026 tax year (lower limit(of bracket), upper limit(of bracket), tax rate, base taxable amount)
    SINGLE: [
        {"lower": 0, "upper": 12400, "rate": 0.10, "base": 0},
        {"lower": 12400, "upper": 50400, "rate": 0.12, "base": 1250},
        {"lower": 50400, "upper": 105700, "rate": 0.22, "base": 5800},
        {"lower": 105700, "upper": 201775, "rate": 0.24, "base": 17966},
        {"lower": 201775, "upper": 256225, "rate": 0.32, "base": 41024},
        {"lower": 256225, "upper": 640600, "rate": 0.35, "base" :58448},
        {"lower": 640600, "upper": float("inf"), "rate": 0.37, "base": 192979.25}
    ],

    (MARRIED, "yes"): [
        {"lower": 0, "upper": 24800, "rate": 0.10,"base": 0},
        {"lower": 24800, "upper": 100800, "rate": 0.12, "base": 2480},
        {"lower": 100800, "upper": 211400, "rate": 0.22, "base": 11600},
        {"lower": 211400, "upper": 403550, "rate": 0.24, "base": 35932},
        {"lower": 403550, "upper": 512450, "rate": 0.32, "base": 82048},
        {"lower": 512450, "upper": 768700, "rate": 0.35, "base": 116896},
        {"lower": 768700, "upper": float("inf"), "rate": 0.37, "base": 206583.50}
    ],

    (MARRIED, "no"): [
        {"lower": 0, "upper": 12400, "rate": 0.10, "base": 0},
        {"lower": 12400, "upper": 50400, "rate": 0.12, "base": 1240},
        {"lower": 50400, "upper": 105700, "rate": 0.22, "base": 5800},
        {"lower": 105700, "upper": 201775, "rate": 0.24, "base": 17966},
        {"lower": 201775, "upper": 256225, "rate": 0.32, "base": 41024},
        {"lower": 256225, "upper": 384350, "rate": 0.35, "base": 58448},
        {"lower": 384350, "upper": float("inf"), "rate": 0.37, "base": 103291.75}
    ],

    HOH: [ 
        {"lower": 0, "upper": 17700, "rate": 0.10, "base": 0},
        {"lower": 17700, "upper": 67450, "rate": 0.12, "base": 1770},
        {"lower": 67450, "upper": 105700, "rate": 0.22, "base": 7740},
        {"lower": 105700, "upper": 201750, "rate": 0.24, "base": 16155},
        {"lower": 201750, "upper": 256200, "rate": 0.32,"base": 39207},
        {"lower": 256200, "upper": 640600, "rate": 0.35, "base": 56631},
        {"lower": 640600, "upper": float("inf"), "rate": 0.37, "base": 191171}
    ],
}

def get_filing_status_key(status, jointly=False):
    if status == MARRIED:
        return (MARRIED, 'yes' if jointly else 'no')
    return status 

def calculate_deduction(status, jointly=False):
    key = get_filing_status_key(status, jointly)
    return STANDARD_DEDUCTION.get(key, 16100)

def calculate_taxable_income(
    gross_income,
    status,
    jointly=False,
    dependents=0,
    adoption_credit_amount=0,
):
    deduction = calculate_deduction(status, jointly)
    dependent_credit_amount = dependents * CHILD_TAX_CREDIT_PER_CHILD
    return max(gross_income - deduction - dependent_credit_amount - adoption_credit_amount, 0)
    

def calculate_tax(taxable_income, status, jointly=False):
    key = get_filing_status_key(status, jointly)
    for bracket in BRACKETS[key]:
        if taxable_income >= bracket["lower"] and taxable_income <= bracket["upper"]:
            return bracket["base"] + (taxable_income - bracket["lower"]) * bracket["rate"]
    return 0

def calculate_total_tax(
    gross_income,
    status,
    jointly=False,
    dependents=0,
    adoption_credit=False,
):
    adoption_credit_amount = ADOPTION_CREDIT_AMOUNT if adoption_credit else 0
    taxable_income = calculate_taxable_income(
        gross_income,
        status,
        jointly,
        dependents,
        adoption_credit_amount,
    )
    return calculate_tax(taxable_income, status, jointly)

# streamlit ui
st.title("2026 Federal Tax Calculator")
st.caption("For Educational Use Only")

col1, col2 = st.columns(2)

with col1: 
    gross_income = st.number_input("Gross Income ($)", min_value=0, value=30000, step=1000)
    filing_status = st.selectbox("Filing Status", [SINGLE, MARRIED, HOH])

with col2:
    if filing_status == MARRIED:
        married_jointly = st.radio("Filing jointly?", ["Yes (Married Filing Jointly)", "No (Married Filing Seperately)"], horizontal=True)
        jointly = married_jointly.startswith("Yes")
    else:
        jointly = False

if st.button("Calculate Tax", type="primary"):
    taxable = calculate_taxable_income(gross_income, filing_status, jointly)
    tax = calculate_tax(taxable, filing_status, jointly)
    effective_rate = (tax / gross_income * 100) if gross_income > 0 else 0

    st.success("--Results--")
    st.metric("Taxable Income", f"${taxable:,.0f}")
    st.metric("Federal Income Tax", f"${tax:,.0f}")
    st.metric("Effective Tax Rate", f"{effective_rate:.1f}%")

    # bracket viz
    st.subheader("Tax Breakdown")
    key = get_filing_status_key(filing_status, jointly)
    for bracket in BRACKETS[key]:
        if bracket["upper"] == float("inf"):
            upper = "inf"
        else:
            upper = f"${bracket['upper']:,.0f}"
        st.text(f"${bracket['lower']:,.0f} - {upper} @ {bracket['rate']*100:.0f}%")


