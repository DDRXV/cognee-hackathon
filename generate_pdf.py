"""
Generate: Self-Evolving GTM Brain — 2-pager PDF
Diagrams drawn with reportlab vector graphics (no external image deps).
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Polygon, Circle,
    Group, Path
)
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Flowable
import os

W, H = A4
BRAND_DARK  = colors.HexColor("#0F172A")
BRAND_BLUE  = colors.HexColor("#2563EB")
BRAND_CYAN  = colors.HexColor("#06B6D4")
BRAND_GREEN = colors.HexColor("#10B981")
BRAND_RED   = colors.HexColor("#EF4444")
BRAND_AMBER = colors.HexColor("#F59E0B")
BRAND_GRAY  = colors.HexColor("#64748B")
BRAND_LIGHT = colors.HexColor("#F1F5F9")
BRAND_WHITE = colors.white

styles = getSampleStyleSheet()

def S(name, **kw):
    base = styles[name]
    return ParagraphStyle(name + str(id(kw)), parent=base, **kw)

H1 = S("Heading1", fontSize=20, textColor=BRAND_DARK, spaceAfter=4, spaceBefore=0, leading=24)
H2 = S("Heading2", fontSize=12, textColor=BRAND_BLUE, spaceAfter=3, spaceBefore=6, leading=15)
H3 = S("Heading3", fontSize=9,  textColor=BRAND_GRAY, spaceAfter=2, spaceBefore=2, leading=12)
BODY = S("Normal", fontSize=8.5, textColor=BRAND_DARK, leading=13, spaceAfter=3)
SMALL = S("Normal", fontSize=7.5, textColor=BRAND_GRAY, leading=11)
CAPTION = S("Normal", fontSize=7, textColor=BRAND_GRAY, leading=10, alignment=TA_CENTER)
BADGE = S("Normal", fontSize=7, textColor=BRAND_WHITE, leading=9, alignment=TA_CENTER)
MONO = S("Code", fontSize=7.5, textColor=BRAND_BLUE, leading=11,
         fontName="Courier", backColor=BRAND_LIGHT)


# ── Flowable wrapper around a reportlab Drawing ──────────────────────────────
class DiagramFlowable(Flowable):
    def __init__(self, drawing):
        super().__init__()
        self.drawing = drawing
        self.width  = drawing.width
        self.height = drawing.height

    def draw(self):
        renderPDF.draw(self.drawing, self.canv, 0, 0)

    def wrap(self, aw, ah):
        return self.width, self.height


# ── Helper drawing primitives ─────────────────────────────────────────────────
def box(d, x, y, w, h, fill, stroke=None, radius=4):
    r = Rect(x, y, w, h, rx=radius, ry=radius,
             fillColor=fill,
             strokeColor=stroke or fill,
             strokeWidth=1 if stroke else 0)
    d.add(r)

def label(d, x, y, text, color=BRAND_WHITE, size=7.5, bold=False, align="middle"):
    fn = "Helvetica-Bold" if bold else "Helvetica"
    s = String(x, y, text, fontSize=size, fillColor=color,
               fontName=fn, textAnchor=align)
    d.add(s)

def arrow_h(d, x1, x2, y, color=BRAND_GRAY, label_text=""):
    d.add(Line(x1, y, x2, y, strokeColor=color, strokeWidth=1.2))
    # arrowhead
    dx = 4 if x2 > x1 else -4
    d.add(Polygon([x2, y, x2-dx, y+3, x2-dx, y-3],
                  fillColor=color, strokeColor=color, strokeWidth=0))
    if label_text:
        mid = (x1+x2)/2
        label(d, mid, y+4, label_text, color=BRAND_GRAY, size=6, align="middle")

def arrow_v(d, x, y1, y2, color=BRAND_GRAY, label_text=""):
    d.add(Line(x, y1, x, y2, strokeColor=color, strokeWidth=1.2))
    dy = 4 if y2 > y1 else -4
    d.add(Polygon([x, y2, x-3, y2-dy, x+3, y2-dy],
                  fillColor=color, strokeColor=color, strokeWidth=0))
    if label_text:
        mid = (y1+y2)/2
        label(d, x+5, mid, label_text, color=BRAND_GRAY, size=6, align="start")


# ── DIAGRAM 1: Architecture (two-layer memory) ────────────────────────────────
def make_architecture_diagram():
    W_d, H_d = 480, 160
    d = Drawing(W_d, H_d)

    # Background
    box(d, 0, 0, W_d, H_d, BRAND_LIGHT, radius=6)

    # Title band
    box(d, 0, H_d-22, W_d, 22, BRAND_DARK, radius=0)
    label(d, W_d/2, H_d-13, "TWO-LAYER MEMORY ARCHITECTURE", BRAND_WHITE, 8, bold=True)

    # Layer 1 — Ingestion
    bx, by, bw, bh = 10, 80, 90, 60
    box(d, bx, by, bw, bh, BRAND_BLUE, radius=5)
    label(d, bx+bw/2, by+bh-12, "INGESTION", BRAND_WHITE, 7, bold=True)
    label(d, bx+bw/2, by+bh-24, "SDR Playbook", BRAND_WHITE, 6.5)
    label(d, bx+bw/2, by+bh-34, "ICP Profiles", BRAND_WHITE, 6.5)
    label(d, bx+bw/2, by+bh-44, "Prospects (dlt)", BRAND_WHITE, 6.5)

    # Arrow 1→2
    arrow_h(d, bx+bw, 155, by+bh/2, BRAND_BLUE, "cognee.add()")

    # Layer 2 — Cognee graph
    cx, cy, cw, ch = 155, 60, 110, 80
    box(d, cx, cy, cw, ch, BRAND_DARK, radius=5)
    label(d, cx+cw/2, cy+ch-12, "COGNEE", BRAND_CYAN, 8, bold=True)
    label(d, cx+cw/2, cy+ch-24, "Knowledge Graph", BRAND_WHITE, 6.5)
    label(d, cx+cw/2, cy+ch-34, "Entities + Relations", BRAND_WHITE, 6)
    label(d, cx+cw/2, cy+ch-44, "Graph DB (Ladybug)", BRAND_GRAY, 6)
    label(d, cx+cw/2, cy+ch-56, "Vector Index (LanceDB)", BRAND_GRAY, 6)

    # Arrow 2→3
    arrow_h(d, cx+cw, 310, cy+ch/2, BRAND_CYAN, "cognee.search()")

    # Layer 3 — Retrieval
    rx, ry, rw, rh = 310, 70, 90, 60
    box(d, rx, ry, rw, rh, colors.HexColor("#064E3B"), radius=5)
    label(d, rx+rw/2, ry+rh-12, "RETRIEVAL", BRAND_GREEN, 7, bold=True)
    label(d, rx+rw/2, ry+rh-24, "GRAPH_COMPLETION", BRAND_WHITE, 6)
    label(d, rx+rw/2, ry+rh-34, "Multi-hop reasoning", BRAND_WHITE, 6)
    label(d, rx+rw/2, ry+rh-44, "GTM intelligence", BRAND_WHITE, 6)

    # Arrow 3→4
    arrow_h(d, rx+rw, 445, ry+rh/2, BRAND_GREEN, "Answers")

    # Layer 4 — SDR output
    ox, oy, ow, oh = 445, 80, 28, 40
    box(d, ox, oy, ow, oh, BRAND_GREEN, radius=4)
    label(d, ox+ow/2, oy+oh/2+4,  "SDR", BRAND_WHITE, 6.5, bold=True)
    label(d, ox+ow/2, oy+oh/2-6, "Gets", BRAND_WHITE, 6)
    label(d, ox+ow/2, oy+oh/2-16, "Answer", BRAND_WHITE, 6)

    # Redis box — bottom
    redis_x, redis_y = 155, 8
    box(d, redis_x, redis_y, 110, 38, colors.HexColor("#7F1D1D"), radius=5)
    label(d, redis_x+55, redis_y+27, "REDIS", colors.HexColor("#FCA5A5"), 7.5, bold=True)
    label(d, redis_x+55, redis_y+17, "Real-time signal cache", BRAND_WHITE, 6)
    label(d, redis_x+55, redis_y+7,  "Deal outcomes  (24h TTL)", BRAND_GRAY, 5.5)

    # Arrow: outcomes → redis (dashed feel, use short line)
    arrow_v(d, redis_x+55, cy, redis_y+38, colors.HexColor("#FCA5A5"), "outcomes")

    # Caption row
    label(d, W_d/2, 2, "Cognee = persistent brain  |  Redis = real-time buffer  |  LanceDB = vector index",
          BRAND_GRAY, 5.5, align="middle")

    return d


# ── DIAGRAM 2: 4-Stage Pipeline Flow ─────────────────────────────────────────
def make_pipeline_diagram():
    W_d, H_d = 480, 110
    d = Drawing(W_d, H_d)
    box(d, 0, 0, W_d, H_d, BRAND_LIGHT, radius=6)
    box(d, 0, H_d-20, W_d, 20, BRAND_DARK, radius=0)
    label(d, W_d/2, H_d-12, "4-STAGE DEMO PIPELINE", BRAND_WHITE, 8, bold=True)

    stages = [
        ("01", "INGEST",   "SDR Playbook\nICP Profiles\nProspects (dlt)", BRAND_BLUE),
        ("02", "RETRIEVE", "ICP Ranking\nOutreach Angles\nObjection Prep",  colors.HexColor("#7C3AED")),
        ("03", "AUDIT",    "Knowledge Wiki\n7-Section Lint\nGraph Edges",   colors.HexColor("#0891B2")),
        ("04", "EVOLVE",   "Redis Buffer\nCognee Update\nBefore/After",     BRAND_GREEN),
    ]

    sw = 95
    gap = 12
    start_x = 8

    for i, (num, title, desc, col) in enumerate(stages):
        sx = start_x + i*(sw+gap)
        sy = 12
        sh = 68

        box(d, sx, sy, sw, sh, col, radius=5)
        # Number badge
        box(d, sx+4, sy+sh-16, 18, 14, BRAND_WHITE, radius=3)
        label(d, sx+13, sy+sh-7, num, col, 7, bold=True)

        label(d, sx+sw/2, sy+sh-26, title, BRAND_WHITE, 7.5, bold=True)

        # Description lines
        lines = desc.split("\n")
        for j, line in enumerate(lines):
            label(d, sx+sw/2, sy+sh-38-j*11, line, BRAND_WHITE, 6)

        # Arrow between stages
        if i < len(stages)-1:
            ax = sx + sw + 1
            ay = sy + sh/2
            arrow_h(d, ax, ax+gap-2, ay, BRAND_GRAY)

    return d


# ── DIAGRAM 3: Self-Evolution Loop ───────────────────────────────────────────
def make_evolution_diagram():
    W_d, H_d = 480, 150
    d = Drawing(W_d, H_d)
    box(d, 0, 0, W_d, H_d, BRAND_LIGHT, radius=6)
    box(d, 0, H_d-20, W_d, 20, BRAND_DARK, radius=0)
    label(d, W_d/2, H_d-12, "SELF-EVOLUTION LOOP", BRAND_WHITE, 8, bold=True)

    # Nodes
    nodes = [
        (50,  65, 80, 44, "DEAL\nCLOSES",   BRAND_AMBER),
        (168, 65, 90, 44, "REDIS\nHSET",     colors.HexColor("#991B1B")),
        (296, 65, 90, 44, "COGNEE\ncognify()", BRAND_BLUE),
        (414, 65, 58, 44, "BETTER\nANSWERS", BRAND_GREEN),
    ]
    for (nx, ny, nw, nh, ntxt, ncol) in nodes:
        box(d, nx, ny, nw, nh, ncol, radius=5)
        lines = ntxt.split("\n")
        for j, ln in enumerate(lines):
            label(d, nx+nw/2, ny+nh/2+6-j*12, ln, BRAND_WHITE, 7.5, bold=True)

    # Arrows between nodes
    gaps = [
        (nodes[0][0]+nodes[0][2], nodes[1][0], nodes[0][1]+nodes[0][3]/2, "outcome\narrives"),
        (nodes[1][0]+nodes[1][2], nodes[2][0], nodes[1][1]+nodes[1][3]/2, "crystallise\nto graph"),
        (nodes[2][0]+nodes[2][2], nodes[3][0], nodes[2][1]+nodes[2][3]/2, "new\nvectors"),
    ]
    for (x1, x2, y, lbl) in gaps:
        mid_x = (x1+x2)/2
        arrow_h(d, x1, x2, y, BRAND_GRAY)
        lines = lbl.split("\n")
        for j, ln in enumerate(lines):
            label(d, mid_x, y+10-j*8, ln, BRAND_GRAY, 5.5, align="middle")

    # Feedback loop arc: answers → better playbook → next SDR
    # Draw as a curved path approximation with lines + label
    fy = 30
    d.add(Line(nodes[3][0]+nodes[3][2]/2, nodes[3][1],
               nodes[3][0]+nodes[3][2]/2, fy,
               strokeColor=BRAND_GREEN, strokeWidth=1.2))
    d.add(Line(nodes[3][0]+nodes[3][2]/2, fy,
               nodes[0][0]+nodes[0][2]/2, fy,
               strokeColor=BRAND_GREEN, strokeWidth=1.2))
    d.add(Line(nodes[0][0]+nodes[0][2]/2, fy,
               nodes[0][0]+nodes[0][2]/2, nodes[0][1],
               strokeColor=BRAND_GREEN, strokeWidth=1.2))
    # Arrowhead pointing down
    ax = nodes[0][0]+nodes[0][2]/2
    d.add(Polygon([ax, nodes[0][1], ax-3, nodes[0][1]+5, ax+3, nodes[0][1]+5],
                  fillColor=BRAND_GREEN, strokeColor=BRAND_GREEN, strokeWidth=0))
    label(d, W_d/2, fy-8,
          "Every deal makes every future SDR smarter",
          BRAND_GREEN, 6.5, bold=True, align="middle")

    # Bottom labels
    annotations = [
        (nodes[0][0]+nodes[0][2]/2, 57, "e.g. BuildFast\n$120K WON"),
        (nodes[1][0]+nodes[1][2]/2, 57, "Fast write\n24h TTL"),
        (nodes[2][0]+nodes[2][2]/2, 57, "Permanent\ngraph update"),
        (nodes[3][0]+nodes[3][2]/2, 57, "ROI framing\nnow in brain"),
    ]
    for (ax2, ay, atxt) in annotations:
        for j, ln in enumerate(atxt.split("\n")):
            label(d, ax2, ay-j*8, ln, BRAND_GRAY, 5.5, align="middle")

    return d


# ── BUILD PDF ─────────────────────────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=18*mm,
        rightMargin=18*mm,
        topMargin=14*mm,
        bottomMargin=14*mm,
    )

    story = []

    # ── PAGE 1 ────────────────────────────────────────────────────────────────

    # Header bar (simulated with a table)
    header_data = [[
        Paragraph("<b>SELF-EVOLVING GTM BRAIN</b>", S("Normal", fontSize=18, textColor=BRAND_WHITE, leading=22)),
        Paragraph("SkillAgents AI &times; Cognee &times; Redis<br/><font size=8 color='#94A3B8'>Redis + Cognee Knowledge Graph Hackathon 2026</font>",
                  S("Normal", fontSize=10, textColor=BRAND_CYAN, leading=14, alignment=TA_RIGHT)),
    ]]
    header_table = Table(header_data, colWidths=[110*mm, 65*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BRAND_DARK),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [6,6,6,6]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 5*mm))

    # Problem + Solution side-by-side
    problem = [
        Paragraph("THE PROBLEM", H2),
        Paragraph(
            "B2B sales teams <b>lose $1.2M in institutional knowledge</b> every time "
            "a rep leaves. Every SDR starts from zero — same objections, same mistakes, "
            "same 3-month ramp. CRMs record <i>what</i> happened. They cannot reason "
            "about <i>why</i>, and they cannot teach the next rep.",
            BODY),
        Spacer(1, 2*mm),
        Paragraph("THE SOLUTION", H2),
        Paragraph(
            "A <b>self-evolving GTM brain</b> that accumulates every deal outcome into "
            "a persistent knowledge graph. Each closed deal — win or loss — makes every "
            "future SDR smarter. The agent never forgets.",
            BODY),
    ]
    solution_badges = [
        ("Cognee",   "Persistent knowledge graph — entities, relationships, learned facts", BRAND_BLUE),
        ("Redis",    "Real-time signal cache — deal outcomes buffered before graph update",  colors.HexColor("#991B1B")),
        ("dlt",      "Typed FK edges: company → signals / tech_stack / contacts",           colors.HexColor("#7C3AED")),
        ("LanceDB",  "Vector index powering semantic graph retrieval",                      BRAND_GRAY),
    ]
    badge_rows = []
    for name, desc, col in solution_badges:
        badge_rows.append([
            Paragraph(f"<b>{name}</b>",
                      S("Normal", fontSize=7.5, textColor=BRAND_WHITE, backColor=col,
                        leading=10, alignment=TA_CENTER)),
            Paragraph(desc, SMALL),
        ])

    badge_table = Table(badge_rows, colWidths=[18*mm, 55*mm])
    badge_table.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [BRAND_LIGHT, BRAND_WHITE]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS", (0,0), (0,-1), [3,3,3,3]),
    ]))

    two_col = Table(
        [[problem, badge_table]],
        colWidths=[90*mm, 80*mm],
    )
    two_col.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
    ]))
    story.append(two_col)
    story.append(Spacer(1, 4*mm))

    # Architecture diagram
    story.append(Paragraph("ARCHITECTURE — TWO-LAYER MEMORY", H2))
    story.append(DiagramFlowable(make_architecture_diagram()))
    story.append(Paragraph(
        "Cognee maintains the persistent knowledge graph (entities, relationships, learned facts) "
        "using Ladybug graph DB + LanceDB vector index. Redis acts as the real-time signal buffer "
        "— deal outcomes land there first (HSET, 24h TTL), then get crystallised into Cognee's "
        "graph via <font name='Courier' size=7.5>cognify()</font>.",
        SMALL))
    story.append(Spacer(1, 4*mm))

    # Pipeline diagram
    story.append(Paragraph("4-STAGE DEMO PIPELINE", H2))
    story.append(DiagramFlowable(make_pipeline_diagram()))

    stage_rows = [
        ["Stage", "Command", "What it shows", "Key output"],
        ["01 INGEST",   "python 01_ingest.py",  "Mixed ingestion: text + dlt resource", "84 graph nodes, 228 edges, FK edges between companies/signals/tech"],
        ["02 RETRIEVE", "python 02_retrieve.py","Agentic reasoning across graph",        "ICP ranking, personalised outreach email, objection playbook"],
        ["03 AUDIT",    "python 03_lint.py",    "7-section knowledge wiki",              "What the AI brain actually knows (Karpathy-style LLM.txt)"],
        ["04 EVOLVE",   "python 04_evolve.py",  "Self-evolution: before → after",        "Redis +2 signals, Cognee updated, same query returns richer answer"],
    ]
    stage_table = Table(stage_rows, colWidths=[22*mm, 38*mm, 55*mm, 60*mm])
    stage_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BRAND_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0), BRAND_WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [BRAND_LIGHT, BRAND_WHITE]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#CBD5E1")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(stage_table)

    # Page break
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    # ── PAGE 2 ────────────────────────────────────────────────────────────────

    story.append(Paragraph("SELF-EVOLUTION LOOP — THE WOW MOMENT", H1))
    story.append(Paragraph(
        "Stage 4 closes the feedback loop. Two deal outcomes are fed in — a win and a stall — "
        "demonstrating the two-layer memory model in action.",
        BODY))
    story.append(Spacer(1, 3*mm))
    story.append(DiagramFlowable(make_evolution_diagram()))
    story.append(Spacer(1, 2*mm))

    # Before / After comparison
    story.append(Paragraph("BEFORE vs AFTER — Same Query, Smarter Answer", H2))
    ba_rows = [
        ["", "BEFORE evolution", "AFTER evolution"],
        ["Query",
         "Best outreach angle for BuildFast SaaS?",
         "Best outreach angle for BuildFast SaaS?"],
        ["Answer\nquality",
         "Generic ICP B framing. Copilot/Cursor gap mentioned. No ROI data. No close-time reference.",
         "ROI math anchored to CTO's own LinkedIn post. $240K ramp cost quantified. '18-day close' cited. Compliance brief for FinServ added."],
        ["What\nchanged",
         "—",
         "Cognee extracted 'ROI quantification', 'CTO public statement', '18-day close pattern' as graph nodes. LanceDB has new embedding vectors. Redis has 2 cached signals."],
    ]
    ba_table = Table(ba_rows, colWidths=[20*mm, 75*mm, 80*mm])
    ba_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BRAND_DARK),
        ("TEXTCOLOR",     (0,0), (-1,0), BRAND_WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND",    (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ("FONTNAME",      (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [BRAND_LIGHT, BRAND_WHITE, BRAND_LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#CBD5E1")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TEXTCOLOR",     (1,1), (1,-1), BRAND_GRAY),
        ("TEXTCOLOR",     (2,1), (2,-1), colors.HexColor("#064E3B")),
    ]))
    story.append(ba_table)
    story.append(Spacer(1, 4*mm))

    # Data model
    story.append(Paragraph("DATA MODEL — dlt FK Edges", H2))
    story.append(Paragraph(
        "Structured prospect data is ingested via a typed "
        "<font name='Courier' size=7.5>@dlt.resource</font>. "
        "Nested arrays become separate tables with <font name='Courier' size=7.5>company_id</font> "
        "foreign keys, which Cognee maps to graph edges:",
        BODY))

    dlt_rows = [
        ["Table",       "Rows", "FK",        "Graph edge"],
        ["prospects",   "5",    "—",         "Root company node"],
        ["signals",     "14",   "company_id","Company → BuyingSignal"],
        ["tech_stack",  "13",   "company_id","Company → Technology"],
        ["contacts",    "7",    "company_id","Company → Person"],
        ["deal_outcomes","2",   "—",         "LessonLearned nodes (Stage 4)"],
    ]
    dlt_table = Table(dlt_rows, colWidths=[32*mm, 16*mm, 26*mm, 101*mm])
    dlt_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), BRAND_BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0), BRAND_WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [BRAND_LIGHT, BRAND_WHITE]),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#CBD5E1")),
    ]))
    story.append(dlt_table)
    story.append(Spacer(1, 4*mm))

    # Tech stack + judge talking points side by side
    stack_content = [
        Paragraph("TECH STACK", H2),
        Table([
            [Paragraph("<b>Cognee 1.1.0</b>", BODY), Paragraph("Knowledge graph engine", SMALL)],
            [Paragraph("<b>Redis (Docker)</b>", BODY), Paragraph("Real-time signal cache (HSET, TTL)", SMALL)],
            [Paragraph("<b>LanceDB</b>", BODY),        Paragraph("Vector index (embedded in Cognee)", SMALL)],
            [Paragraph("<b>dlt</b>", BODY),            Paragraph("Typed structured ingestion + FK edges", SMALL)],
            [Paragraph("<b>OpenAI</b>", BODY),         Paragraph("Entity extraction + embeddings", SMALL)],
            [Paragraph("<b>Python 3.10</b>", BODY),    Paragraph("asyncio, redis-py, python-dotenv", SMALL)],
        ], colWidths=[28*mm, 45*mm], style=TableStyle([
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("ROWBACKGROUNDS",(0,0), (-1,-1), [BRAND_LIGHT, BRAND_WHITE]),
        ])),
    ]

    judges_content = [
        Paragraph("KEY POINTS FOR JUDGES", H2),
        Paragraph(
            "<b>1. Not keyword search</b> — Cognee traverses graph relationships. "
            "BuildFast's CTO post about Cursor AI connects to AI literacy gap signal, "
            "which maps to ICP B winning pattern. Pure vector search misses this chain.",
            SMALL),
        Spacer(1, 2*mm),
        Paragraph(
            "<b>2. Redis is real</b> — we use Redis HSET explicitly for deal outcome "
            "caching. <font name='Courier' size=6.5>skillagents:signal:deal-001</font> "
            "is a live key with 24h TTL. Not just a tagline.",
            SMALL),
        Spacer(1, 2*mm),
        Paragraph(
            "<b>3. Self-evolving = closed loop</b> — Stage 4 proves it. The AFTER "
            "answer is measurably richer than BEFORE. The graph grew. Future SDRs "
            "benefit from deals they never worked.",
            SMALL),
        Spacer(1, 2*mm),
        Paragraph(
            "<b>4. dlt FK edges</b> — nested arrays become graph edges automatically. "
            "Structured memory, not just text chunks.",
            SMALL),
    ]

    bottom_table = Table(
        [[stack_content, judges_content]],
        colWidths=[80*mm, 95*mm],
    )
    bottom_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
    ]))
    story.append(bottom_table)
    story.append(Spacer(1, 4*mm))

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=BRAND_GRAY))
    story.append(Spacer(1, 2*mm))
    footer_data = [[
        Paragraph("SkillAgents AI &times; Cognee &times; Redis — Redis + Cognee Knowledge Graph Hackathon 2026",
                  S("Normal", fontSize=6.5, textColor=BRAND_GRAY)),
        Paragraph("Run: <font name='Courier' size=6.5>./demo.sh</font>  |  UI: http://localhost:3000",
                  S("Normal", fontSize=6.5, textColor=BRAND_GRAY, alignment=TA_RIGHT)),
    ]]
    footer_table = Table(footer_data, colWidths=[110*mm, 65*mm])
    footer_table.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    story.append(footer_table)

    doc.build(story)
    print(f"[✓] PDF written to: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "gtm_brain_overview.pdf")
    build_pdf(out)
