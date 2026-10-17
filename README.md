# Business Intelligence – Tarea 4: Introducción a Series de Tiempo

Noel Eduardo Sánchez Useda · Universidad del Istmo · Entrega: 25 de octubre de 2026

Análisis de la venta diaria del dataset *Online Retail* (UCI): procesos simulados (Parte 0),
limpieza (1), calendario (2), tendencia y estacionalidad (3), SARIMA (4), pronóstico con
origen móvil y fuga de información (5) y análisis RFM (6).

## Contenido

```
data/Online_Retail.xlsx   datos originales (UCI Machine Learning Repository)
src/limpiar.py            función limpiar(df, devolver_bitacora=False)
Tarea4.ipynb              notebook con todas las partes, de principio a fin
figures/                  figuras generadas por el notebook
tables/                   tablas (.csv) generadas por el notebook
report/                   documento: Tarea4_BI.tex y Tarea4_BI.pdf (con las figuras)
requirements.txt          dependencias
```

## Cómo ejecutarlo

Se necesita [uv](https://docs.astral.sh/uv/) y Python 3.10 o superior.

```bash
# 1. Entrar a la carpeta del repositorio
cd bi-tarea4-series-de-tiempo

# 2. Crear el entorno e instalar las dependencias (solo la primera vez)
uv venv
uv pip install -r requirements.txt

# 3. Abrir Jupyter
uv run jupyter notebook
```

Abrir `Tarea4.ipynb` y elegir **Kernel → Restart & Run All**. El notebook lee
`data/Online_Retail.xlsx`, importa `limpiar` desde `src/` y regenera todas las cifras,
las figuras (`figures/`) y las tablas (`tables/`) del documento. La ejecución completa
tarda unos minutos (la lectura del `.xlsx` y los reajustes SARIMA de la Parte 5 son lo más lento).

Para recompilar el documento: subir `report/Tarea4_BI.tex` y las figuras de `figures/` a
Overleaf (o compilar con `pdflatex` con las figuras en la misma carpeta).

## Semillas

| Parte | Semilla |
|---|---|
| 0, réplicas del escenario *i* | `SEED_BASE + i`, con `SEED_BASE = 2026` |
| 0, realizaciones de la figura | `SEED_BASE + 100 + i` |
| 0.4, procesos (a) tendencia y (b) patrón semanal | `SEED_BASE + 10` y `SEED_BASE + 11` |
| 5.2 (a), validación cruzada aleatoria | `2026, 2027, …, 2035` (10 repeticiones) |
| 6.2, desempate de quintiles | `numpy.random.default_rng(2026)` |

## Decisiones principales

- **Limpieza** (`src/limpiar.py`): se eliminan duplicados exactos, facturas con prefijo `A`,
  ventas anuladas por una cancelación manual (`M`), códigos que no son productos, precios
  ≤ 0 y cantidades negativas sin `C`. Se conservan las cancelaciones (`C`) y las filas sin
  `CustomerID` (la Parte 6 las excluye por su cuenta). La bitácora (reglas en orden de
  aplicación) está en el documento, Cuadro 1.3.
- **Serie diaria**: calendario completo del 1 de dic. de 2010 al 8 de dic. de 2011 (el 9 de
  dic. se descarta por estar incompleto); los días cerrados son datos faltantes.

## Uso de herramientas de IA

Se usó Claude (Anthropic) como apoyo para estructurar el código, redactar borradores y revisar
explicaciones. El autor ejecutó el código, comparó los resultados y escribió y corrigió las
respuestas de análisis. El detalle, con ejemplos, está en la última sección del documento.
