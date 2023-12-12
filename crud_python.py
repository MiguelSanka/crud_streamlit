import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Vendors Managament Portal")
st.markdown("Enter the data of the new vendor")

con = st.experimental_connection("gsheets", type=GSheetsConnection)

data = con.read(worksheet="Vendors", usecols=list(range(6)), ttl=5)
data = data.dropna(how="all")

BUSINESS_TYPES = [
    "Manufacturer",
    "Distributor",
    "Wholesaler",
    "Retailer",
    "Service provider"
]

PRODUCTS = [
    "Electronics",
    "Apparel",
    "Groceries"
]

with st.form(key="vendor_form"):
    company_name = st.text_input(label="Company name*")
    business_type = st.selectbox("Business type", options=BUSINESS_TYPES, index=None)
    products = st.multiselect("Products Offered", options=PRODUCTS)
    year_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboard Date")
    additional_info = st.text_area(label="Additional Notes")
    
    st.markdown("**required*")
    submit_button = st.form_submit_button("Submit Vendor Details")

    if submit_button:
        if not company_name or not business_type:
            st.warning("Ensure all mandatory fields are filled")
            st.stop()
        elif data["CompanyName"].str.contains(company_name).any():
            st.warning("A vendor with this company name already exists")
            st.stop()
        else:
            vendor_data = pd.DataFrame(
                [
                    {
                        "CompanyName": company_name,
                        "BusinessType": business_type,
                        "Products": ", ".join(products),
                        "YearsInBusiness": year_in_business,
                        "OnBoardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "AdditionalInfo": additional_info,
                    }
                ]
            )

            updated_df = pd.concat([data, vendor_data], ignore_index=True)

            con.update(worksheet="Vendors", data=updated_df)

            st.success("Vendor details sucessfully submitted!")