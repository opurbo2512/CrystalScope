#import libaray and crystal_structure class
import streamlit as st
from crystal import CrystalStructure

#set page configuration
st.set_page_config(
    page_title="Crystallographical analysis",
    page_icon = "🔬",
    layout = "wide"
    )

#setting captions
st.markdown("""
# 🔬 Crystal Structure Analyzer

Analyze and visualize crystal structures from:

✅ Chemical Formula

✅ CIF File

✅ Materials Project ID

Powered by Pymatgen + Materials Project API
""")

#making a object
cs = CrystalStructure()

#selecting input type
with st.sidebar:
    st.caption("Input")
    inp_type = st.selectbox("Select input type:",["chemical formula","cif file","mp-id"])
    #giving info about the input
    st.info("""
        Examples:

        • Formula → Fe2O3

        • MP-ID → mp-13

        • CIF → Upload a .cif file
    """)

#taking input for different type
if inp_type == "cif file":
    st.subheader("Upload cif File")
    file = st.file_uploader(
        "Chose an image",
        type = "cif"
    )
    if file is not None:
        data = file.getvalue().decode("utf-8")
    
elif inp_type == "chemical formula":
    data = st.text_input("Enter the formula:")

elif inp_type == "mp-id":
    data = st.text_input("Enter the material project(mp) id:")

#making analyzer button
b = st.button(
    "🚀 Analyze Structure",
    use_container_width=True
)

#collecting all the data
if b:
    #making spinner for waiting
    with st.spinner("Collecting data..."):
        try:
            #making structure from data
            if inp_type == "cif file":
                structure , sga = cs.file_to_structure(data)
            elif inp_type == "chemical formula":
                if not cs.is_valid_formula(data):
                    st.error("It is not a valid chemical formula")
                    st.warning("A valid chemical formula is like (Fe2SO4) or (Fe4).")

                structure , sga = cs.formula_to_structure(data)
            elif inp_type == "mp-id":
                if not cs.is_valid_mp_id(data):
                    st.error("It is a invalid mp id")
                    st.warning("The standard form of a mp id is 'mp-13'. First two character will be mp and then (-).Then there will be a number.")
                structure , sga = cs.mp_id_to_structure(data)

            #collecting data
            formula = cs.get_formula(structure)
            lattice_df = cs.get_lattice_parameters(structure)
            volume = cs.get_volume(structure)
            density = cs.get_density(structure)
            no_sites = cs.get_no_of_sites(structure)
            space_group_symbol, space_group_number = cs.get_space_group(sga)
            crystal_system = cs.get_crystal_system(sga)
            lattice_system = cs.get_lattice_system(sga)
            no_cor = cs.get_co(structure)

            view = cs.creating_3d_model(structure)
            st.success("Data collection complete")

            show = True

        except:
            st.error("There are error in your information" \
            "Give correct information and try again.")
            show = False

    if show:

        #making tabs
        tab1 , tab2 , tab3 = st.tabs(["📈 Properties", "🏗 Structure", "📄 Raw Data"])
        with tab1:
            st.subheader("📊 Structure Summary")
            #showing data as metric
            c1,c2,c3 = st.columns(3)
            with c1:
                st.metric(
                    "Chemical Formula",
                    formula
                )
                st.metric(
                    "Vomume (Ang^3)",
                    round(volume,4)
                )
                st.metric(
                    "Density (gm/cm^3)",
                    round(density,4)
                )

            with c2:
                st.metric(
                    "No of sites",
                    no_sites
                )
                st.metric(
                    "Space group symbol",
                    space_group_symbol
                )
                st.metric(
                    "Space group number",
                    space_group_number
                )

            with c3:
                st.metric(
                    "Crystal system",
                    crystal_system
                )
                st.metric(
                    "Lattice system",
                    lattice_system
                )
                st.metric(
                    "number of coordinate",
                    no_cor
                )
        with tab3:
            #showing data as dataframe
            st.subheader("Lattice Parameters:")
            st.dataframe(
                lattice_df,
                use_container_width=True,
                hide_index=True
            )

        with tab2:
            #showing the 3d picture
            st.subheader("3D model of the componets")
            html = view._make_html()
            st.components.v1.html(
                html,
                height = 600,
                width = 800
            )

