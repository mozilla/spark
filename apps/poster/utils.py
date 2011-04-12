import cStringIO as StringIO
import ho.pisa as pisa

from django.http import HttpResponse

from cgi import escape

import jingo


def render_to_pdf(request, template, data):
    html  = jingo.render(request, template, data)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.content), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html.content))