"""Centralized visual settings for generated OsdagBridge reports.

Only presentation values belong here. Design calculations and report data stay
in the report and analysis modules.
"""

# Page geometry
PAGE_SIZE = "a4paper"
PAGE_MARGIN = "1in"
PAGE_BOTTOM = "1.15in"
PAGE_FOOTSKIP = "24pt"
PAGE_HEADSEP = "12pt"

# Table layout
TABLE_COL_PADDING = "6pt"
TABLE_ROW_STRETCH = "1.12"
LONGTABLE_PRE_SKIP = "0pt"
LONGTABLE_POST_SKIP = "6pt"
TABLE_RULE_WIDTH = "0.5pt"
TABLE_EXTRA_ROW_HEIGHT = "0.6pt"

# Color palette
OSDAG_GREEN_NAME = "osdagGreen"
OSDAG_GREEN_HEX = "91B014"

# Document typography
DOCUMENT_FONT_SIZE = "12pt"
DOCUMENT_LINE_STRETCH = "1.15"

# Header and footer
HEADER_FOOTER_TEXT = "Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay"
HEADER_RULE_COLOR = OSDAG_GREEN_NAME
HEADER_RULE_HEIGHT = "1pt"
HEADER_RULE_VSPACE = "2pt"
FOOTER_RULE_COLOR = OSDAG_GREEN_NAME
FOOTER_RULE_VSPACE = "6pt"
PAGE_NUMBER_FORMAT = r"Page \thepage\ of \pageref{LastPage}"

# Table page-break safety
TABLE_NEEDSPACE = r"5\baselineskip"

# Extra bottom clearance for longtable rows above the footer.
TABLE_BOTTOM_CLEARANCE = "1.15in"

# Chapter 7 bill-of-materials table: total width stays within the text block.
BOM_TABLE_SPEC = r"|C{0.7cm}|L{3.1cm}|C{1.7cm}|C{1.1cm}|C{1.5cm}|C{1.3cm}|C{1.5cm}|"

# Charts
CHART_FIGURE_SIZE = (8.0, 4.5)
CHART_DPI = 150
CHART_PASS_COLOR = "#4C9F70"
CHART_FAIL_COLOR = "#D64545"
CHART_THRESHOLD_COLOR = "red"
