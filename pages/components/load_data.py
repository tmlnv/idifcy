"""Лоадер для данных, если они не загрузились в сессии"""
import streamlit as st

from tools import ifchelper

session = st.session_state


def load_data():
    if "ifc_file" in session:

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
