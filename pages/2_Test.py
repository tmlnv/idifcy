from time import sleep

import streamlit as st
import numpy as np
import pandas as pd
from ifctester import ids, reporter

from pages.components.constants import MSG_UPLOAD_FILE_REQ
from pages.components.custom_sidebar import custom_sidebar
from pages.components.ids_check_res_df import create_specifications_dataframe
from tools import ifchelper

session = st.session_state


def draw_chart():
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)


def plot_map():
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [59.93, 30.31],
        columns=['lat', 'lon'])

    st.map(map_data)


def write_widget():
    x = st.slider('x')  # 👈 this is a widget
    return x


def input_name():
    st.text_input("Your name", key='name')
    st.write(st.session_state.name)


def checkbox():
    if st.checkbox('Show dataframe', True):
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        st.write(chart_data)


def selectbox():
    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })

    option = st.selectbox(
        'Which number do you like best?',
        df['first column'])

    st.write('You selected: ', option)


def show_progress():
    st.write('Starting...')

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i + 1}')
        bar.progress(i + 1)
        sleep(0.01)

    st.write('...and now we\'re done!')


def initialize_session_state():
    # session["isHealthDataLoaded"] = False
    # session["HealthData"] = {}
    # session["Graphs"] = {}
    # session["SequenceData"] = {}
    # session["CostScheduleData"] = {}
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


def load_data():
    if "ifc_file" in session:
        # st.write(dir(session.ifc_file))

        session["DataFrame"] = get_ifc_pandas()
        session.Classes = session.DataFrame["Class"].value_counts().keys().tolist()
        session["IsDataFrameLoaded"] = True


def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        "IfcBuildingElement"
    )
    frame = ifchelper.create_pandas_dataframe(data, pset_attributes)
    return frame


def run_tests():
    show_progress()
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
    allowed_types = ['Базовая стена:Внешняя несущая', 'Прямоугольный импост:50 x 150мм', 'Перекрытие:Типовой 200мм',
                     'Базовая стена:Перегородка из кирпича, 120']

    assert element in allowed_types


def run_ids_test():
    ids_file = st.file_uploader("Выберите файл IDS", type=['ids'], key="uploaded_file")
    if ids_file:
        my_ids = ids.open(ids_file)

        for spec in my_ids.specifications:
            st.write(spec.asdict())

        st.write(my_ids.info)
        st.write(dir(my_ids))

        show_progress()

        my_ids.validate(session["ifc_file"])
        st.write(session["ifc_file"])

        report = reporter.Json(my_ids).report()
        st.write(report)

        res_df = create_specifications_dataframe(report)
        st.write(res_df)

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
        tab1, tab2 = st.tabs(["Test", " Some second stuff"])
        with tab1:
            ## DATAFRAME REVIEW
            st.header("Test")
            # st.write(draw_chart())
            # st.write(plot_map())
            # st.write(x := write_widget(), 'squad is', x * x)
            # input_name()
            # checkbox()
            # selectbox()
            # show_progress()
            st.write(session.DataFrame)
            # from st_aggrid import AgGrid
            # AgGrid(session.DataFrame)
            run_ids_test()

            if st.button('Run tests', key="run_tests", help='Провести тест'):
                run_tests()

            # st.button('Run tests', key="run_tests", help='Провести тест', on_click=run_tests)

            st.download_button('Download CSV', file_name=session.file_name.replace('ifc', '.csv'),
                               data=session.DataFrame.to_csv())
            st.download_button('Download JSON', file_name=session.file_name.replace('ifc', '.json'),
                               data=session.DataFrame.to_json())
            # st.button("Download CSV", key="download_csv", on_click=download_csv)
            # st.button("Download Excel", key="download_excel", on_click=download_excel)

            # st.write(len(session.ifc_file.by_type('IfcWall')))
    else:
        st.header(MSG_UPLOAD_FILE_REQ)

    custom_sidebar()


execute()
