import logging
import os
import tempfile

from osdagbridge.core.reports.charts import make_quantity_charts
from osdagbridge.core.reports.report_utils import _fig_embed, make_longtable
from osdagbridge.core.reports.styles import BOM_TABLE_SPEC

logger = logging.getLogger(__name__)


def ch7_quantities(input_dict):
    def _number(key):
        try:
            return float(input_dict.get(key))
        except (TypeError, ValueError):
            return None

    header = r"""\hline
\textbf{S.N.} & \textbf{Item Description} & \textbf{Volume} & \textbf{Quantity} & \textbf{Total Volume} & \textbf{Weight (MT)} & \textbf{Total Weight (MT)} \\
\hline"""
    rows = (
        r"1 & Structural Steel (IS 2062) for Girders & " + str(input_dict.get("steel_girders_vol_formula", "N.A.")) + r" & " + str(input_dict.get("steel_girders_qty", "N.A.")) + r" & " + str(input_dict.get("steel_girders_vol_total", "N.A.")) + r" & " + str(input_dict.get("steel_girders_wt_single", "N.A.")) + r" & " + str(input_dict.get("steel_girders_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"2(a) & Cross Bracing - Top Chord & " + str(input_dict.get("bracing_top_vol_formula", "N.A.")) + r" & " + str(input_dict.get("bracing_top_qty", "N.A.")) + r" & " + str(input_dict.get("bracing_top_vol_total", "N.A.")) + r" & " + str(input_dict.get("bracing_top_wt_single", "N.A.")) + r" & " + str(input_dict.get("bracing_top_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"2(b) & Cross Bracing - Bottom Chord & " + str(input_dict.get("bracing_bot_vol_formula", "N.A.")) + r" & " + str(input_dict.get("bracing_bot_qty", "N.A.")) + r" & " + str(input_dict.get("bracing_bot_vol_total", "N.A.")) + r" & " + str(input_dict.get("bracing_bot_wt_single", "N.A.")) + r" & " + str(input_dict.get("bracing_bot_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"2(c) & Cross Bracing - Diagonal Chord & " + str(input_dict.get("bracing_diag_vol_formula", "N.A.")) + r" & " + str(input_dict.get("bracing_diag_qty", "N.A.")) + r" & " + str(input_dict.get("bracing_diag_vol_total", "N.A.")) + r" & " + str(input_dict.get("bracing_diag_wt_single", "N.A.")) + r" & " + str(input_dict.get("bracing_diag_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"3 & Concrete (M40) for Deck Slab & " + str(input_dict.get("concrete_deck_vol_formula", "N.A.")) + r" & " + str(input_dict.get("concrete_deck_qty", "N.A.")) + r" & " + str(input_dict.get("concrete_deck_vol_total", "N.A.")) + r" & " + str(input_dict.get("concrete_deck_wt_single", "N.A.")) + r" & " + str(input_dict.get("concrete_deck_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"4 & Reinforcement Steel (Fe 500) & " + str(input_dict.get("rebar_deck_vol_formula", "N.A.")) + r" & " + str(input_dict.get("rebar_deck_qty", "N.A.")) + r" & " + str(input_dict.get("rebar_deck_vol_total", "N.A.")) + r" & " + str(input_dict.get("rebar_deck_wt_single", "N.A.")) + r" & " + str(input_dict.get("rebar_deck_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"5 & Shear Stud Connectors & " + str(input_dict.get("shear_studs_vol_formula", "N.A.")) + r" & " + str(input_dict.get("shear_studs_qty", "N.A.")) + r" & " + str(input_dict.get("shear_studs_vol_total", "N.A.")) + r" & " + str(input_dict.get("shear_studs_wt_single", "N.A.")) + r" & " + str(input_dict.get("shear_studs_wt_total", "N.A.")) + r" \\" + "\n\\hline\n"
        + r"6 & Crash Barrier & " + str(input_dict.get("crash_barrier_vol_formula", "N.A.")) + r" & " + str(input_dict.get("crash_barrier_qty", "N.A.")) + r" & " + str(input_dict.get("crash_barrier_vol_total", "N.A.")) + r" & " + str(input_dict.get("crash_barrier_wt_single", "N.A.")) + r" & " + str(input_dict.get("crash_barrier_wt_total", "N.A.")) + r" \\" + "\n\\hline"
    )
    chart_tex = ""
    try:
        steel = [("Girders", _number("steel_girders_wt_total"))]
        bracing = sum(value for value in (
            _number("bracing_top_wt_total"),
            _number("bracing_bot_wt_total"),
            _number("bracing_diag_wt_total"),
        ) if value is not None)
        steel.append(("Cross Bracing", bracing))
        end_diaphragm = _number("end_diaphragm_wt_total")
        if end_diaphragm is not None:
            steel.append(("End Diaphragms", end_diaphragm))
        steel = [(label, value) for label, value in steel if value is not None]
        concrete = _number("concrete_deck_vol_total")
        reinforcement = _number("rebar_deck_wt_total")
        steel_path = os.path.join(tempfile.gettempdir(), "osdagbridge_steel_quantities.png")
        material_path = os.path.join(tempfile.gettempdir(), "osdagbridge_material_quantities.png")
        make_quantity_charts(steel, concrete, reinforcement, steel_path, material_path)
        parts = []
        if steel:
            parts.append(_fig_embed(steel_path, "Structural Steel Weight", width=r"0.8\textwidth"))
        if concrete is not None or reinforcement is not None:
            parts.append(_fig_embed(material_path, "Concrete and Reinforcement Quantities", width=r"0.8\textwidth"))
        chart_tex = "\n".join(parts)
    except Exception as exc:
        logger.warning("Could not create material quantity charts: %s", exc)

    return (r"""
\chapter{Material Take-off \& Quantity Summary}
\label{ch:material-takeoff}

\begingroup
\setlength{\tabcolsep}{3.5pt}
""" + make_longtable(
        BOM_TABLE_SPEC,
        r"\textbf{Bill of Materials (Steel, Concrete, and Reinforcement Quantities)}",
        header,
        rows,
    ) + r"""
""" + chart_tex + r"""
""")
