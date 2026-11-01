from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from auth import authenticate_customer, initialise_database, register_customer, reset_customer_password


st.set_page_config(page_title="OilPulse | Global Oil Intelligence", page_icon="🛢️", layout="wide", initial_sidebar_state="collapsed")
ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "World_Oil_Operations_Practice_Dataset.xlsx"
initialise_database()


@st.cache_data
def load_data():
    frame = pd.read_excel(DATA_FILE, sheet_name="Oil Data")
    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    return frame


def money(value):
    return f"${value / 1_000:,.1f}bn"


st.markdown("""
<style>
#MainMenu, header, footer, [data-testid="stSidebar"] {display:none!important}
.stApp {background:linear-gradient(145deg,#030a20 0%,#071936 55%,#041126 100%);color:#eaf2ff}
.block-container{padding:1.15rem 2.4rem 3rem;max-width:1500px} h1,h2,h3{color:#fff!important}
.brand{font-weight:900;font-size:1.42rem;letter-spacing:-.04em;color:#fff}.brand span{color:#2f75ff}
.eyebrow{color:#68a3ff;font-size:.75rem;font-weight:800;letter-spacing:.15em;text-transform:uppercase}
.hero{padding:4.2rem 3.2rem;border:1px solid #1d3970;border-radius:26px;background:radial-gradient(circle at 80% 25%,#17499c 0,#0b2454 25%,#050d25 66%);box-shadow:0 26px 70px #010715;margin:.8rem 0 1.2rem;overflow:hidden}
.hero h1{font-size:clamp(2.4rem,5vw,5.5rem)!important;line-height:.95;letter-spacing:-.06em;max-width:900px;margin:.75rem 0 1rem}.hero p{font-size:1.1rem;max-width:760px;color:#b8c9e8}
.headline{background:#0b1d3c;border:1px solid #294d86;border-left:5px solid #397dff;border-radius:14px;padding:1rem 1.25rem;color:#eaf2ff;font-weight:700;margin-bottom:1rem}
.card{background:linear-gradient(160deg,#0c2144,#08172f);border:1px solid #1f4175;border-radius:18px;padding:1.35rem;height:100%;box-shadow:0 12px 28px #020817}.card p{color:#aabbd8}.blue{color:#5d96ff}.pill{display:inline-block;background:#173b80;color:#dbe9ff;padding:.32rem .72rem;border-radius:999px;font-size:.75rem;font-weight:800}
[data-testid="stMetric"]{background:#091a36;border:1px solid #21467c;border-radius:16px;padding:1.05rem;box-shadow:0 10px 25px #010713}[data-testid="stMetricValue"]{color:#fff}[data-testid="stMetricLabel"]{color:#9eb4d8}
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button{border:0;border-radius:999px;background:#2868f5;color:#fff;font-weight:800;padding:.55rem 1.25rem}.stButton>button:hover,.stDownloadButton>button:hover{background:#4a82ff;color:#fff}
[data-baseweb="tab-list"]{gap:.5rem}[data-baseweb="tab"]{background:#0a1b37;border-radius:999px;padding:.5rem 1rem;color:#c8d7ef}
.social a{display:inline-block;margin:.25rem .45rem .25rem 0;padding:.55rem .9rem;border:1px solid #2a4c80;border-radius:999px;color:#dbe8ff!important;text-decoration:none}.small{color:#8fa5c8;font-size:.86rem}.footer{margin-top:2.4rem;padding:1.5rem 0;border-top:1px solid #17355f;color:#8fa5c8}
</style>
""", unsafe_allow_html=True)


def account_page():
    st.markdown('<div class="brand">OIL<span>PULSE</span></div>', unsafe_allow_html=True)
    st.markdown("""<section class="hero"><div class="eyebrow">Global operational intelligence</div>
    <h1>See the pulse of world oil operations.</h1><p>Explore production, sales, revenue, profit and downtime through a secure student-built analytics experience.</p></section>""", unsafe_allow_html=True)
    login, register, forgot = st.tabs(["Login", "Customer registration", "Forgot password"])
    with login:
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")
        if submitted:
            customer = authenticate_customer(username, password)
            if customer:
                st.session_state.customer = customer
                st.rerun()
            st.error("Incorrect username or password.")
    with register:
        with st.form("register", clear_on_submit=True):
            a, b = st.columns(2)
            full_name = a.text_input("Full name")
            dob = b.date_input("Date of birth", value=None, min_value=date(1900,1,1), max_value=date.today())
            address = st.text_area("Home address")
            email = st.text_input("Recovery email")
            username = st.text_input("Create a username")
            p1 = st.text_input("Create a password", type="password")
            p2 = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", type="primary")
        if submitted:
            if p1 != p2:
                st.error("The passwords do not match.")
            else:
                ok, message = register_customer(username, full_name, address, dob, email, p1)
                (st.success if ok else st.error)(message)
    with forgot:
        st.info("This educational version verifies your registered details locally. A public deployment should send a time-limited email token.")
        with st.form("forgot", clear_on_submit=True):
            username = st.text_input("Registered username")
            email = st.text_input("Recovery email")
            dob = st.date_input("Date of birth", value=None, min_value=date(1900,1,1), max_value=date.today())
            p1 = st.text_input("New password", type="password")
            p2 = st.text_input("Confirm new password", type="password")
            submitted = st.form_submit_button("Reset password", type="primary")
        if submitted:
            if p1 != p2:
                st.error("The passwords do not match.")
            else:
                ok, message = reset_customer_password(username, email, dob, p1)
                (st.success if ok else st.error)(message)


