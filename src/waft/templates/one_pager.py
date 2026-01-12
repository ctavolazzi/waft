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
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 10.5pt;
            line-height: 1.6;
            color: #1a1a1a;
            margin: 0;
            padding: 0;
            background: #fff;
        }

        .header {
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 0.12in;
            margin-bottom: 0.2in;
            background: linear-gradient(to bottom, #f8f9fa 0%, #fff 100%);
            padding-top: 0.08in;
            padding-left: 0.05in;
            padding-right: 0.05in;
            margin-left: -0.05in;
            margin-right: -0.05in;
        }

        .title {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 20pt;
            font-weight: 700;
            margin: 0;
            padding: 0;
            color: #2c3e50;
            letter-spacing: -0.5pt;
            line-height: 1.2;
        }

        .subtitle {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 9pt;
            color: #5a6c7d;
            margin-top: 0.06in;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }

        .content {
            margin: 0;
            padding: 0;
        }

        h1 {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 16pt;
            font-weight: 700;
            margin: 0.2in 0 0.12in 0;
            page-break-after: avoid;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.06in;
            letter-spacing: -0.3pt;
        }

        h2 {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 13pt;
            font-weight: 600;
            margin: 0.18in 0 0.1in 0;
            page-break-after: avoid;
            color: #34495e;
            border-bottom: 1.5px solid #bdc3c7;
            padding-bottom: 0.04in;
            letter-spacing: -0.2pt;
        }

        h3 {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-size: 11.5pt;
            font-weight: 600;
            margin: 0.14in 0 0.08in 0;
            page-break-after: avoid;
            color: #34495e;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
            font-size: 10.5pt;
        }

        p {
            margin: 0.1in 0;
            text-align: justify;
            color: #34495e;
            line-height: 1.6;
        }

        ul, ol {
            margin: 0.12in 0;
            padding-left: 0.3in;
        }

        li {
            margin: 0.06in 0;
            line-height: 1.5;
            color: #34495e;
        }

        li::marker {
            color: #3498db;
        }

        dl {
            margin: 0.1in 0;
            border-left: 2px solid #ddd;
            padding-left: 0.15in;
        }

        dt {
            font-weight: bold;
            margin-top: 0.08in;
            margin-bottom: 0.03in;
            color: #333;
        }

        dt:first-child {
            margin-top: 0;
        }

        dd {
            margin-left: 0.25in;
            margin-bottom: 0.08in;
            padding-left: 0.05in;
        }

        pre {
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 8.5pt;
            background: #2c3e50;
            color: #ecf0f1;
            border-left: 4px solid #3498db;
            padding: 0.12in;
            margin: 0.12in 0;
            page-break-inside: avoid;
            overflow-x: auto;
            border-radius: 3px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        code {
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 9pt;
            background: #f1f3f5;
            color: #e74c3c;
            padding: 0.03in 0.05in;
            border-radius: 3px;
            border: 1px solid #dee2e6;
            font-weight: 500;
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

        .section {
            margin-bottom: 0.35in;
            page-break-inside: avoid;
            background: #f8f9fa;
            padding: 0.14in;
            border-left: 5px solid #3498db;
            border-top: 1px solid #e1e8ed;
            border-right: 1px solid #e1e8ed;
            border-bottom: 1px solid #e1e8ed;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            margin-left: -0.14in;
            margin-right: -0.14in;
            padding-left: 0.14in;
            padding-right: 0.14in;
        }

        .section h2 {
            margin-top: 0;
            margin-left: -0.14in;
            margin-right: -0.14in;
            padding-left: 0.14in;
            padding-right: 0.14in;
            padding-bottom: 0.08in;
            border-bottom: 2px solid #3498db;
            background: linear-gradient(to bottom, #ecf0f1 0%, #f8f9fa 100%);
            margin-bottom: 0.12in;
        }

        .section-content {
            margin-top: 0.12in;
        }

        .section-content p {
            margin: 0.08in 0;
            text-align: justify;
        }

        .section-content ul, .section-content ol {
            margin: 0.1in 0;
            padding-left: 0.3in;
        }

        .section-content li {
            margin: 0.06in 0;
            line-height: 1.5;
        }

        .section-content strong {
            font-weight: 600;
            color: #2c3e50;
        }

        .abstract {
            background: linear-gradient(to right, #e8f4f8 0%, #f0f8fb 100%);
            border-left: 4px solid #3498db;
            border-top: 1px solid #bdc3c7;
            border-right: 1px solid #bdc3c7;
            border-bottom: 1px solid #bdc3c7;
            padding: 0.14in;
            margin: 0.18in 0;
            border-radius: 3px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .abstract-title {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-weight: 700;
            font-size: 11.5pt;
            margin-bottom: 0.08in;
            color: #2c3e50;
            text-transform: uppercase;
            letter-spacing: 0.8pt;
        }

        .author-info {
            margin: 0.12in 0;
            font-size: 9pt;
            color: #5a6c7d;
            font-style: italic;
            border-top: 1px dotted #bdc3c7;
            padding-top: 0.08in;
            text-align: right;
        }

        .diagram {
            margin: 0.15in 0;
            text-align: center;
        }

        .diagram img {
            max-width: 100%;
            height: auto;
        }

        .figure-caption {
            font-size: 8pt;
            font-style: italic;
            margin-top: 0.05in;
        }

        blockquote {
            border-left: 4px solid #e74c3c;
            padding-left: 0.18in;
            margin: 0.15in 0;
            font-style: italic;
            color: #34495e;
            background: #fef5f5;
            padding: 0.12in;
            padding-left: 0.18in;
            border-radius: 2px;
            font-size: 10pt;
            line-height: 1.6;
        }

        blockquote cite {
            display: block;
            margin-top: 0.06in;
            font-size: 8.5pt;
            color: #7f8c8d;
            font-style: normal;
            text-align: right;
        }

        .pillar {
            background: linear-gradient(to right, #fff5f5 0%, #fff 100%);
            border: 2px solid #e74c3c;
            border-left: 5px solid #e74c3c;
            padding: 0.12in;
            margin: 0.15in 0;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(231,76,60,0.15);
        }

        .pillar-title {
            font-family: 'Helvetica Neue', 'Arial', sans-serif;
            font-weight: 700;
            font-size: 11.5pt;
            margin-bottom: 0.08in;
            color: #c0392b;
            text-transform: uppercase;
            letter-spacing: 0.8pt;
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
        {% if component_htmls %}
            {# Render all component types using their HTML output #}
            {% for component_html in component_htmls %}
                {{ component_html | safe }}
            {% endfor %}
        {% elif sections %}
            {# Fallback: render sections for backward compatibility #}
            {% for section in sections %}
            <section class="section">
                <h2>{{ section.title }}</h2>
                {% if section.subtitle %}
                <h3>{{ section.subtitle }}</h3>
                {% endif %}
                <div class="section-content">
                    {{ section.content | safe }}
                </div>
            </section>
            {% endfor %}
        {% else %}
            {{ content | safe }}
        {% endif %}
    </div>
</body>
</html>
"""
