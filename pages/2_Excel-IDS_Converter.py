import pandas as pd
import streamlit as st
import datetime
from ifctester import ids
from PIL import Image


# =========================================================================================================================
# pattern
# =========================================================================================================================
def pattern(value):
    result = None if value == '' else value
    try:
        if ',' in value:
            enums = [j.strip() for j in value.split(',')]
            if isinstance(enums[0], str):
                base = "string"
            elif isinstance(enums[0], int):
                base = "integer"
            elif isinstance(enums[0], bool):
                base = "boolean"
            else:
                base = "decimal"

            result = ids.Restriction(base=base, options={'enumeration': enums})
        if value[:1] == '/' and value[-1:] == '/':
            value = value[1:-1]
            if 'clusive=' in value:
                l = value.split(',')
                options = {}
                for it in l:
                    key = it.split('=')[0].strip()
                    val = int(it.split('=')[1].strip())
                    options[key] = val
                result = ids.Restriction(base="integer", options=options)
            elif 'ength=' in value:
                l = value.split(',')
                options = {}
                for it in l:
                    key = it.split('=')[0].strip().strip()
                    val = int(it.split('=')[1].strip())
                    options[key] = val
                result = ids.Restriction(base="string", options=options)
            else:
                result = ids.Restriction(base="string", options={'pattern': value})
        print(result)
        return result

    except:
        return None


# =========================================================================================================================
# page config
# =========================================================================================================================

