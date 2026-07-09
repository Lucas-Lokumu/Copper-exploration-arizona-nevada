from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# =========================
# 1. Chemins du projet
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_MRDS = BASE_DIR / "MRDS_copper_AZ_NV.gpkg"
DATA_HIGH_CONTEXT = BASE_DIR / "high_potential_10km_mining_points_count.gpkg"

OUTPUT_TABLES = BASE_DIR / "outputs" / "tables"
OUTPUT_FIGURES = BASE_DIR / "outputs" / "figures"

OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

# =========================
# 2. Lecture des données
# =========================

mrds = gpd.read_file(DATA_MRDS)
high_context = gpd.read_file(DATA_HIGH_CONTEXT)

print("MRDS copper:", mrds.shape)
print("High potential + context:", high_context.shape)

# =========================
# 3. Statistiques principales
# =========================

potential_stats = (
    mrds["classe_potentiel"]
    .value_counts()
    .reset_index()
)
potential_stats.columns = ["classe_potentiel", "count"]

high_sites = mrds[mrds["classe_potentiel"] == "Élevé"].copy()

high_by_state = (
    high_sites["state"]
    .value_counts()
    .reset_index()
)
high_by_state.columns = ["state", "count"]

high_by_county = (
    high_sites["county"]
    .value_counts()
    .reset_index()
)
high_by_county.columns = ["county", "count"]

mining_context_stats = (
    high_context["contexte_minier"]
    .value_counts()
    .reset_index()
)
mining_context_stats.columns = ["contexte_minier", "count"]

priority_counties = (
    high_context["county"]
    .value_counts()
    .reset_index()
)
priority_counties.columns = ["county", "count"]

# =========================
# 4. Réordonner les catégories
# =========================

potential_order = ["Faible", "Moyen", "Élevé"]
context_order = ["Faible", "Moyen", "Fort", "Très fort"]

potential_stats = (
    potential_stats
    .set_index("classe_potentiel")
    .reindex(potential_order)
    .reset_index()
)

mining_context_stats = (
    mining_context_stats
    .set_index("contexte_minier")
    .reindex(context_order)
    .reset_index()
)

# =========================
# 5. Export CSV
# =========================

potential_stats.to_csv(OUTPUT_TABLES / "stats_potential_classes.csv", index=False, encoding="utf-8-sig")
high_by_state.to_csv(OUTPUT_TABLES / "stats_high_potential_by_state.csv", index=False, encoding="utf-8-sig")
high_by_county.to_csv(OUTPUT_TABLES / "stats_high_potential_by_county.csv", index=False, encoding="utf-8-sig")
mining_context_stats.to_csv(OUTPUT_TABLES / "stats_high_potential_by_mining_context.csv", index=False, encoding="utf-8-sig")
priority_counties.to_csv(OUTPUT_TABLES / "stats_final_priority_by_county.csv", index=False, encoding="utf-8-sig")

# =========================
# 6. Graphiques améliorés
# =========================

def add_value_labels(ax, horizontal=False):
    if horizontal:
        for bar in ax.patches:
            width = bar.get_width()
            ax.text(
                width + 0.2,
                bar.get_y() + bar.get_height() / 2,
                f"{int(width)}",
                va="center",
                fontsize=10
            )
    else:
        for bar in ax.patches:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height)}",
                ha="center",
                va="bottom",
                fontsize=10
            )


def save_bar_chart_custom(
    df,
    x_col,
    y_col,
    title,
    filename,
    colors=None,
    horizontal=False,
    xlabel="",
    ylabel="Nombre de sites"
):
    fig, ax = plt.subplots(figsize=(9, 5))

    if horizontal:
        df_plot = df.sort_values(y_col)
        color_values = [colors.get(x, "#1f77b4") for x in df_plot[x_col]] if colors else None

        ax.barh(df_plot[x_col], df_plot[y_col], color=color_values)
        ax.set_xlabel(xlabel if xlabel else "Nombre de sites")
        ax.set_ylabel("")
        add_value_labels(ax, horizontal=True)

    else:
        color_values = [colors.get(x, "#1f77b4") for x in df[x_col]] if colors else None

        ax.bar(df[x_col], df[y_col], color=color_values)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        add_value_labels(ax, horizontal=False)

    ax.set_title(title, fontsize=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES / filename, dpi=300)
    plt.close()


potential_colors = {
    "Faible": "#F2E85C",
    "Moyen": "#F4A340",
    "Élevé": "#E31A1C"
}

context_colors = {
    "Faible": "#BDBDBD",
    "Moyen": "#F2E85C",
    "Fort": "#F4A340",
    "Très fort": "#E31A1C"
}

state_colors = {
    "Arizona": "#F4A340",
    "Nevada": "#E31A1C"
}

save_bar_chart_custom(
    potential_stats,
    "classe_potentiel",
    "count",
    "Répartition des sites cuivre par classe de potentiel",
    "fig_potential_classes.png",
    colors=potential_colors
)

save_bar_chart_custom(
    high_by_state,
    "state",
    "count",
    "Sites cuivre à potentiel élevé par État",
    "fig_high_potential_by_state.png",
    colors=state_colors
)

save_bar_chart_custom(
    mining_context_stats,
    "contexte_minier",
    "count",
    "Contexte minier historique autour des sites élevés",
    "fig_mining_context.png",
    colors=context_colors
)

save_bar_chart_custom(
    priority_counties.head(12),
    "county",
    "count",
    "Principaux comtés prioritaires",
    "fig_priority_counties.png",
    horizontal=True,
    xlabel="Nombre de sites"
)

# =========================
# 7. Résumé console
# =========================

print("\n=== Classes de potentiel ===")
print(potential_stats)

print("\n=== Sites élevés par État ===")
print(high_by_state)

print("\n=== Contexte minier ===")
print(mining_context_stats)

print("\n=== Top comtés prioritaires ===")
print(priority_counties.head(12))

print("\nExports terminés.")