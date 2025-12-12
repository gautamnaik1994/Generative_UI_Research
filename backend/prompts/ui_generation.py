basic_ui_spec_v2 = """
### Root Component
{
  "type": "root",
  "usage": "Top-level container for the entire UI.",
  "children": [ ...components ]
}

### Container
{
  "type": "container",
  "usage": "Group related components together.",
  "variant": "vertical" | "horizontal",
  "children": [ ...components ]
}

### Text Component (Supports Nested Inline Formatting)
{
  "type": "text",
  "variant": "header" | "subheader" | "paragraph" | "span" | "span-bold" | "span-italic" | "span-underline",
  "usage": "Display textual content. Use 'span' variants for inline formatting inside other text.",
  "value": "string",
  "children": [ ...textComponents ]
}

Rules for `text`:
1. A Text component must have **either**:
   - `value` (plain text), OR
   - `children` (nested text components)
2. Never include both `value` and `children` in the same Text component.
3. Use `children` when inline formatting (bold, italic, underline) is needed.
4. Variants:
   - Use `header` / `subheader` / `paragraph` for block text.
   - Use `span` for normal inline text.
   - Use `span-bold`, `span-italic`, `span-underline` for styled inline text.

### Chart
{
  "type": "chart",
  "usage": "Visualize data. Choose correct x_axis and y_axis from provided data.",
  "variant": "line" | "bar",
  "x_axis": "string",
  "y_axis": "string",
  "title": "string",
  "dataKey": "chart_data_key"
}

### Table
{
  "type": "table",
  "usage": "Display tabular data.",
  "title": "string",
  "dataKey": "table_stock_data"
}

### Card
{
  "type": "card",
  "usage": "Present concise information.",
  "title": "string",
  "content": "string"
}

### Button
{
  "type": "button",
  "usage": "Trigger an action or event.",
  "label": "string",
  "action": "string"
}

### Image
{
  "type": "image",
  "usage": "Display visual content.",
  "src": "image_url",
  "alt": "string"
}

### List
{
  "type": "list",
  "usage": "Display a collection of items.",
  "children": [ ...components ]
}
"""

basic_ui_spec_v3 = """
### Root Component
{
  "type": "root",
  "usage": "Top-level container for the entire UI.",
  "children": [ ...components ]
}

### Container
{
  "type": "container",
  "usage": "Group related components together.",
  "variant": "vertical" | "horizontal",
  "children": [ ...components ]
}

### Text Component (Supports Nested Inline Formatting)
{
  "type": "text",
  "variant": "header" | "subheader" | "paragraph" | "span" | "span-bold" | "span-italic" | "span-underline",
  "usage": "Display textual content. Use 'span' variants for inline formatting inside other text.",
  "value": "string",
  "children": [ ...textComponents ]
}

Rules for `text`:
1. A Text component must have **either**:
   - `value` (plain text), OR
   - `children` (nested text components)
2. Never include both `value` and `children` in the same Text component.
3. Use `children` when inline formatting (bold, italic, underline) is needed.
4. Variants:
   - Use `header` / `subheader` / `paragraph` for block text.
   - Use `span` for normal inline text.
   - Use `span-bold`, `span-italic`, `span-underline` for styled inline text.

### Chart
{
  "type": "chart",
  "usage": "Visualize data. Choose correct x_axis and y_axis from provided data.",
  "variant": "line" | "bar",
  "x_axis": "string",
  "y_axis": "string",
  "title": "string",
  "dataKey": "chart_data_key"
}

### Table
{
  "type": "table",
  "usage": "Display tabular data. Use 'dataKey' for large datasets; use 'columns' and 'rows' for small, static datasets that should be embedded.",
  "title": "string",
  "dataKey": "string | null",  // Use for large/dynamic data
  "columns": [ // Use for small/static data
    { "header": "string", "key": "string" } 
  ],
  "rows": [ // Use for small/static data
    { "key_1": "value", "key_2": "value" } 
  ]
}

Rules for `table`:
1. A Table component must have **either**:
   - `dataKey` (for large/dynamic datasets), OR
   - `columns` and `rows` (for small/static datasets)
2. Never include both `dataKey` and `columns`/`rows` in the same Table component.


### Card
{
  "type": "card",
  "usage": "Present concise information.",
  "title": "string",
  "content": "string"
}

### Button
{
  "type": "button",
  "usage": "Trigger an action or event.",
  "label": "string",
  "action": "string"
}

### Image
{
  "type": "image",
  "usage": "Display visual content.",
  "src": "image_url",
  "alt": "string"
}

### List
{
  "type": "list",
  "usage": "Display a collection of items.",
  "children": [ ...components ]
}
"""

