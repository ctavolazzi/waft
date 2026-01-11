"""
One-Pager Template
==================

Simple, clean template for 2-page one-pagers.
Content starts immediately on page 1.
"""

ONE_PAGER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.5in;
        }

        @page :first {
            margin: 0.5in;
        }

        body {
            font-family: Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #000;
            margin: 0;
            padding: 0;
        }

        .header {
            border-bottom: 2px solid #000;
            padding-bottom: 0.1in;
            margin-bottom: 0.15in;
        }

        .title {
            font-size: 18pt;
            font-weight: bold;
            margin: 0;
            padding: 0;
        }

        .subtitle {
            font-size: 9pt;
            color: #666;
            margin-top: 0.05in;
        }

        .content {
            margin: 0;
            padding: 0;
        }

        h1 {
            font-size: 14pt;
            font-weight: bold;
            margin: 0.15in 0 0.1in 0;
            page-break-after: avoid;
        }

        h2 {
            font-size: 12pt;
            font-weight: bold;
            margin: 0.12in 0 0.08in 0;
            page-break-after: avoid;
        }

        h3 {
            font-size: 11pt;
            font-weight: bold;
            margin: 0.1in 0 0.06in 0;
            page-break-after: avoid;
        }

        p {
            margin: 0.08in 0;
            text-align: justify;
        }

        ul, ol {
            margin: 0.1in 0;
            padding-left: 0.25in;
        }

        li {
            margin: 0.05in 0;
        }

        pre {
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 0.1in;
            margin: 0.1in 0;
            page-break-inside: avoid;
            overflow-x: auto;
        }

        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f0f0f0;
            padding: 0.02in 0.04in;
        }

        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 0.15in 0;
        }

        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">{{ title }}</div>
        {% if subtitle %}
        <div class="subtitle">{{ subtitle }}</div>
        {% endif %}
    </div>

    <div class="content">
        {{ content | safe }}
    </div>
</body>
</html>
"""
