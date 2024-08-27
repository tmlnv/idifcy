# idifcy

Intelligent Design Implementation for Facilitating Construction Yields (idifcy)
is a tool designed to help Civil Engineers manage IFC files.
It enhances the quality assurance processes in construction projects
through IDS validation and verification and IFC model visualization.

![demo screenshot](https://drive.google.com/uc?export=view&id=125ZCo3L1ZGZMRo7HebLNp7jCCrz6sosb)

## Setup

### Python part

To install the necessary Python dependencies:

```bash
poetry install
```

### JS part

For setting up the JavaScript environment, particularly for the frontend viewer:

```bash
cd pages/frontend-viewer/
npm install
```

## Run

To start the application with Streamlit:

```bash
streamlit run Homepage.py
```

## Docker

You can use Docker to build and run idifcy as follows:

```commandline
# Build Docker image
docker build -t idifcy .

# Run Docker container
docker run -p 8501:8501 idifcy
```

### DockerHub

Note: The current version of idifcy relies on a specific version of ifcopenshellthat
that is not available on PyPI. Therefore, to use idifcy,
you must pull the working build from DockerHub.

```commandline
docker pull tmlnv/idifcy:latest
```

## References

1. [_Ifc 101 course_](https://github.com/myoualid/ifc-101-course)
2. [_ifcopenshell_](https://github.com/IfcOpenShell/IfcOpenShell)
3. [_IDS_](https://github.com/buildingSMART/IDS)
4. [_ids converter_](https://github.com/c4rlosdias/ids_converter)
