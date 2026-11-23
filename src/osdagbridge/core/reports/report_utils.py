from osdagbridge.core.utils.common import (
    KEY_MP_GD_MEMBER_ID,
    KEY_MP_GD_SELECT_GIRDER,
    KEY_TS_NO_OF_GIRDERS
)


def add_repeating_longtable_headers(document):
    """Add continuation headers to raw longtables in a chapter fragment.

    The report chapters are assembled as LaTeX strings rather than PyLaTeX
    objects.  Existing tables therefore already contain their captions and
    header rows, but need the ``longtable`` head markers added around them.
    This function copies the original header into the continuation head and
    leaves captions/table numbering untouched.
    """
    output = []
    cursor = 0
    begin = r"\begin{longtable}{"
    end = r"\end{longtable}"

    while True:
        start = document.find(begin, cursor)
        if start < 0:
            output.append(document[cursor:])
            break
        output.append(document[cursor:start])
        finish = document.find(end, start)
        if finish < 0:
            output.append(document[start:])
            break
        finish += len(end)
        table = document[start:finish]

        if r"\endfirsthead" in table:
            output.append(table)
            cursor = finish
            continue

        caption_end = table.find("\n", table.find(r"\caption{"))
        if caption_end < 0:
            output.append(table)
            cursor = finish
            continue
        first_hline = table.find(r"\hline", caption_end)
        second_hline = table.find(r"\hline", first_hline + len(r"\hline"))
        if first_hline < 0 or second_hline < 0:
            output.append(table)
            cursor = finish
            continue

        hline = r"\hline"
        replacement = (
            table[:second_hline + len(hline)]
            + "\n\\endfirsthead\n"
            + r"\multicolumn{1}{l}{\textit{Table \thetable\ (continued)}}\\"
            + "\n"
            + table[first_hline:second_hline + len(hline)]
            + "\n\\endhead"
            + table[second_hline + len(hline):]
        )
        output.append(replacement)
        cursor = finish

    return "".join(output)


def make_longtable(spec, caption, header, rows, continued_caption=None,
                   footer=None):
    """Build a longtable with a repeated header and stable table numbering.

    ``caption`` is emitted only in the first head.  Continuation pages use
    plain text containing ``\\thetable`` instead of a second ``\\caption`` so
    the table counter is not incremented.
    """
    continued_caption = continued_caption or r"Table \thetable\ (continued)"
    footer = footer or r"\multicolumn{1}{r}{\textit{Continued on next page}} \\"
    return (
        r"\begin{longtable}{" + spec + r"}" + "\n"
        + r"\caption{" + caption + r"}\\" + "\n"
        + header + "\n"
        + r"\endfirsthead" + "\n\n"
        + r"\multicolumn{" + _longtable_column_count(spec) + r"}{l}{\textbf{" + continued_caption + r"}}\\" + "\n"
        + header + "\n"
        + r"\endhead" + "\n\n"
        + footer + "\n"
        + r"\endfoot" + "\n"
        + rows + "\n"
        + r"\end{longtable}"
    )


def _longtable_column_count(spec):
    """Return a usable column count for a simple LaTeX column specification."""
    count = 0
    depth = 0
    i = 0
    while i < len(spec):
        if spec[i] == "{":
            depth += 1
        elif spec[i] == "}":
            depth = max(depth - 1, 0)
        elif depth == 0 and spec[i] in "lcrpmbLCRPMB":
            count += 1
        i += 1
    return str(max(count, 1))


def _tex(value):
    """Escape a Python value for safe LaTeX embedding."""
    s = str(value) if value is not None else ''
    if not s:
        return r''
    # Normalise non-ASCII glyphs from section designations (e.g. "∠ 100 ⅹ 100ⅹ 10")
    # that pdflatex cannot render.
    for uni, ascii_ in [('∠', 'L'), ('ⅹ', 'x'), ('×', 'x')]:
        s = s.replace(uni, ascii_)
    s = s.replace('\\', r'\textbackslash{}')
    for ch, esc in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'),
                    ('{', r'\{'), ('}', r'\}'),          
                    ('_', r'\_\allowbreak{}'),            
                    ('~', r'\textasciitilde{}'), ('^', r'\^{}')]:
        s = s.replace(ch, esc)
    s = s.replace(':', r':\allowbreak{}')
    return s


def _render_value(source_dict, key, unit=""):
    val = source_dict.get(key)
    if val in ("", None):
        return ""
    return _tex(val) + unit


def get_girder_entries(input_dict):
    """
    Retrieve all girder labels and member IDs from backend keys.

    Usage Example:
    --------------------------
    girder_entries = get_girder_entries(bridge.input_dict)
    
    # 1. Fallback handling (if backend hasn't populated keys yet)
    if not girder_entries:
        n = int(bridge.input_dict.get(KEY_TS_NO_OF_GIRDERS, 1))
        girder_entries = [(f"Girder {i}", f"M1") for i in range(1, n + 1)]
        
    # 2. Get total number of girders safely
    n_girders = len(girder_entries)
    
    # 3. Iterate over the girders to build table rows
    for lbl, mid in girder_entries:
        # lbl will be e.g., "G1", mid will be e.g., "G1M1"
        # Access girder specific keys dynamically:
        # val = input_dict.get(f"{KEY_MP_GIRDER_DEPTH}.{lbl}.{mid}")
        pass

    Returns:
        List[Tuple[str, str]]
    """
    n = int(input_dict.get(KEY_TS_NO_OF_GIRDERS, 0))

    entries = []

    for i in range(1, n + 1):
        entries.append(
            (
                input_dict.get(f"{KEY_MP_GD_SELECT_GIRDER}.G{i}", ""),
                input_dict.get(f"{KEY_MP_GD_MEMBER_ID}.G{i}.M1", ""),
            )
        )

    return entries


def _fig_or_placeholder(path, caption, width=r'0.9\textwidth'):
    """Embed figure if path is provided (file already copied to assets), else show placeholder box.
    path is the relative path as pdflatex will see it (e.g. 'assets/plan.png').
    """
    if path:
        p = path.replace('\\', '/')
        return (r'\begin{figure}[H]' + '\n'
                r'\centering' + '\n'
                r'\includegraphics[width=' + width + ']{' + p + '}\n'
                r'\caption*{' + caption + '}\n'
                r'\end{figure}')
    return (r'\begin{figure}[H]' + '\n'
            r'\centering' + '\n'
            r'\fbox{\parbox{0.97\textwidth}{' + '\n'
            r'\textit{[ PLACEHOLDER: ' + caption + r' ]}' + '\n'
            r'}}' + '\n'
            r'\caption*{' + caption + '}\n'
            r'\end{figure}')

def _fig_embed(path, caption, width=r'\textwidth', height=None):
    """Embed a real figure when path is provided (already copied); otherwise use an fbox placeholder."""
    if path:
        p = path.replace('\\', '/')
        opts = 'width=' + width
        if height:
            opts += ',height=' + height + ',keepaspectratio'
        return (r'\begin{figure}[H]' + '\n'
                r'\vspace{-0.5em}' + '\n'
                r'\centering' + '\n'
                r'\includegraphics[' + opts + ']{' + p + '}\n'
                r'\vspace{0.5em}' + '\n'
                r'\caption*{\small ' + caption + '}\n'
                r'\vspace{-0.5em}' + '\n'
                r'\end{figure}')
    # fbox placeholder — matches template exactly
    return (r'\noindent\fbox{\parbox{0.97\textwidth}{' + '\n'
            r'\textit{[ PLACEHOLDER: ' + caption + r' ]}' + '\n'
            r'}}')
