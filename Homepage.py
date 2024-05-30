import ifcopenshell
import streamlit as st

from pages.components.custom_sidebar import custom_sidebar


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

    ### Empty IDS
    session["IdsFile"] = None
    session["IdsReport"] = None
    session["IdsReportDF"] = None


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
        ###  📁 Upload file in ifc format
        """
    )

    ## Add File uploader to Side Bar Navigation
    # st.header('Model Loader')
    st.file_uploader("Upload file", type=["ifc"], key="uploaded_file", on_change=callback_upload)

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.success("File successfully uploaded")

        col1, col2 = st.columns([2, 1])
        col1.subheader(f'Project "{get_project_name()}" successfully uploaded')
        col2.text_input("Change project name", key="project_name_input")
        col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())

        st.write("🔃 You can also upload another file")

    custom_sidebar()


if __name__ == "__main__":
    session = st.session_state
    main()
