import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open("resultados_por_documento.json", encoding="utf-8") as f:
    docs = json.load(f)

# --- Clasificación por publicación ---
def clasificar(nombre):
    if nombre.startswith("Filipinas"):
        return "Filipinas (1909-1910)"
    if nombre.startswith("Femina") or nombre.startswith("Fémina"):
        return "Fémina (1922-1923)"
    if nombre.startswith("Heraldo"):
        return "Heraldo de la Mujer (1919)"
    if nombre.startswith("LA-VANGUARDIA"):
        return "La Vanguardia (1944)"
    return "Otros"

for d in docs:
    d["publicacion"] = clasificar(d["nombre"])

COLOR_MAIN = "#2C3E50"
COLOR_ACCENT = "#2980B9"
PUB_COLORS = {
    "Filipinas (1909-1910)": "#2980B9",
    "Fémina (1922-1923)": "#C0392B",
    "Heraldo de la Mujer (1919)": "#27AE60",
    "La Vanguardia (1944)": "#8E44AD",
}

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#999999",
    "axes.grid": True,
    "grid.color": "#dddddd",
    "grid.linewidth": 0.6,
})

# ============================================================
# Figura 1: Métricas globales — gráfico de barras
# ============================================================
metricas_globales = {
    "CER": (0.8674, False),
    "WER": (1.0570, False),
    "NED": (0.3437, False),
    "BLEU": (0.5448, True),
    "ROUGE-1": (0.7927, True),
    "ROUGE-L": (0.6789, True),
}

fig, ax = plt.subplots(figsize=(8, 4.5))
nombres = list(metricas_globales.keys())
valores = [v[0] for v in metricas_globales.values()]
colores = ["#C0392B" if not v[1] else "#27AE60" for v in metricas_globales.values()]

bars = ax.bar(nombres, valores, color=colores, edgecolor="white", width=0.6)
for bar, val in zip(bars, valores):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
            f"{val:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

ax.set_title("Métricas globales — PERO-OCR sin fine-tuning (92 documentos)")
ax.set_ylabel("Valor")
ax.set_ylim(0, 1.15)
ax.spines[["top", "right"]].set_visible(False)

from matplotlib.patches import Patch
legend_elems = [
    Patch(facecolor="#C0392B", label="Métricas de error (0 = perfecto)"),
    Patch(facecolor="#27AE60", label="Métricas de similitud (1 = perfecto)"),
]
ax.legend(handles=legend_elems, loc="upper right", fontsize=8, frameon=False)

plt.tight_layout()
plt.savefig("metricas_globales.png", dpi=150)
plt.close()

# ============================================================
# Figura 2: Métricas por documento, ordenadas (estilo "metrics-sorted")
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(13, 7))

metric_specs = [
    ("cer", "CER", "Character Error Rate", False),
    ("wer", "WER", "Word Error Rate", False),
    ("ned", "NED", "Normalized Edit Distance", False),
    ("bleu", "BLEU", "BLEU", True),
    ("rouge1", "ROUGE-1", "ROUGE-1", True),
    ("rougeL", "ROUGE-L", "ROUGE-L", True),
]

for ax, (key, title, full_name, higher_better) in zip(axes.flat, metric_specs):
    valores = sorted([d[key] for d in docs], reverse=not higher_better)
    x = np.arange(1, len(valores) + 1)
    color = "#27AE60" if higher_better else "#C0392B"
    ax.scatter(x, valores, s=10, color=color, alpha=0.75)
    ax.set_title(f"{title}\n({full_name})", fontsize=10)
    ax.set_xlabel("Documentos (ordenados)")
    ax.set_ylabel(title)
    ax.spines[["top", "right"]].set_visible(False)
    media = np.mean(valores)
    ax.axhline(media, color="#555555", linestyle="--", linewidth=1, label=f"Media = {media:.3f}")
    ax.legend(fontsize=8, frameon=False, loc="best")

fig.suptitle("Distribución de métricas por documento, ordenadas de mejor a peor (92 documentos)",
              fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("metricas_por_documento.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Figura 3: CER por publicación — boxplot
# ============================================================
publicaciones = ["Filipinas (1909-1910)", "Fémina (1922-1923)",
                  "Heraldo de la Mujer (1919)", "La Vanguardia (1944)"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# CER
data_cer = [[d["cer"] for d in docs if d["publicacion"] == p] for p in publicaciones]
bp = axes[0].boxplot(data_cer, labels=[p.split(" (")[0] for p in publicaciones],
                      patch_artist=True, showfliers=True)
for patch, p in zip(bp["boxes"], publicaciones):
    patch.set_facecolor(PUB_COLORS[p])
    patch.set_alpha(0.6)
axes[0].set_title("CER por publicación")
axes[0].set_ylabel("CER (0 = perfecto)")
axes[0].spines[["top", "right"]].set_visible(False)
axes[0].tick_params(axis="x", rotation=20)

# ROUGE-L
data_rl = [[d["rougeL"] for d in docs if d["publicacion"] == p] for p in publicaciones]
bp2 = axes[1].boxplot(data_rl, labels=[p.split(" (")[0] for p in publicaciones],
                       patch_artist=True, showfliers=True)
for patch, p in zip(bp2["boxes"], publicaciones):
    patch.set_facecolor(PUB_COLORS[p])
    patch.set_alpha(0.6)
axes[1].set_title("ROUGE-L por publicación")
axes[1].set_ylabel("ROUGE-L (1 = perfecto)")
axes[1].spines[["top", "right"]].set_visible(False)
axes[1].tick_params(axis="x", rotation=20)

fig.suptitle("Comparación de rendimiento por publicación", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("metricas_por_publicacion.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# Tabla resumen por publicación (para el README)
# ============================================================
resumen = []
for p in publicaciones:
    sub = [d for d in docs if d["publicacion"] == p]
    resumen.append({
        "publicacion": p,
        "n": len(sub),
        "cer_medio": round(float(np.mean([d["cer"] for d in sub])), 4),
        "wer_medio": round(float(np.mean([d["wer"] for d in sub])), 4),
        "bleu_medio": round(float(np.mean([d["bleu"] for d in sub])), 4),
        "rouge1_medio": round(float(np.mean([d["rouge1"] for d in sub])), 4),
        "rougeL_medio": round(float(np.mean([d["rougeL"] for d in sub])), 4),
        "ned_medio": round(float(np.mean([d["ned"] for d in sub])), 4),
    })

with open("resumen_por_publicacion.json", "w", encoding="utf-8") as f:
    json.dump(resumen, f, indent=2, ensure_ascii=False)

for r in resumen:
    print(r)

print("\nGraficas generadas: metricas_globales.png, metricas_por_documento.png, metricas_por_publicacion.png")
