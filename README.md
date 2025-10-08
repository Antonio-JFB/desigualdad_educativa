# Desigualdad Educativa en Sonora

## 📌 Descripción del Proyecto
Este proyecto busca analizar **la evolución de la matrícula escolar en Sonora** en los últimos años para responder la pregunta:

> **¿Ha aumentado la desigualdad educativa entre las escuelas públicas y privadas en Sonora de 2022 a 2025?**

Para responder esta pregunta, cruzaremos datos de **alumnos inscritos** con datos de **escuelas registradas**, identificando tendencias de crecimiento o disminución de matrícula por tipo de sostenimiento (público / privado) y su distribución geográfica.

---

## 🎯 Pregunta de Investigación
**Pregunta:**  
¿Está aumentando la desigualdad educativa entre el sistema público y privado en Sonora en los últimos ciclos escolares (2022–2025)?

**Hipótesis inicial:**  
Se espera que la matrícula de escuelas privadas crezca proporcionalmente más que la matrícula en escuelas públicas, lo que podría reflejar un aumento de la brecha educativa.

---

## 🧑‍🤝‍🧑 Público Objetivo
El producto final de este análisis (dashboard interactivo) está destinado a:
- Investigadores y tomadores de decisiones en el área de **educación pública**.
- Organizaciones de la sociedad civil interesadas en **equidad educativa**.
- Periodistas y académicos que estudien la evolución del sistema educativo.

---

## 📂 Fuentes de Datos

1. **Matrículas de Educación Básica en Sonora**  
   Fuente: [SIGED – SEP](https://www.siged.sep.gob.mx/SIGED/escuelas.html) 
	   [Plataforma Nacional de Datos abiertos](https://datos.gob.mx/dataset/registro_alumnado_personal_docente_educacion_basica_media_superior_formato_911) 
   Descripción: Catálogo actualizado de escuelas en México, con ubicación georreferenciada, nivel educativo y tipo de sostenimiento (público o privado).
   Frecuencia: Ciclo escolar.

2. **Directorio de Escuelas**  
   Fuente: [Plataforma Nacional de Datos abiertos](https://datos.gob.mx/dataset/catalogo_centros_trabajo_sep)  
   Descripción: Listado de centros educativos de la Secretaría de Educación Pública del estado de Sonora.

3. **Datos Económicos de Sonora**  
   Fuente: INEGI (PIB estatal, indicadores socioeconómicos, información sobre educación).  
   Uso: Para correlacionar matrícula con desarrollo económico de la región.

---

## 🏗️ Estructura del Proyecto (Cookiecutter Data Science)


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
