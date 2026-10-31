from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def build_history_pdf(chat_title: str, rows) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    y = h - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, f"Tarix: {chat_title}")
    y -= 30
    c.setFont("Helvetica", 10)
    for r in rows:
        line = f"[{r['created_at']}] {r['kind']} | {r['keyword'] or '-'}"
        c.drawString(40, y, line[:110])
        y -= 16
        if y < 50:
            c.showPage(); c.setFont("Helvetica", 10); y = h - 50
    c.save()
    return buf.getvalue()