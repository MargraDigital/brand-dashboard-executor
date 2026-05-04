import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate(output_path, data):
    w, h = landscape(A4)
    c = canvas.Canvas(output_path, pagesize=landscape(A4))

    navy = colors.HexColor('#1E2E45')
    teal = colors.HexColor('#0F6E56')
    bg = colors.HexColor('#F4F3EF')
    white = colors.white

    # Background
    c.setFillColor(bg)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Header
    c.setFillColor(navy)
    c.rect(0, h-70, w, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 20)
    c.drawString(30, h-45, 'Personal Brand Dashboard')
    c.setFont('Helvetica', 12)
    c.drawString(30, h-62, data.get('week', ''))

    # Metric cards
    metrics = [
        ('Name Searches', data.get('name_searches', '-')),
        ('Sessions', data.get('sessions', '-')),
        ('Open Rate %', data.get('open_rate', '-')),
        ('SoLV %', data.get('solv', '-')),
    ]

    card_w = (w - 60) / 4
    card_h = 120
    card_y = h - 220

    for i, (title, value) in enumerate(metrics):
        x = 30 + i * (card_w + 10)
        c.setFillColor(white)
        c.roundRect(x, card_y, card_w - 10, card_h, 8, fill=1, stroke=0)
        c.setFillColor(teal)
        c.setFont('Helvetica-Bold', 24)
        c.drawCentredString(x + (card_w-10)/2, card_y + 55, str(value))
        c.setFillColor(navy)
        c.setFont('Helvetica', 11)
        c.drawCentredString(x + (card_w-10)/2, card_y + 30, title)

    # Signals
    signals = [
        ('Name Search Trend', data.get('signal_name', '-')),
        ('Newsletter Opens', data.get('signal_opens', '-')),
        ('GBP Ranking', data.get('signal_gbp', '-')),
        ('Web Traffic', data.get('signal_traffic', '-')),
    ]

    sig_y = card_y - 100
    c.setFillColor(navy)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(30, sig_y + 70, 'Signals')

    sig_w = (w - 60) / 4
    for i, (title, value) in enumerate(signals):
        x = 30 + i * (sig_w + 10)
        # Colour code signal
        if value == 'Growing' or value == 'Strong' or value == 'Improving' or value == 'Above avg':
            badge_color = teal
        elif value == 'Declining' or value == 'Dropping' or value == 'Below avg':
            badge_color = colors.HexColor('#C0392B')
        else:
            badge_color = colors.HexColor('#888888')

        c.setFillColor(badge_color)
        c.roundRect(x, sig_y, sig_w - 10, 55, 6, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(x + (sig_w-10)/2, sig_y + 28, str(value))
        c.setFont('Helvetica', 10)
        c.drawCentredString(x + (sig_w-10)/2, sig_y + 12, title)

    c.save()

if __name__ == '__main__':
    data = {
        'week': os.environ.get('WEEK', ''),
        'name_searches': os.environ.get('NAME_SEARCHES', '-'),
        'sessions': os.environ.get('SESSIONS', '-'),
        'open_rate': os.environ.get('OPEN_RATE', '-'),
        'solv': os.environ.get('SOLV', '-'),
        'signal_name': os.environ.get('SIGNAL_NAME', '-'),
        'signal_opens': os.environ.get('SIGNAL_OPENS', '-'),
        'signal_gbp': os.environ.get('SIGNAL_GBP', '-'),
        'signal_traffic': os.environ.get('SIGNAL_TRAFFIC', '-'),
    }
    out = os.environ.get('PDF_OUTPUT', 'dashboard.pdf')
    generate(out, data)
