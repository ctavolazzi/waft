# analysis_orax.sty

LaTeX package for creating professional analysis reports with an orange-themed color scheme.

## Features

- **Orange Color Theme**: Consistent orange color scheme throughout the document
- **Custom Section Formatting**: Enhanced section, subsection, and subsubsection styling
- **Figure Enhancements**: Custom figure environments with orange-colored captions
- **Typography**: Professional typography settings optimized for analysis reports
- **Page Layout**: Sensible default page geometry
- **Header/Footer**: Styled headers and footers with orange accents

## Usage

```latex
\documentclass{article}
\usepackage{analysis_orax}

\begin{document}
\title{Analysis Report}
\author{Your Name}
\date{\today}
\maketitle

\section{Introduction}
Your content here.

\begin{figure}[htb]
    \centering
    \includegraphics[width=1\textwidth]{figures/figure1.png}
    \caption{Figure Description}
    \label{fig:1}
\end{figure}

\end{document}
```

## Custom Commands

### `\analysiscaption{text}`
Creates an orange-colored, bold caption for figures.

### `\analysisfigure[placement]{width}{path}{caption}`
Convenience command for creating styled figures:
```latex
\analysisfigure[htb]{1\textwidth}{figures/figure1.png}{Figure Description}
```

### `\highlight{text}`
Highlights text with an orange background.

### `\emphasize{text}`
Emphasizes text in orange color.

### `\analysissection{title}` and `\analysissubsection{title}`
Styled section commands (alternative to standard `\section` and `\subsection`).

## Color Definitions

- `analysisorange`: Primary orange (RGB: 255,153,0)
- `analysisdarkorange`: Darker orange for accents (RGB: 204,102,0)
- `analysislightorange`: Lighter orange for backgrounds (RGB: 255,204,102)
- `analysisgray`: Neutral gray for text (RGB: 128,128,128)

## Customization

You can override default settings:

```latex
% Custom geometry
\geometry{left=1.5in, right=1.5in}

% Custom graphics path
\graphicspath{{my_figures/}{other_images/}}
```

## Requirements

The package requires the following LaTeX packages (automatically loaded):
- xcolor
- graphicx
- caption
- titlesec
- geometry
- fancyhdr
- hyperref
- microtype

## Version

Version 1.0.0 (2026-01-16)

## License

Part of the WAFT Framework.
