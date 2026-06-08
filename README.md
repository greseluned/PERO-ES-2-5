# PERO-ES-2-5: Transcripción con PERO-OCR sobre prensa histórica en español de dos a cinco columnas

## Descripción

Este repositorio recoge las pruebas realizadas para evaluar la eficacia de PERO-OCR en tareas de transcripción automática de prensa histórica en español. El objetivo principal es comprobar su rendimiento en documentos con layouts variables y de complejidad moderada: páginas con más de una columna, pero sin llegar a la complejidad compositiva de los grandes formatos tipo broadsheet.

PERO-OCR es un sistema de reconocimiento óptico de caracteres desarrollado por el grupo DCGM de la Faculty of Information Technology de la Brno University of Technology. Está orientado al procesamiento de documentos históricos impresos y manuscritos, e integra tareas de análisis de layout, detección de líneas de texto y transcripción OCR. Aunque sus modelos publicados fueron concebidos inicialmente para documentos europeos y, de forma específica, para prensa checa de baja calidad digitalizada a partir de microfilmes, sus desarrolladores indican que puede ofrecer buenos resultados en documentos impresos europeos en distintas lenguas. Por este motivo, este repositorio explora su aplicabilidad a prensa histórica en español.

En una primera fase (v.1.0.0), las pruebas se realizan sin fine tuning sobre un corpus de prensa escrita en lengua española procedente de Filipinas, República Dominicana y Puerto Rico. Este corpus, denominado corpus-pruebas, contiene documentos con entre 2 y 5 columnas y tiene como propósito servir como conjunto de evaluación para sistemas de reconocimiento óptico de caracteres.

En una segunda fase (v.2.0.0), se realizan pruebas con fine tuning a partir de un segundo corpus, denominado corpus-entrenamiento, con el fin de valorar si la adaptación del modelo a las características específicas de la prensa histórica en español mejora la calidad de la transcripción.

Los corpus y las pruebas han sido desarrollados en el marco del proyecto GRESEL-UNED: “Narrativas poscoloniales en periódicos en español de Asia, España y el Caribe hispánico” (PID2023-151280OB-C22), financiado por el Ministerio de Ciencia e Innovación / AEI.

---

## Estructura del repositorio

```
PERO-ES-2-5/
├── corpus-pruebas/              
	├──pruebas-jpg/ 			 # Imágenes digitalizadas (92 páginas en formato JPG)
	├──pruebas-page_xml/           # Transcripciones manuales en formato PAGE-XML (Transkribus)
	├──pruebas-transcripciones/       # Transcripciones automáticas generadas por PERO-OCR
├── corpus-entrenamiento/              
	├──entrenamiento-jpg/ 			 # Imágenes digitalizadas (92 páginas en formato JPG)
	├──entrenamiento_xml/           # Transcripciones en formato PAGE-XML (Transkribus)
	├──entrenamiento_txt/       # Transcripciones generadas con Transkribus y revisadas
└── evaluacion_sin_entrenamiento/
    ├── metricas_globales.json  # Métricas de evaluación globales (CER, WER, BLEU, ROUGE)
    ├── resultados_por_documento.json  # Métricas individuales por documento
    └── ground_truth/           # Textos de referencia extraídos de los PAGE-XML
└── evaluacion_con_entrenamiento/
    ├── metricas_globales.json  # Métricas de evaluación globales (CER, WER, BLEU, ROUGE)
    ├── resultados_por_documento.json  # Métricas individuales por documento
    └── ground_truth/           # Textos de referencia extraídos de los PAGE-XML
```

### Descripción de las carpetas

**`corpus-pruebas/`**
Contiene 92 páginas completas  procedentes de las siguientes publicaciones:

- *Filipinas* (1909–1910) — Revista femenina editada en Manila (NÚMERO DE PÁGINAS)
- *Fémina* (1922–1923) — Revista femenina dominicana, editada en San Pedro de Macorís (NÚMERO DE PÁGINAS)
- *Heraldo de la Mujer* (1919) — Publicación periódica de Puerto Rico (NÚMERO DE PÁGINAS)
- *La Vanguardia* (1944) — Diario filipino de noticias e intereses generales. (NÚMERO DE PÁGINAS)

