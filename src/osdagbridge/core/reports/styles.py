"""Centralized visual settings for generated OsdagBridge reports.

Only presentation values belong here. Design calculations and report data stay
in the report and analysis modules.
"""

# Page geometry
PAGE_SIZE = "a4paper"
PAGE_MARGIN = "1in"

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

