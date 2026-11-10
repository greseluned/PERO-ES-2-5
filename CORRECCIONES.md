# Correcciones del corpus (noviembre de 2026)

Durante la preparación del corpus de etiquetado de regiones se comprobó, página por página, que cada PAGE-XML corresponde a la imagen con la que está emparejado. La comprobación combinó tres fuentes: el nombre de imagen y las dimensiones que Transkribus guarda en cada XML (`imageFilename`, `imageWidth`, `imageHeight`), una medida automática de alineación (densidad de tinta dentro de las líneas transcritas frente a la de las mismas líneas desplazadas) y la revisión visual de todas las páginas con puntuación baja, superponiendo las líneas del XML a la imagen y comparando el texto transcrito con el impreso. Se buscaron además duplicados por suma de comprobación de las imágenes, por identificador de página de Transkribus y por texto transcrito.

Se encontraron los problemas siguientes, que esta versión corrige. Cada corrección se aplica a la vez al PAGE-XML, a la transcripción de página (`entrenamiento_txt_paginas`) y a las transcripciones de línea (`entrenamiento_txt_lineas`) de la página, que se derivan del XML; en el corpus de pruebas, también a la transcripción de PERO-OCR (`pruebas-transcripciones`).

## Corpus de entrenamiento

| Archivo(s) | Problema | Corrección |
|---|---|---|
| `Sorpresas-Chicago_Pag28.xml` y `Sorpresas-Chicago_Pag31.xml` | Los dos XML estaban intercambiados (Pag28.xml transcribía la imagen 31 y viceversa). | Se intercambian los nombres. |
| `Heraldo-de-la-mujer-Aug-1919_p003`, `p008`, `p009`, `p010`, `p011`, `p014`, `p015`, `p016` y `p020` (.xml) | Cada XML tenía el número de otra página; el número correcto es el de su `imageFilename` en Transkribus (p003 → p008, p008 → p009, p009 → p010, p010 → p011, p011 → p014, p014 → p015, p015 → p016, p016 → p020, p020 → p022). | Se renombran al número de la página que transcriben. |
| `Heraldo-de-la-mujer-Aug-1919_p001.xml`, `p002.xml` y `p022.xml` (originales) | Son copias de las transcripciones de `Semana-1949-02-10_p005`, `p006` y `p033`, que ya están en el corpus. | Se eliminan. |
| `Heraldo-de-la-mujer-Aug-1919_p001.jpg`, `p002.jpg` y `p003.jpg` | Tras la corrección se quedan sin transcripción. | Se retiran. |
| `Hispanidad-4-Abril-1940-P12` (.xml y .jpg) | La imagen es una copia exacta de `Hispanidad-5-Mayo-1940-P12.jpg` (sumario del número de mayo); la imagen de la página transcrita no está en el repositorio. | Se retira la pareja. Puede volver a incluirse exportando de Transkribus la imagen correcta. |

Resultado: 619 páginas (antes 623).

## Corpus de pruebas

| Archivo(s) | Problema | Corrección |
|---|---|---|
| `LA-VANGUARDIA-XXV-Num-77-29-04-1944` (.xml y .jpg) | El XML es la transcripción de la página 1 (ya incluida como `LA-VANGUARDIA-XXV-Num-77-P01`) y la imagen es una copia exacta de la página 4 (ya incluida como `LA-VANGUARDIA-XXV-Num-77-29-04-1944-P04`). | Se retira la pareja. |
| `Fémina-15-10-1922_p004` (.xml y .jpg) | Es la misma página de Transkribus (pageId 104387259) que `Fémina-15-12-1922_p004` del corpus de entrenamiento; la fecha impresa del número es 15 de diciembre de 1922. Al estar en los dos corpus, la evaluación no era independiente. | Se retira del corpus de pruebas. |

Resultado: 90 páginas (antes 92).

## Consecuencias para los resultados publicados

Los resultados de `metodologia.md`, `corpus-pruebas/informe_evaluacion.txt` y los archivos de métricas se obtuvieron con la versión anterior de los dos corpus. El fine-tuning se entrenó con 15 páginas cuyas líneas no correspondían a la imagen (12 del Heraldo de la Mujer, 2 de Sorpresas Chicago y 1 de Hispanidad) y la evaluación incluyó una página mal emparejada y otra presente también en el entrenamiento. Esos resultados deben repetirse con esta versión; hasta entonces han de leerse como provisionales.

Todas las páginas corregidas se han vuelto a comprobar con la medida de alineación después del cambio.