**`evaluacion_sin_entrenamiento/`**
Contiene los resultados de la evaluación automática de las transcripciones de PERO-OCR frente al ground truth manual, calculados con las métricas estándar del framework From Paper to Pixel (Macicior-Mitxelena y García-Serrano, 2026).

**`corpus-entrenamiento/`**
Contiene  páginas completas  procedentes de las siguientes publicaciones:

- *Excelsior* (1929–1932) — Revista decenal ilustrada editada en Manila (NÚMERO DE PÁGINAS)
- *Sorpresas Chicago*

**`evaluacion_con_entrenamiento/`**
Se completará en la versión v.2.0.0 del repositorio

---

## Métricas de evaluación

La evaluación se realizó utilizando las siguientes métricas:

| Métrica | Valor | Descripción |
|---|---|---|
| CER | 0.8674 | Character Error Rate (tasa de error por carácter) |
| WER | 1.0570 | Word Error Rate (tasa de error por palabra) |
| BLEU | 0.5448 | Similitud de secuencias de palabras |
| ROUGE-1 | 0.7927 | Coincidencia de vocabulario |
| ROUGE-L | 0.6789 | Coincidencia de secuencias largas |
| NED | 0.3437 | Normalized Edit Distance |

En las pruebas realizdas con PERO-OCR sin fine-tuning, los mejores resultados se obtuvieron en páginas de *Filipinas* (1909), con CER entre 0.02 y 0.06, mientras que los peores corresponden a páginas con anotaciones parciales en Transkribus.

---

## Metodología de transcripción

Las transcripciones manuales se realizaron en la plataforma Transkribus con los modelos... Se incluye la segmentación estructural en regiones, párrafos y líneas mediante el estándar PAGE-XML.

---

## Autoras

- **Rocío Ortuño Casanova** — Departamento de Literatura Española y Teoría de la Literatura, UNED
- **María Teresa Vera Rojas** — Departamento de Literatura Española, Universitat de les Illes Balears

## Colaborador técnico

- **Fernando Obispo Permuy** — Implementación del pipeline OCR y evaluación, UNED

---

## Cita

Si utiliza este corpus en su investigación, por favor cítelo de la siguiente manera:

> Ortuño Casanova, R., Vera Rojas, M. T., y Obispo Permuy, F. (2026). *PERO-ES-2-5: Transcripción con PERO-OCR sobre prensa histórica en español de dos a cinco columnas* [repositorio]. 

---

## Licencia

Este corpus se distribuye bajo la licencia **Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0)**.

Puede compartir y adaptar el material para fines no comerciales siempre que se proporcione atribución adecuada.

Más información: https://creativecommons.org/licenses/by-nc/4.0/deed.es

---

## Financiación

Este trabajo ha sido financiado por el Ministerio de Ciencia e Innovación / AEI en el marco del proyecto coordinado GRESEL UNED (PID2023-151280OB-C22).

---

## Referencias

Hradiš, M., Kodym, O., & Kohút, J. (2026). PERO OCR: Automatic document processing (Versión actual del software). Facultad de Tecnología de la Información, Universidad Tecnológica de Brno. https://github.com/DCGM/pero-ocr
Kišš, M., Beneš, K., & Hradiš, M. (2021). AT-ST: Self-training adaptation strategy for OCR in domains with limited transcriptions. En Proceedings of the International Conference on Document Analysis and Recognition (ICDAR 2021).
Kodym, O., & Hradiš, M. (2021). Page layout analysis system for unconstrained historic documents. En Proceedings of the International Conference on Document Analysis and Recognition (ICDAR 2021).
Kohút, J., & Hradiš, M. (2021). TS-Net: OCR trained to switch between text transcription styles. En Proceedings of the International Conference on Document Analysis and Recognition (ICDAR 2021).
Macicior-Mitxelena, J. y García-Serrano, A. (2026). 'From Paper to Pixel: Experimental Framework for Access to Historical Spanish Documents'. Software/Código. https://github.com/jaionemacicior/from-paper-to-pixel
READ-COOP SCE. (2026). Transkribus [Software]. https://transkribus.eu/
