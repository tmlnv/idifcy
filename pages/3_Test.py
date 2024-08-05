import json

import streamlit as st
from ifctester import ids, reporter

from pages.components.constants import MSG_UPLOAD_FILE_REQ
from pages.components.custom_sidebar import custom_sidebar
from pages.components.ids_check_res_df import create_specifications_dataframe
from pages.components.load_data import load_data

session = st.session_state


def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False
    if "IdsFile" not in session:
        session["IdsFile"] = None
    session["IdsReport"] = None
    session["IdsReportDF"] = None


def upload_ids_file():
    ids_file = st.file_uploader("Choose an IDS file", type=["ids"], key="uploaded_file")
    if ids_file:
        my_ids = ids.open(ids_file)
        session["IdsFile"] = my_ids


def print_ids_as_dict():
    for spec in session["IdsFile"].specifications:
        st.write(spec.asdict())


def run_ids_test():
    ids_info = session["IdsFile"].info

    try:
        ids_author = ids_info["author"]
    except KeyError:
        ids_author = "Неизвестный автор"

    st.write(f'Ids specification: **{ids_info["title"]}**, author: {ids_author}')

    is_finished = False

    while not is_finished:
        with st.spinner("Quality control in progress"):
            session["IdsFile"].validate(session["ifc_file"])

            report = reporter.Json(session["IdsFile"]).report()
            session["IdsReport"] = report

            session["IdsReportDF"] = create_specifications_dataframe(report)

        is_finished = True


def execute():
    st.set_page_config(
        page_title="IFC Model AQA",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("File testing")

    if "IsDataFrameLoaded" not in session:
        initialize_session_state()

    if not session.IsDataFrameLoaded:
        load_data()

    if session.IsDataFrameLoaded:
        tab1, tab2, tab3 = st.tabs(["Test", "IDS Specification", "IDS Results"])
        with tab1:
            st.header("Test")

            upload_ids_file()

            if session["IdsFile"]:
                if st.button(
                    "Conduct quality check",
                    key="run_ids_test",
                    help="Conduct the test according to the IDS specification",
                ):
                    run_ids_test()
                if session.get("IdsReportDF"):
                    st.header("Test results")
                    st.write(session["IdsReportDF"])

        with tab2:
            st.header("IDS Specification")
            if session["IdsFile"]:
                print_ids_as_dict()
            else:
                st.write("Upload IDS file on the 'Test' tab to view the specification")

        with tab3:
            st.header("IDS Results")
            if ids_report := session.get("IdsReport"):
                st.header("Test results")
                st.download_button(
                    "Download JSON",
                    file_name="IDS_RES_" + session.file_name.replace("ifc", ".json"),
                    data=json.dumps(ids_report),
                )
                st.write(ids_reports)
            else:
                st.write("Upload IDS file on the 'Tests' tab and conduct test by pressing 'Run IDS tests' button")

    else:
        st.header(MSG_UPLOAD_FILE_REQ)

    custom_sidebar()


execute()
