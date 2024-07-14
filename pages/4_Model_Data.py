import streamlit as st

from pages.components.constants import MSG_UPLOAD_FILE_REQ
from pages.components.custom_sidebar import custom_sidebar
from pages.components.load_data import load_data
from tools import pandashelper
from tools import graph_maker

session = st.session_state


def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


def download_csv():
    pandashelper.download_csv(session.file_name, session.DataFrame)


def execute():
    st.set_page_config(
        page_title="IFC Model Quantities",
        page_icon="🔩",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("Данные модели")
    if "IsDataFrameLoaded" not in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:
        tab1, tab2 = st.tabs(["Dataframe Utilities", "Quantities Review"])
        with tab1:
            ## DATAFRAME REVIEW
            st.header("DataFrame Review")
            st.write(session.DataFrame)
            st.download_button(
                "Download CSV", file_name=session.file_name.replace("ifc", ".csv"), data=session.DataFrame.to_csv()
            )
            st.download_button(
                "Download JSON", file_name=session.file_name.replace("ifc", ".json"), data=session.DataFrame.to_json()
            )
        with tab2:
            row2col1, row2col2 = st.columns(2)
            with row2col1:
                if session.IsDataFrameLoaded:
                    class_selector = st.selectbox("Select Class", session.Classes, key="class_selector")
                    session["filtered_frame"] = pandashelper.filter_dataframe_per_class(
                        session.DataFrame, session.class_selector
                    )
                    session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame"])
                    if session["qtos"] is not None:
                        qto_selector = st.selectbox("Select Quantity Set", session.qtos, key="qto_selector")
                        quantities = pandashelper.get_quantities(session.filtered_frame, session.qto_selector)
                        st.selectbox("Select Quantity", quantities, key="quantity_selector")
                        st.radio("Split per", ["Level", "Type"], key="split_options")
                    else:
                        st.warning("No Quantities to Look at !")
            ## DRAW FRAME
            with row2col2:
                if "quantity_selector" in session and session.quantity_selector == "Count":
                    total = pandashelper.get_total(session.filtered_frame)
                    st.write(f"The total number of {session.class_selector} is {total}")
                else:
                    if session.qtos is not None:
                        st.subheader(f"{session.class_selector} {session.quantity_selector}")
                        graph = graph_maker.load_graph(
                            session.filtered_frame,
                            session.qto_selector,
                            session.quantity_selector,
                            session.split_options,
                        )
                        st.plotly_chart(graph)
    else:
        st.header(MSG_UPLOAD_FILE_REQ)

    custom_sidebar()


execute()