if "customer" not in st.session_state:
    account_page()
    st.stop()

df = load_data()
top1, top2, top3 = st.columns([5, 1.2, 1])
top1.markdown('<div class="brand">OIL<span>PULSE</span></div><div class="small">Global operations intelligence</div>', unsafe_allow_html=True)
top2.markdown(f"<div class='small'>Signed in as</div><b>{st.session_state.customer['full_name']}</b>", unsafe_allow_html=True)
if top3.button("Log off", use_container_width=True):
    del st.session_state["customer"]
    st.rerun()

page = st.radio("Navigation", ["Home", "Analytics", "Data Explorer", "About Project", "Contact & Social"], horizontal=True, label_visibility="collapsed")

if page == "Home":
    st.markdown("""<section class="hero"><div class="eyebrow">OilPulse intelligence platform</div><h1>Your gateway to global oil data.</h1>
    <p>Turn twelve years of synthetic operational records into clear, decision-ready insight. Built for learning, analysis and a professional student portfolio.</p></section>""", unsafe_allow_html=True)
    st.markdown('<div class="headline">OIL DATA 2015–2026 &nbsp; • &nbsp; Filter by year, region and country &nbsp; • &nbsp; Production, sales, revenue, profit and downtime</div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.markdown('<div class="card"><span class="pill">12 YEARS</span><h3>Global coverage</h3><p>Compare 15 producing countries across five regions with consistent monthly operational records.</p></div>', unsafe_allow_html=True)
    b.markdown('<div class="card"><span class="pill">SECURE</span><h3>Customer access</h3><p>Local registration, salted password hashing, login, logoff and recovery-email password reset.</p></div>', unsafe_allow_html=True)
    c.markdown('<div class="card"><span class="pill">PORTFOLIO</span><h3>Decision-ready</h3><p>Interactive charts and filtered CSV export demonstrate practical Python data-analysis skills.</p></div>', unsafe_allow_html=True)
    st.subheader("Start exploring")
    st.write("Choose **Analytics** above to filter the dashboard, or **Data Explorer** to inspect and download individual records.")

elif page == "Analytics":
    st.markdown('<div class="headline">ANALYTICS WORKSPACE — 2015–2026 GLOBAL OIL OPERATIONS</div>', unsafe_allow_html=True)
    f1,f2,f3 = st.columns(3)
    years = f1.multiselect("Year", sorted(df.Year.unique()), default=sorted(df.Year.unique()))
    regions = f2.multiselect("Region", sorted(df.Region.unique()), default=sorted(df.Region.unique()))
    available = sorted(df.loc[df.Region.isin(regions), "Country"].unique())
    countries = f3.multiselect("Country", available, default=available)
    data = df[df.Year.isin(years) & df.Region.isin(regions) & df.Country.isin(countries)].copy()
    if data.empty:
        st.warning("Select at least one year, region and country.")
        st.stop()
    revenue = data.Revenue_USD_m.sum(); profit = data.Operating_Profit_USD_m.sum()
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("Production", f"{data.Production_Mbbl.sum():,.0f} Mbbl")
    m2.metric("Sales", f"{data.Sales_Volume_Mbbl.sum():,.0f} Mbbl")
    m3.metric("Revenue", money(revenue)); m4.metric("Profit", money(profit))
    m5.metric("Downtime", f"{data.Unplanned_Downtime_pct.mean():.1f}%")
    monthly = data.groupby("Date", as_index=False).agg(Production_Mbbl=("Production_Mbbl","sum"),Sales_Volume_Mbbl=("Sales_Volume_Mbbl","sum"),Revenue_USD_m=("Revenue_USD_m","sum"),Operating_Profit_USD_m=("Operating_Profit_USD_m","sum"),Unplanned_Downtime_pct=("Unplanned_Downtime_pct","mean"))
    charts = [("Production_Mbbl","Production trend","#3a7cff"),("Sales_Volume_Mbbl","Sales trend","#22c9a9"),("Revenue_USD_m","Revenue trend","#f4b942"),("Operating_Profit_USD_m","Profit trend","#a978ff"),("Unplanned_Downtime_pct","Downtime trend","#ff637d")]
    for row in (charts[:2], charts[2:4]):
        cols = st.columns(2)
        for col,(field,title,colour) in zip(cols,row):
            fig=px.area(monthly,x="Date",y=field,title=title);fig.update_traces(line_color=colour,fillcolor=colour);fig.update_layout(template="plotly_dark",paper_bgcolor="#07152e",plot_bgcolor="#07152e")
            col.plotly_chart(fig,use_container_width=True)
    fig=px.line(monthly,x="Date",y="Unplanned_Downtime_pct",title="Average unplanned downtime",markers=True);fig.update_traces(line_color="#ff637d");fig.update_layout(template="plotly_dark",paper_bgcolor="#07152e",plot_bgcolor="#07152e")
    st.plotly_chart(fig,use_container_width=True)

elif page == "Data Explorer":
    st.markdown('<div class="headline">DATA EXPLORER — FILTER, REVIEW AND DOWNLOAD</div>', unsafe_allow_html=True)
    a,b,c=st.columns(3)
    year=a.selectbox("Year",["All"]+sorted(df.Year.unique().tolist()))
    region=b.selectbox("Region",["All"]+sorted(df.Region.unique().tolist()))
    country=c.selectbox("Country",["All"]+sorted(df.Country.unique().tolist()))
    data=df.copy()
    if year!="All": data=data[data.Year==year]
    if region!="All": data=data[data.Region==region]
    if country!="All": data=data[data.Country==country]
    st.metric("Matching records",f"{len(data):,}")
    st.dataframe(data,use_container_width=True,height=480)
    st.download_button("Download filtered CSV",data.to_csv(index=False).encode("utf-8"),"oilpulse_filtered_data.csv","text/csv")

elif page == "About Project":
    st.markdown("""<section class="hero"><div class="eyebrow">Student portfolio project</div><h1>About OilPulse.</h1>
    <p>OilPulse is an educational Python data-analysis application created to demonstrate how operational data can support clear business decisions.</p></section>""", unsafe_allow_html=True)
    left,right=st.columns(2)
    left.markdown("""<div class="card"><h3>Purpose</h3><p>The project turns complex oil-operation records into accessible KPIs, charts and downloadable evidence. It demonstrates Python, Pandas, Plotly, Streamlit, SQLite, authentication and responsive interface design.</p><p>The figures are entirely synthetic and must not be treated as official statistics, financial advice or live market information.</p></div>""",unsafe_allow_html=True)
    right.markdown("""<div class="card"><h3>Student learning outcomes</h3><p>• Prepare and validate structured data<br>• Apply business-focused filters<br>• Communicate trends with charts<br>• Protect passwords using salted hashing<br>• Design an accessible multi-page app<br>• Explain limitations and ethical data use</p></div>""",unsafe_allow_html=True)
    st.subheader("Technology used")
    st.write("Python · Streamlit · Pandas · Plotly · SQLite · PBKDF2-HMAC-SHA256 · Excel/CSV")

else:
    st.markdown("""<section class="hero"><div class="eyebrow">Connect with the project</div><h1>Contact & social media.</h1><p>Follow the student portfolio, view related projects and share OilPulse with your learning network.</p></section>""",unsafe_allow_html=True)
    st.markdown("""<div class="social">
    <a href="https://www.linkedin.com/in/rajakokila-periyathamby-4b3689120/" target="_blank">LinkedIn</a>
    <a href="https://github.com/Rajakokila-P" target="_blank">GitHub</a>
    <a href="https://www.instagram.com/" target="_blank">Instagram</a>
    <a href="https://www.facebook.com/" target="_blank">Facebook</a>
    <a href="https://x.com/" target="_blank">X / Twitter</a></div>""",unsafe_allow_html=True)
    st.info("The LinkedIn and GitHub links use your portfolio addresses. Replace the Instagram, Facebook and X links in app.py with your own profile addresses when ready.")
    st.markdown("""<div class="card"><h3>Project statement</h3><p>OilPulse was developed as a student portfolio application to demonstrate practical data analysis, secure account handling and professional dashboard design. It uses synthetic practice data covering 2015–2026 and is intended solely for education and skills development.</p></div>""",unsafe_allow_html=True)

st.markdown('<div class="footer">OilPulse © 2026 · Educational portfolio project · Synthetic practice data · Not financial advice</div>',unsafe_allow_html=True)
