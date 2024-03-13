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
    ids_file = st.file_uploader("Выберите файл IDS", type=["ids"], key="uploaded_file")
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

    st.write(f'Название ids спецификации: **{ids_info["title"]}**, автор: {ids_author}')

    is_finished = False

    while not is_finished:
        with st.spinner("Выполняется проверка качества"):
            session["IdsFile"].validate(session["ifc_file"])

            report = reporter.Json(session["IdsFile"]).report()
            session["IdsReport"] = report

            session["IdsReportDF"] = create_specifications_dataframe(report)

        is_finished = True


def execute():
    st.set_page_config(
        page_title="Test",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("Тестирование файла")

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
                    "Провести проверку качества",
                    key="run_ids_test",
                    help="Провести тест в соответствии с IDS спецификацией",
                ):
                    run_ids_test()
                if session.get("IdsReportDF"):
                    st.header("Результаты проверки")
                    st.write(session["IdsReportDF"])

        with tab2:
            st.header("IDS Specification")
            if session["IdsFile"]:
                print_ids_as_dict()
            else:
                st.write("Загрузите IDS файл на вкладке 'Test' для просмотра спецификации")

        with tab3:
            st.header("IDS Results")
            if ids_report := session.get("IdsReport"):
                st.header("Результаты проверки")
                st.download_button(
                    "Download JSON",
                    file_name="IDS_RES_" + session.file_name.replace("ifc", ".json"),
                    data=json.dumps(ids_report),
                )
                st.write(ids_report)
            else:
                st.write("Загрузите IDS файл на вкладке 'Test' и произведите проверку, нажав на кнопку 'Run IDS tests'")

    else:
        st.header(MSG_UPLOAD_FILE_REQ)

    custom_sidebar()


execute()