im = Image.open('./resources/img/IDS_logo.ico')
st.set_page_config(
    page_title="IDS Converter",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================================================================
# System vars
# =========================================================================================================================


if 'ids' not in st.session_state:
    st.session_state.ids = None

if 'IdsFile' not in st.session_state:
    st.session_state["IdsFile"] = None

if 'df_specifications' not in st.session_state:
    st.session_state.df = None
if 'df_applicability' not in st.session_state:
    st.session_state.df = None
if 'df_requirement' not in st.session_state:
    st.session_state.df = None

if 'file_name' not in st.session_state:
    st.session_state.file_name = None

if 'convert' not in st.session_state:
    st.session_state.convert = False

# =========================================================================================================================
# Sidebar
# =========================================================================================================================

with st.sidebar:
    uploaded_file = st.file_uploader("📥 Choose a XLSX file", type=['xlsx'])

# =========================================================================================================================
# If file loaded or bSDD connection
# =========================================================================================================================

with st.container():
    # Create Dataframe

    if uploaded_file:

        st.session_state.convert = False

        st.session_state.df_specifications = pd.read_excel(uploaded_file, dtype=str, skiprows=2,
                                                           sheet_name="SPECIFICATIONS")
        st.session_state.df_applicability = pd.read_excel(uploaded_file, dtype=str, skiprows=2,
                                                          sheet_name="APPLICABILITY")
        st.session_state.df_requirements = pd.read_excel(uploaded_file, dtype=str, skiprows=2,
                                                         sheet_name="REQUIREMENTS")

        st.session_state.file_name = uploaded_file.name.split('.')[0] + '.ids'

        if st.session_state.df_specifications is not None:

            st.header('IDS Information')
            col1, col2 = st.columns(2, gap="large")
            with col1:
                title = st.text_input('_Title:_')
                copyright = st.text_input('_Copyright:_')
                version = st.text_input('_Version:_')
                author = st.text_input('_Author:_', 'xxxxx@xxxxx.xxx')
                ifc_version = st.selectbox('_IFC Version:_', ('IFC2X3', 'IFC4', 'IFC4X3'))

            with col2:
                date = st.text_input('_Date:_', datetime.date.today())
                description = st.text_input('_Description:_')
                purpose = st.text_input('_Purpose:_')
                milestone = st.text_input('_Milestone:_')

            st.divider()
            st.markdown(':white_check_mark: :green[check your specifications:]')

            for index, spec in st.session_state.df_specifications.iterrows():
                with st.expander(':green[Specification Name : ]' + spec.iloc[0]):
                    st.markdown(f':green[Description : ]{spec.iloc[1]}')
                    st.markdown(f':green[Optionality : ]{spec.iloc[2]}')

                    st.markdown(f':green[Applied to : ]')
                    df_app = st.session_state.df_applicability.query(f"specification == '{spec.iloc[0]}'").fillna('')
                    for index, app in df_app.iterrows():
                        for i in range(df_app.shape[1] - 1):
                            if app.iloc[i] != '' and df_app.columns.to_list()[i] != 'specification':
                                st.write(df_app.columns.to_list()[i] + ' : ' + app.iloc[i])

                    if spec.iloc[2] == 'REQUIRED':
                        st.markdown(f':green[MUST HAVE: ]')
                    elif spec.iloc[2] == 'PROHIBITED':
                        st.markdown(f':green[MUST NOT HAVE: ]')
                    elif spec.iloc[2] == 'OPTIONAL':
                        st.markdown(f':green[MAY HAVE: ]')
                    else:
                        st.markdown(f':green[requirements: ]')

                    df_req = st.session_state.df_requirements.query(f"specification == '{spec.iloc[0]}'").fillna('')
                    for index, req in df_req.iterrows():
                        for i in range(df_req.shape[1] - 1):
                            if req.iloc[i] != '' and df_app.columns.to_list()[i] != 'specification':
                                st.write(df_req.columns.to_list()[i] + ' : ' + req.iloc[i])

            st.divider()

            #
            # Convert dataframe to ids
            #
            submitted = st.button("Convert to IDS ▶️")
            if submitted:
                my_ids = ids.Ids(title=title,
                                 copyright=copyright,
                                 version=version,
                                 author=author,
                                 description=description,
                                 date=date,
                                 purpose=purpose,
                                 milestone=milestone
                                 )
                for index, spec in st.session_state.df_specifications.iterrows():
                    my_spec = ids.Specification(
                        name=spec.iloc[0],
                        description=spec.iloc[1],
                        minOccurs=0 if spec.iloc[2].upper() in ['OPTIONAL', 'PROHIBITED'] else 1,
                        maxOccurs='unbounded' if spec.iloc[2].upper() in ['REQUIRED', 'OPTIONAL'] else 0,
                        ifcVersion=ifc_version
                    )

                    df_app_spec = st.session_state.df_applicability.query(f"specification == '{spec.iloc[0]}'").fillna(
                        '')
                    df_req_spec = st.session_state.df_requirements.query(f"specification == '{spec.iloc[0]}'").fillna(
                        '')

                    # create applicability
                    for index, row in df_app_spec.iterrows():
                        # add entity

                        entity = ids.Entity(
                            name=pattern(row['entity name']),
                            predefinedType=pattern(row['predefined type'])
                        ) if row['entity name'] != '' else None

                        # add attribute

                        attribute = ids.Attribute(
                            name=pattern(row['attribute name']),
                            value=pattern(row['attribute value'])
                        ) if row['attribute name'] != '' else None

                        # add property

                        property = ids.Property(
                            uri=row['URI'] if row['URI'] != '' else None,
                            name=pattern(row['property name']),
                            value=pattern(row['property value']),
                            propertySet=pattern(row['property set']),
                            datatype=row['data type'] if row['data type'] != '' else None
                        ) if row['property name'] != '' else None

                        # add classification

                        classification = ids.Classification(
                            uri=row['URI'] if row['URI'] != '' else None,
                            value=pattern(row['classification reference']),
                            system=pattern(row['classification system'])
                        ) if row['classification reference'] != '' and row['classification system'] != '' else None

                        # add material

                        material = ids.Material(
                            uri=row['URI'] if row['URI'] != '' else None,
                            value=pattern(row['material name'])
                        ) if row['material name'] != '' else None

                        # add parts

                        parts = ids.PartOf(
                            entity=row['part of entity'].upper(),
                            relation=None if row['relation'] == '' else row['relation']
                        ) if row['part of entity'] != '' else None

                        if entity:
                            my_spec.applicability.append(entity)
                        if attribute:
                            my_spec.applicability.append(attribute)
                        if property:
                            my_spec.applicability.append(property)
                        if classification:
                            my_spec.applicability.append(classification)
                        if material:
                            my_spec.applicability.append(material)
                        if parts:
                            my_spec.applicability.append(parts)

                    # create requirements
                    for index, row in df_req_spec.iterrows():
                        row['optionality'] = 'REQUIRED' if row['optionality'] == '' else row['optionality']
                        # add entity

                        entity = ids.Entity(
                            name=pattern(row['entity name']),
                            predefinedType=pattern(row['predefined type']),
                        ) if row['entity name'] != '' else None

                        # add attribute

                        attribute = ids.Attribute(
                            name=pattern(row['attribute name']),
                            value=pattern(row['attribute value'])
                        ) if row['attribute name'] != '' else None

                        # add property

                        property = ids.Property(
                            uri=row['URI'] if row['URI'] != '' else None,
                            name=pattern(row['property name']),
                            value=pattern(row['property value']),
                            propertySet=pattern(row['property set']),
                            datatype=row['data type'] if row['data type'] != '' else None,
                            minOccurs=0 if row['optionality'].upper() in ['OPTIONAL', 'PROHIBITED'] else 1,
                            maxOccurs='unbounded' if row['optionality'].upper() in ['REQUIRED', 'OPTIONAL'] else 0
                        ) if row['property name'] != '' else None

                        # add classification

                        classification = ids.Classification(
                            uri=row['URI'] if row['URI'] != '' else None,
                            value=pattern(row['classification reference']),
                            system=pattern(row['classification system']),
                            minOccurs=0 if row['optionality'].upper() in ['OPTIONAL', 'PROHIBITED'] else 1,
                            maxOccurs='unbounded' if row['optionality'].upper() in ['REQUIRED', 'OPTIONAL'] else 0
                        ) if row['classification reference'] != '' and row['classification system'] != '' else None

                        # add material

                        material = ids.Material(
                            uri=row['URI'] if row['URI'] != '' else None,
                            value=pattern(row['material name']),
                            minOccurs=0 if row['optionality'].upper() in ['OPTIONAL', 'PROHIBITED'] else 1,
                            maxOccurs='unbounded' if row['optionality'].upper() in ['REQUIRED', 'OPTIONAL'] else 0
                        ) if row['material name'] != '' else None

                        # add parts

                        parts = ids.PartOf(
                            entity=row['part of entity'].upper(),
                            relation=None if row['relation'] == '' else row['relation'],
                            minOccurs=0 if row['optionality'].upper() in ['OPTIONAL', 'PROHIBITED'] else 1,
                            maxOccurs='unbounded' if row['optionality'].upper() in ['REQUIRED', 'OPTIONAL'] else 0
                        ) if row['part of entity'] != '' else None

                        if entity:
                            my_spec.requirements.append(entity)
                        if attribute:
                            my_spec.requirements.append(attribute)
                        if property:
                            my_spec.requirements.append(property)
                        if classification:
                            my_spec.requirements.append(classification)
                        if material:
                            my_spec.requirements.append(material)
                        if parts:
                            my_spec.requirements.append(parts)

                    # Add specification in specifications
                    my_ids.specifications.append(my_spec)

                st.session_state.ids = my_ids.to_string()
                st.session_state["IdsFile"] = my_ids

                if st.session_state.ids is not None:
                    st.session_state.convert = True
                    st.balloons()
                else:
                    st.error('ERRO : File not created!')

            if st.session_state.convert and st.session_state.ids:
                st.download_button('📥 Download IDS file', st.session_state.ids, file_name=st.session_state.file_name,
                                   mime='xml')
