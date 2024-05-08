# Aplicación de ML a Odoo
Hay muchísimas formas en las que se pueden aplicar técnicas de aprendizaje automático (ML por sus siglas en inglés: Machine Learning) en Sistemas de Información Empresariales. En esta carpeta hay un módulo para Odoo que demuestra la aplicación de técnicas de clustering y clasificación a Odoo. Para poder ejecutar estos ejemplos, es necesario instalar los siguientes paquetes:
* numpy
* scikit-learn
* pandas
* joblib

## Preparación de los datos
Será necesario descargar [este dataset](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling/data) sobre clientes de un banco pensado para intentar predecir si un cliente dejará o no el banco. Para poder cargar los datos correctamente en Odoo, independientemente del idioma en el que esté, es necesario cambiar el nombre de los paises campo geography por el código del pais de la siguiente manera:
* Spain -> ES
* Germany -> DE
* France -> FR

Una vez hecha esta corrección, los datos pueden cargarse directamente mediante la opción de cargar CSV que incorpora Odoo desde la vista del Cliente del banco.

## Clustering
Para incorporar el clustering, se añaden 2 modelos a la base de datos:
* **clustering**: representa los parámetros y el tipo de algoritmo a utilizar, así como el resultado de un proceso de clustering que contiene las agrupaciones de los clientes.
* **group**: representa 1 grupo dentro un proceso de clustering que contiene varios clientes.

## Clasificación
La carpeta [dt_training](dt_training) contiene un cuaderno de Jupyter en el que se puede ver el proceso de entrenamiento de un árbol de decisión. En última estancia, el cuaderno genera un fichero que contiene el modelo entrenado con sus parámetros y el preprocesamiento necesario que luego será cargado por el módulo de Odoo y utilizado para predecir si un cliente dejaría o no el banco.