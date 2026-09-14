# Metodología y resultados — Fine-tuning PERO-OCR para prensa histórica hispana

**Proyecto:** GRESEL-UNED (PID2023-151280OB-C22)  
**Técnico:** Fernando Obispo Permuy  
**Supervisora:** Rocío Ortuño Casanova  
**Fecha:** Septiembre de 2026  

---

## 1. Objetivo

El objetivo de este trabajo es adaptar el motor de OCR PERO-OCR a las características específicas de la prensa histórica en español de Filipinas, España y el Caribe hispánico (siglos XIX-XX), mediante un proceso de fine-tuning sobre un corpus de entrenamiento anotado manualmente en Transkribus, y evaluar la mejora obtenida respecto al modelo base mediante métricas estándar de calidad de OCR (CER y WER).

---

## 2. Corpus de entrenamiento

El corpus de entrenamiento se compone de páginas digitalizadas y transcritas manualmente en Transkribus, exportadas en formato PAGE-XML. Cada página se acompaña de su imagen JPG y sus transcripciones a nivel de línea y de página en formato TXT.

### 2.1. Publicaciones incluidas

| Publicación | Fechas | Páginas | Fuente |
|---|---|---|---|
| Excelsior (Filipinas) | 1929-1932 | — | Corpus original |
| Filipinas Ante Europa | 1899-1910 | — | Corpus original |
| Heraldo de la Mujer | 1919 | — | Corpus original |
| Sorpresas Chicago | — | — | Corpus original |
| La Malasia | — | — | Corpus original |
| Fémina | 1922-1923 | — | Corpus original |
| Boletín Oficial de la Cámara de Comercio Española de Filipinas | — | — | Corpus original |
| El Oriente | — | — | Corpus original |
| Hispanidad (Filipinas) | Abril-Agosto 1940 (nº 4-8) | 153 | Transkribus |
| Semana (España) | Enero-Junio 1949 (nº 3, 7, 8, 12, 16, 20, 21, 24) | 334 | Zenodo |

### 2.2. Estadísticas del corpus

| Conjunto | Páginas | Pares imagen-línea |
|---|---|---|
| Entrenamiento (train) | — | 14.696 |
| Validación (val) | — | 1.837 |
| Test | — | 1.838 |
| **Total** | **623** | **18.371** |

La división en train/val/test se realizó por número completo de periódico (issue_id), no por página aleatoria, para evitar que el modelo memorizara la maqueta de una publicación concreta y garantizar una evaluación realista de la generalización.

---

## 3. Proceso de fine-tuning

### 3.1. Configuración técnica

| Parámetro | Valor |
|---|---|
| Modelo base | PERO-OCR `OCR_350000.pt` (VGG_LSTM_B64_L17_S4_CB4) |
| Parámetros entrenables | 17.102.144 |
| Alfabeto | 511 caracteres |
| Hardware | NVIDIA GeForce RTX 5090 |
| Framework | PyTorch 2.11 + CUDA 12.8 |
| Entorno | Python 3.11, conda (pero_train_511) |
| Épocas | 15 |
| Optimizador | Adam (lr=1e-4, weight_decay=1e-5) |
| Scheduler | ReduceLROnPlateau (patience=2, factor=0.5) |
| Función de pérdida | CTC Loss (blank=0, zero_infinity=True) |
| line_px_height | 40 px |
| vertical_scale | 1.25 |
| cudnn | False (necesario por limitación del modelo TorchScript base) |

### 3.2. Nota técnica sobre cudnn

El modelo base `OCR_350000.pt` fue compilado con PyTorch 1.x en 2021 como modelo TorchScript. Esto produce una incompatibilidad con el backward de la capa RNN/LSTM cuando cudnn está habilitado (`cudnn RNN backward can only be called in training mode`), independientemente de la versión de PyTorch o de la GPU utilizada. La solución adoptada fue deshabilitar cudnn (`torch.backends.cudnn.enabled = False`), lo que hace que la capa RNN procese en CPU mientras las capas CNN aprovechan la GPU. Esto reduce la velocidad de entrenamiento a aproximadamente 1h30 por época.

### 3.3. Evolución del entrenamiento

| Época | train_loss | val_loss | Mejor modelo |
|---|---|---|---|
| 1 | 0.8343 | 0.2824 | ✅ |
| 2 | 0.4375 | 0.3230 | |
| 3 | 0.4050 | 0.2803 | ✅ |
| 4 | 0.3789 | 0.2837 | |
| 5 | 0.3746 | 0.2770 | ✅ |
| 6 | 0.3593 | 0.3080 | |
| 7 | 0.3563 | 0.3198 | |
| 8 | 0.3485 | 0.2944 | |
| **9** | **0.2985** | **0.2466** | **✅ (guardado)** |
| 10 | 0.2642 | 0.3054 | |
| 11 | 0.2828 | 0.3052 | |
| 12 | 0.2209 | 0.3102 | |
| 13 | 0.1818 | 0.3006 | |
| 14 | 0.1637 | 0.3516 | |
| 15 | 0.1596 | 0.3427 | |

El mejor modelo corresponde a la **época 9** (val_loss=0.2466). A partir de la época 10 el train_loss sigue bajando pero el val_loss sube, lo que indica sobreajuste leve. El modelo guardado como `mejor_modelo.pt` es el de la época 9.

