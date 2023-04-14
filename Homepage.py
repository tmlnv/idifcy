import ifcopenshell
import streamlit as st


def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True

    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name


def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input


def main():
    st.set_page_config(
        layout="wide",
        page_title="IFC BIM Model AQA",
        page_icon="🏗️",
    )
    st.title("IFC BIM Model AQA")
    st.markdown(
        """ 
    ###  📁 Загрузите файл в формате ifc
    """
    )

    ## Add File uploader to Side Bar Navigation
    # st.header('Model Loader')
    st.file_uploader("Выберите файл", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.success(f'Файл успешно загружен')

        col1, col2 = st.columns([2, 1])
        col1.subheader(f'Файл проекта успешно загружен "{get_project_name()}"')
        col2.text_input("✏️ Изменить название проекта", key="project_name_input")
        col2.button("✔️ Применить", key="change_project_name", on_click=change_project_name())

        st.write("🔃 Вы так же можете загрузить новый файл")

    st.sidebar.write("""
    ### Credits:
    #### Artem Leonov
    
    Follow me on [GitHub](https://github.com/tmlnv)
    
    --------------
    License: MIT
    
    """)
    st.write("")
    st.sidebar.write("")


if __name__ == "__main__":
    session = st.session_state
    main()
