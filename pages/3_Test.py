import json
from time import sleep

import streamlit as st
import numpy as np
import pandas as pd
from ifctester import ids, reporter

from pages.components.constants import MSG_UPLOAD_FILE_REQ
from pages.components.custom_sidebar import custom_sidebar
from pages.components.ids_check_res_df import create_specifications_dataframe
from pages.components.load_data import load_data

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
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False
    session["IdsFile"] = None
    session["IdsReport"] = None
    session["IdsReportDF"] = None


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
    st.write(f'Total elements failed checking {counter}')


def test_type_of_element(element):
    allowed_types = ['Базовая стена:Внешняя несущая', 'Прямоугольный импост:50 x 150мм', 'Перекрытие:Типовой 200мм',
                     'Базовая стена:Перегородка из кирпича, 120']

    assert element in allowed_types


def upload_ids_file():
    ids_file = st.file_uploader("Выберите файл IDS", type=['ids'], key="uploaded_file")
    if ids_file:
        my_ids = ids.open(ids_file)
        session["IdsFile"] = my_ids


def print_ids_as_dict():
    for spec in session["IdsFile"].specifications:
        st.write(spec.asdict())


def run_ids_test():
    ids_info = session["IdsFile"].info
    st.write(f'Название ids спецификации: **{(ids_info)["title"]}**, автор: {ids_info["author"]}')

    show_progress()

    session["IdsFile"].validate(session["ifc_file"])

    report = reporter.Json(session["IdsFile"]).report()
    session["IdsReport"] = report

    session["IdsReportDF"] = create_specifications_dataframe(report)


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
                        'Run IDS tests',
                        key="run_ids_test",
                        help='Провести тест в соответствии с IDS спецификацией'
                ):
                    run_ids_test()
                if session.get("IdsReportDF"):
                    st.header("Результаты проверки")
                    st.write(session["IdsReportDF"])


            if st.button('Run tests', key="run_tests", help='Провести тест'):
                run_tests()

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
                    'Download JSON',
                    file_name='IDS_RES_' + session.file_name.replace('ifc', '.json'),
                    data=json.dumps(ids_report)
                )
                st.write(ids_report)
            else:
                st.write("Загрузите IDS файл на вкладке 'Test' и произведите проверку, нажав на кнопку 'Run IDS tests'")

    else:
        st.header(MSG_UPLOAD_FILE_REQ)

    custom_sidebar()


execute()
