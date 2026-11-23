# OsdagBridge Report-Generator Project History

## 1. Starting point

The original OsdagBridge report was generated with PyLaTeX, but it had several
presentation problems:

- multi-page tables did not consistently repeat their headers;
- vehicle and footpath live loads were combined poorly;
- some dimensions were displayed in the wrong unit;
- tables had inconsistent widths and spacing;
- utilization and material quantities had no visual summary;
- some figure assets were not reaching the report generator;
- some report fields were blank or unclear;
- figure placeholders used generic template wording.

The baseline file was preserved as `Report_Before.pdf`.

## 2. Work completed

### Centralized styling

Created `src/osdagbridge/core/reports/styles.py` as the shared source for page
geometry, table spacing, colors, typography, header/footer values, and chart
settings.

### Longtable support

Added reusable longtable helpers in `report_utils.py` and converted report tables
to continuation-header format. Tables such as the load combinations, girder
properties, stiffener checks, deflection checks, and overall design summary now
show continuation headers in the generated PDF.

### Chapter 3 load presentation

Separated vehicle live loads and footpath live loads. Vehicle rows are created
from the selected input flags instead of a hardcoded display list. Braking,
impact-factor, eccentricity, and available load values are displayed in their
own columns.

The footpath logic was corrected to use the actual bridge geometry selection.
When the input is `Footpath = None`, the report now shows `No footpath selected.`

### Chapter 2 units and table alignment

Girder section dimensions stored in metres are converted for display to the
millimetre units declared by the table. For example, `1.67 mm` became
`1670 mm`.

The initial Chapter 2 tables were also widened to align with the page text block.
The Executive Summary input table received the same width treatment, and units
were added to girder spacing and deck thickness fields.

### Utilization-ratio chart

Added chart generation in `charts.py`. The chart uses existing report/design
values, draws a red dashed UR = 1.0 line, and colors passing and failing bars
differently. It is embedded in the overall design-check section.

### Material quantity charts

Added Chapter 7 charts for structural steel and concrete/reinforcement
quantities. The chart values come from the dynamically calculated BOQ quantity
dictionary rather than hardcoded report values.

### Figure handling

Replaced generic `PLACEHOLDER` wording with an informative unavailable-figure
message. The existing headless CAD export method was connected to the report
payload so successfully exported CAD images can be transferred into the LaTeX
build.

## 3. Validation performed

- Python syntax checks passed for the modified report and CAD handoff modules.
- `git diff --check` passed.
- Multiple generated reports were inspected: Test6, Test7, Test8, and the newer
  After_Report1 output.
- The final selected report contains 68 physical pages.
- Repeated longtable headers were confirmed.
- Chapter 2 table alignment and corrected dimensions were visually checked.
- The footpath-none message was confirmed.
- The UR chart and material charts were confirmed as present.
- The newer After_Report1 output was selected because its affected tables fit
  better than the earlier After_Report output.

## 4. Known limitations to disclose

- The footer currently reports `of 67` although the PDF has 68 physical pages.
- Some engineering figures remain unavailable in the generated report. No
  unrelated or fabricated drawing was inserted.
- Table 5.4 still requires a final robust multirow-pagination redesign.
- End Diaphragm material quantity is not populated by the current BOQ source,
  so it is not shown as a distinct quantity category.
- Some wind and horizontal seismic force fields remain blank because the
  backend does not provide report-ready values for them.
- The references contain an IRC 5 year that should be cross-checked against the
  implementation's IRC 5:2015 source naming.

## 5. Final deliverables prepared

- `Report_Before.pdf`
- `After_Report.pdf`
- `After_Report.tex`
- `TECHNICAL_CHANGES.md`
- `IMPLEMENTATION_AUDIT.md`
- `CHANGELOG.md`
- `OsdagBridge_Report_Submission.zip`

