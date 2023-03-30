import streamlit as st
from tools import ifchelper

session = st.session_state

def load_data():
    if "ifc_file" in session:
        st.write(dir(session.ifc_file))

def initialize_session_state():
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

def run_tests():
    st.write(dir(session.DataFrame))
    st.write(session.DataFrame.get('Type'))
    obj_types = session.DataFrame.get('Type')
    st.write(type(obj_types))
    counter = 0
    for elem in session.DataFrame.get('Type'):
        try:
            test_type_of_element(elem)
        except AssertionError as e:
            counter += 1
            # st.write(f"Check failed, problem is {dir(e)}")
            # st.write(f"Check failed, problem is {e}")
            # continue
    st.write(f'Total elements failed checking {counter}')

def test_type_of_element(element):
    allowed_types = ['Базовая стена:Внешняя несущая', 'Прямоугольный импост:50 x 150мм', 'Перекрытие:Типовой 200мм', 'Базовая стена:Перегородка из кирпича, 120']

    assert element in allowed_types


def execute():
    st.set_page_config(
        page_title="Quantities",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header("Тестирование файла")
    if not "IsDataFrameLoaded" in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:
        tab1, tab2 = st.tabs(["Dataframe Utilities", "Quantities Review"])
        with tab1:
            ## DATAFRAME REVIEW
            st.header("DataFrame Review")
            st.write(session.DataFrame)
            # from st_aggrid import AgGrid
            # AgGrid(session.DataFrame)

            st.button('Run tests', key="run_tests", on_click=run_tests())

            st.download_button('Download CSV', file_name=session.file_name.replace('ifc', '.csv'),
                               data=session.DataFrame.to_csv())
            st.download_button('Download JSON', file_name=session.file_name.replace('ifc', '.json'),
                               data=session.DataFrame.to_json())
            # st.button("Download CSV", key="download_csv", on_click=download_csv)
            # st.button("Download Excel", key="download_excel", on_click=download_excel)

            st.write(len(session.ifc_file.by_type('IfcWall')))
    else:
        st.header("Загрузите файл на домашней странице")


execute()
