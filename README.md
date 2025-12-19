# R-Simple Interpreter

A lightweight, web-based interpreter for a subset of the R programming language, built with Python (PLY) and Flask.

## Overview

This project implements a lexical analyzer, syntax analyzer, and interpreter for R-like syntax. It features a modern web interface where users can write, import, and execute scripts directly in the browser.

## Features

### Interpreter Capabilities

- **Variables & Assignments**: Supports `<-` and `=` assignment operators.
- **Data Types**: Integers, Floats, Strings, and Vectors (lists).
- **Arithmetic**: `+`, `-`, `*`, `/`.
- **Comparison**: `>`, `<`, `>=`, `<=`, `==`, `!=`.
- **Control Flow**:
  - `if` / `else` statements.
  - `while` loops.
  - `for` loops (iterating over vectors).
- **Built-in Functions**:
  - `print()`: Output values.
  - `c()`: Create vectors (combined list).
  - `cat()`: Concatenate and print.
  - `paste()`: Concatenate strings.

### Web Interface

- **Code Editor**: Syntax-ready textarea with line numbers.
- **Smart Editing**: Auto-closing for parentheses `()`, braces `{}`, and quotes `""`.
- **File Import**: Load local `.R` or `.txt` scripts directly into the editor (client-side only, no server upload).
- **Console Output**: R-style output display (e.g., `[1] value`).
- **Dark Mode**: Sleek, developer-friendly UI with the "Fira Code" font.

## Project Structure

```
.
├── app.py                  # Flask application entry point
├── requirements.txt        # Python dependencies
├── r_interpreter/          # Core interpreter package
│   ├── lexer.py            # Lexical Analyzer (Token definitions)
│   ├── parser.py           # Syntax Analyzer (Grammar rules)
│   └── interpreter.py      # Interpreter Logic (AST execution)
├── static/
│   └── style.css           # UI Styles
└── templates/
    └── index.html          # Frontend interface
```

## Installation & Usage

1.  **Prerequisites**: Python 3.x installed.

2.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:

    ```bash
    python3 app.py
    ```

4.  **Access the Interface**:
    Open your web browser and navigate to `http://localhost:8000`.

## Example Script

Try running this code in the editor:

```r
# Calculate Factorial
n <- 5
fact <- 1

while (n > 0) {
    fact <- fact * n
    n <- n - 1
}

cat("Factorial of 5 is:", fact)
```

## License

This project is created for educational purposes.
