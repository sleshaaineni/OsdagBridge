"""Small, presentation-only chart helpers for generated reports."""

from . import styles


def _save(fig, path):
    import matplotlib.pyplot as plt
    fig.savefig(path, dpi=styles.CHART_DPI, bbox_inches="tight")
    plt.close(fig)


def make_ur_chart(groups, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = []
    values = []
    for group, entries in groups.items():
        for label, value in entries:
            labels.append(f"{group}\n{label}")
            values.append(value)
    if not values:
        return False
    fig, ax = plt.subplots(figsize=styles.CHART_FIGURE_SIZE)
    colors = [styles.CHART_FAIL_COLOR if value > 1.0 else styles.CHART_PASS_COLOR for value in values]
    ax.bar(range(len(values)), values, color=colors)
    ax.axhline(1.0, color=styles.CHART_THRESHOLD_COLOR, linestyle="--", label="UR = 1.0")
    ax.set_ylabel("Utilization Ratio")
    ax.set_xticks(range(len(labels)), labels, rotation=35, ha="right")
    ax.legend()
    fig.tight_layout()
    _save(fig, path)
    return True


def make_quantity_charts(steel, concrete, reinforcement, steel_path, material_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if steel:
        fig, ax = plt.subplots(figsize=styles.CHART_FIGURE_SIZE)
        labels, values = zip(*steel)
        ax.bar(labels, values, color=styles.CHART_PASS_COLOR)
        ax.set_ylabel("Weight (MT)")
        fig.tight_layout()
        _save(fig, steel_path)
    if concrete or reinforcement:
        fig, left = plt.subplots(figsize=styles.CHART_FIGURE_SIZE)
        if concrete:
            left.bar(["Concrete"], [concrete], color="#8C8C8C")
        left.set_ylabel("Concrete volume (m³)")
        right = left.twinx()
        if reinforcement:
            right.bar(["Reinforcement"], [reinforcement], color="#4C78A8", alpha=0.8)
        right.set_ylabel("Reinforcement weight (MT)")
        fig.tight_layout()
        _save(fig, material_path)