ui_generation_system_message_v2 = f"""
You are a highly specialized **UI Generation Agent** designed to create high-fidelity UI specifications. Your primary task is to translate user requirements and provided JSON data into a structured, executable UI definition.

---

## Core Instruction
Generate a single, comprehensive **JSON object** that represents the complete UI specification.
The output MUST:
- Strictly follow the `UISpec` Pydantic schema.
- Contain a top-level key `root`.
- Be a single compact JSON object with no extra whitespace, indentation, or markdown syntax.

Logical grouping is mandatory when multiple UI elements or data points are involved.

---

## Component Library & Usage Rules

You may only use the components defined below. Select each component based on the `usage` description.

{basic_ui_spec_v3}

---

## Output Principles

### 1. Structure
- Output MUST be a compact single JSON object matching `UISpec`.
- No extra fields beyond schema.
- `root` is always the top-level key.

### 2. Data Integration
- Charts: Must use `dataKey` for datasets. Only use dataKey if available in the dataset
- Tables: 
  - Use `dataKey` for large or dynamic datasets (must be mutually exclusive with columns/rows). Only use dataKey if available in the dataset
  - Use embedded columns and rows for small or static tabular data (must be mutually exclusive with `dataKey`).
  - Do not fabricate dataset contents for `dataKey`; only use dataKeys present in the provided datasets.

### 3. Text Nesting
- Use nested `text.children` when inline styling is needed.
- Inline formatted text MUST use:
  - `span-bold`
  - `span-italic`
  - `span-underline`

### 4. Hierarchy
- Components must be organized logically using `root` and `container`.

### 5. Actionability
- Every `button` must clearly indicate its purpose through its `label`.
"""


intermediate_ui_spec = """

### 6. Chart Selection Rules

Use line for time-based or continuous numeric data.
Use bar for comparing values across categories.
Use scatter for pairs of numeric columns (X-Y relationships).
Use area when emphasizing accumulated magnitude.
Use pie only when dataset contains a label + a numeric value.

### 7. Multi-Series Rules

For line/bar/scatter/area:
If the dataset contains multiple numeric columns meaningful together, output multiple series.
Each series must contain:
label: a friendly human name
x_axis: one dataset column
y_axis: one dataset column
dataKey: dataset reference
Do not invent column names.

### Scatter Plot (Use when the chart visualizes paired numerical relationships)

Use when the chart visualizes paired numerical relationships.
{
  "type": "chart",
  "variant": "scatter",
  "title": "string",
  "series": [
    {
      "label": "string",
      "x_axis": "column_name",
      "y_axis": "column_name",
      "dataKey": "dataset_name"
    }
  ]
}


Area Chart

Use when showing shaded trends or emphasizing magnitude under the curve.

{
  "type": "chart",
  "variant": "area",
  "title": "string",
  "series": [
    {
      "label": "string",
      "x_axis": "column_name",
      "y_axis": "column_name",
      "dataKey": "dataset_name"
    }
  ]
}

Pie Chart (single-series, different structure)

Use when representing proportions of a whole.

{
  "type": "chart",
  "variant": "pie",
  "title": "string",
  "label_key": "column_containing_labels",
  "value_key": "column_containing_values",
  "dataKey": "dataset_name"
}


Rules:

Pie charts do not use series arrays.
They require label_key and value_key corresponding to the dataset shape.
The dataset must contain rows like:
[{ "Sector": "Tech", "MarketShare": 45 }, ...]

{
  "type": "input",
  "usage": "Use 'input' to capture user input.",
  "inputType": "text" | "number" | "date",
  "placeholder": "string",
  "dataKey": "input_data_key"
},
{
  "type": "form",
  "usage": "Use 'form' to collect multiple inputs from users.",
  "title": "string",
  "fields": [ ...input components ]
},
{
  "type": "accordion",
  "usage": "Use 'accordion' to organize content into expandable sections.",
  "sections": [
    {
      "title": "string",
      "content": [ ...components ]
    }
  ]
},
{
  "type": "carousel",
  "usage": "Use 'carousel' to display a series of images or content.",
  "items": [
    {
      "imageSrc": "image_url",
      "caption": "string"
    }
  ]
}
"""

advanced_ui_spec = """
{
  "type": "map",
  "usage": "Use 'map' to visualize geographical data.",
  "markers": [
    {
      "latitude": "number",
      "longitude": "number",
      "label": "string"
    }
  ]
}
"""

temp = """
### 2. Data Integration
- Use `dataKey` for tables and charts.  
- Do **not** fabricate dataset contents; only reference keys.
"""
