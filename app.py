import streamlit as st

# set page title and favicon
st.set_page_config(page_title="Sucafina Standardizer", page_icon=":coffee:", layout="wide")

# instead of those columns, set the display to flex and align items to center, then add the logo and title in a row layout
st.markdown(
    """
    <style>
    .title {
        display: flex;
        flex-direction: column;
        align-items: center;
        }
    .title-row {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .title-row img {
        margin-right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="title">
    <div class="title-row">
        <img src="https://group.sucafina.com/themes/sucafina/assets/img/base/logo.svg" width="150">
        <h5>STANDARDIZER</h5>
    </div>
    </div>
    """,
    unsafe_allow_html=True
)


# set divider
st.markdown("---")

# app main content

# set 2 content columns with width ratio 1:4

contentCol1, contentCol2, contentCol3 = st.columns([2, 0.5, 4])
with contentCol1:
    # add load data section
    st.header("Data")
    
    # input file uploader
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "geojson", "kml"])
    
    # file type with number of records
    # if it is a csv or xlsx file, prompt user to specify the number of header rows to skip
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "csv":
            import pandas as pd
            num_header_rows = st.number_input("Number of header rows to skip", min_value=0, value=0)
            data = pd.read_csv(uploaded_file, skiprows=num_header_rows)
            num_records = len(data)
        elif file_type == "xlsx":
            import pandas as pd
            data = pd.read_excel(uploaded_file)
            num_records = len(data)
        elif file_type in ["geojson", "kml"]:
            import geopandas as gpd
            data = gpd.read_file(uploaded_file)
            num_records = len(data)
        st.success(f"{file_type.upper()} - {num_records} records")

    # add a section to preview the uploaded data in form of a table, the table should be scrollable if there are many records
    # st.subheader("Data Preview")
    if uploaded_file is not None:
        st.dataframe(data)

with contentCol2: # empty column for spacing
    pass    

with contentCol3:
    # add attribute mapping section
    st.header("Attribute Mapping")
    st.subheader("Plot Attributes")

    # subsection for Origin, Supplier Code, and Supply Chain
    # arrange the three attributes in a row with equal width and use a combo box for Origin
    originCol, supplierCodeCol, supplyChainCol = st.columns(3)
    with originCol:
        origin_options = ["Brazil", "Colombia", "Costa Rica", "Ethiopia", "Guatemala", "Honduras", "India", "Indonesia", "Kenya", "Laos", "Mexico", "Nicaragua", "Peru", "Rwanda", "Tanzania", "Uganda", "Vietnam"]
        selected_origin = st.selectbox("Origin", options=origin_options)

    with supplierCodeCol:
        supplier_code = st.text_input("Supplier Code")

    with supplyChainCol:
        supply_chain = st.text_input("Supply Chain")

    # ... (inside your contentCol3 block)

    plotIDCol, farmerIDCol, plotRegionCol, plotDistrictCol = st.columns(4)

    if uploaded_file is not None:
        # 1. Prepare options: Add a special "--- Manual Entry ---" option at the top
        columns = ["NULL", "--- Manual Entry ---"] + data.columns.tolist()
        
        # Define a helper function to handle the logic for each field to keep code DRY
        def get_mapped_value(label, key_suffix):
            selection = st.selectbox(label, options=columns, key=f"sel_{key_suffix}")
            if selection == "--- Manual Entry ---":
                # If manual entry is chosen, show a text input
                return st.text_input(f"Enter {label} manually", key=f"txt_{key_suffix}")
            if selection == "NULL":
                return None
            return selection

        with plotIDCol:
            plot_id_val = get_mapped_value("Plot ID", "pid")

        with farmerIDCol:
            farmer_id_val = get_mapped_value("Farmer ID", "fid")

        with plotRegionCol:
            plot_region_val = get_mapped_value("Plot Region", "preg")

        with plotDistrictCol:
            plot_district_val = get_mapped_value("Plot District", "pdist")
    # subsection for certications. use checkbox for each to set true or false value
    st.subheader("Certifications")
    
    # arrange the certifications in a row layout with equal width
    # keep the number of columns variable depending on the number of certifications
    certification_options = ["Is Geodata Validated?", "Cafe Practices", "RFA_UTZ", "Impact", "Organic", "4C", "Fair Trade", "Other"]
    num_certifications = len(certification_options)
    cert_columns = st.columns(num_certifications)
    certifications = {}
    for i, cert in enumerate(certification_options):
        with cert_columns[i]:
            certifications[cert] = st.checkbox(cert)

    # add a section for Geometry mapping
    st.header("Geometry Mapping")

    # we shall add buttons that represent the different geometry fixes to be applied to the data, the buttons will be arranged in a row layout, but let us do that later

    # using state display a table (standardized data) with the following columns: sucafina_plot_id, supplier_plot_id, farmer_id, supplier_code, plot_region, plot_district, plot_area_ha, plot_longitude, plot_latitude, plot_gps_point, plot_gps_polygon, plot_wkt, is_geodata_validated, is_cafe_practices_certified, is_rfa_utz_certified, is_impact_certified, is_organic_certified, is_4c_certified, is_fairtrade_certified, other_certification_name, plot_supply_chain, and plot_farmer_group
    # initially the table will be empty, but once the attributes are mapped and the geometry fixed, the table will be populated with the standardized data
    if uploaded_file is not None:
        standardized_data = {
            "sucafina_plot_id": [],
            "supplier_plot_id": [],
            "farmer_id": [],
            "supplier_code": [],
            "plot_region": [],
            "plot_district": [],
            "plot_area_ha": [],
            "plot_longitude": [],
            "plot_latitude": [],
            "plot_gps_point": [],
            "plot_gps_polygon": [],
            "plot_wkt": [],
            "is_geodata_validated": [],
            "is_cafe_practices_certified": [],
            "is_rfa_utz_certified": [],
            "is_impact_certified": [],
            "is_organic_certified": [],
            "is_4c_certified": [],
            "is_fairtrade_certified": [],
            "other_certification_name": [],
            "plot_supply_chain": [],
            "plot_farmer_group": []
        }
        st.dataframe(standardized_data)

        