El proceso de entrenamiento completo (15 épocas) duró aproximadamente **23 horas** en la RTX 5090, desde las 10:31 del 10/09/2026 hasta las 09:39 del 11/09/2026. En cada época se procesaron correctamente **14.686 de 14.696** imágenes de entrenamiento (10 imágenes descartadas por ser demasiado estrechas para el modelo, T < longitud de la transcripción).

---

## 4. Evaluación: CER y WER

### 4.1. Corpus de pruebas

La evaluación se realizó sobre un corpus de pruebas independiente de 92 páginas con transcripciones revisadas manualmente (gold standard), procedentes de las siguientes publicaciones:

- Filipinas (1909-1910)
- Filipinas Ante Europa
- Fémina (1922-1923)
- Heraldo de la Mujer (1919)
- La Vanguardia (1944)

### 4.2. Metodología de cálculo

Para cada página del corpus de pruebas se extrajo el texto generado por PERO-OCR y se comparó con el gold standard mediante la distancia de edición de Levenshtein:

- **CER (Character Error Rate):** distancia de edición a nivel de carácter dividida entre el número de caracteres del gold standard.
- **WER (Word Error Rate):** distancia de edición a nivel de palabra dividida entre el número de palabras del gold standard.

### 4.3. Resultados comparativos

| Modelo | CER medio | WER medio |
|---|---|---|
| PERO-OCR base (sin fine-tuning) | 36.78% | 52.41% |
| PERO-OCR fine-tuneado (época 9) | 36.40% | 51.93% |
| **Mejora** | **-0.38 pp** | **-0.48 pp** |

Los resultados detallados por documento están disponibles en:
- `corpus-pruebas/metricas_modelo_base.json`
- `corpus-pruebas/metricas_modelo_finetuned.json`
- `corpus-pruebas/informe_evaluacion.txt`

### 4.4. Análisis de los resultados

La mejora global es modesta (0.38 puntos porcentuales en CER). Esto se debe principalmente a dos factores:

1. **Diversidad del corpus de pruebas.** El corpus de pruebas incluye publicaciones con tipografías y estados de conservación muy distintos. El modelo se ha especializado en prensa filipina e hispana del corpus de entrenamiento, pero el corpus de pruebas incluye también La Vanguardia (1944), que presenta características tipográficas diferentes y obtiene un CER de entre el 58% y el 75% tanto con el modelo base como con el fine-tuneado.

2. **Tamaño del corpus de entrenamiento.** Con 623 páginas y 18.371 pares imagen-línea, el corpus es suficiente para un primer fine-tuning pero limitado para una especialización profunda en todas las tipografías presentes en el corpus de pruebas.

---

## 5. Transcripción de prensa filipina (prensa-franquista)

Paralelamente al fine-tuning, se procesaron y subieron al repositorio `prensa-franquista` las siguientes publicaciones filipinas:

### 5.1. Hispanidad (Filipinas, 1940)

- **Números:** 4, 5, 6, 7 y 8 (abril-agosto 1940)
- **Páginas:** 153
- **Proceso:** exportación desde Transkribus + renombrado al formato estándar del proyecto + generación de TXT desde PAGE-XML
- **Estado:** transcritas y revisadas (gold standard)

### 5.2. Yugo (Filipinas, 1938)

- **Números:** enero 1938 (páginas 4-103) y febrero 1938 (páginas 105, 109, 151)
- **Páginas:** 76
- **Proceso:** exportación desde Transkribus + renombrado + generación de TXT
- **Estado:** transcritas y revisadas (gold standard)

### 5.3. Arriba-España Manila

- **Páginas:** 208
- **Proceso:** exportación desde Transkribus (estado naranja, sin revisión humana) + corrección post-OCR con Llama 3.2 ejecutado en local mediante Ollama (sin coste de créditos). El proceso corrigió los errores de OCR directamente sobre los PAGE-XML, generando también los TXT corregidos.
- **Estado:** transcritas automáticamente con corrección post-OCR

### 5.4. Excelsior (Filipinas, 1937-1940)

- **Números:** octubre 1937 (nº 1053), febrero, mayo, junio, agosto, septiembre, octubre y noviembre 1938 (nº 1055, 1058, 1059, 1061-1064), octubre 1940 (nº 1087)
- **Páginas:** 593 JPG generados desde 9 PDFs descargados del repositorio de la Universidad de Filipinas (UPD)
- **Proceso:** conversión PDF→JPG con PyMuPDF (resolución 2x) + transcripción con el modelo PERO-OCR fine-tuneado
- **Páginas transcritas:** 589 (4 fallaron por geometría irregular en el detector de layout)
- **Estado:** transcritas automáticamente con el modelo fine-tuneado, sin revisión humana

---

## 6. Conclusiones y próximos pasos

El fine-tuning de PERO-OCR sobre el corpus de prensa histórica hispana ha producido una mejora modesta pero real en las métricas globales de CER y WER. Para mejorar la calidad de transcripción en publicaciones específicas como Excelsior se recomienda:

1. **Añadir páginas de Excelsior al corpus de entrenamiento** con su gold standard, utilizando el modelo de Transkribus ya entrenado para Excelsior como punto de partida.
2. **Ampliar el corpus de entrenamiento** con más páginas de las publicaciones presentes en el corpus de pruebas.
3. **Evaluar el CER y WER por publicación** para identificar qué publicaciones se benefician más del fine-tuning y dónde es necesario más material de entrenamiento.
4. **Explorar el post-OCR con modelos de lenguaje** (Llama 3.2, Gemini) como paso adicional para corregir los errores residuales de OCR, siguiendo el proceso ya aplicado a Arriba-España Manila.

