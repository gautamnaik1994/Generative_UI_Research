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
Usage: Top-level container for the entire UI.
{
  "type": "root",
  "children": [ ...components ]
}

### Container
Usage: Group related components together.
{
  "type": "container",
  "variant": "vertical" | "horizontal",
  "children": [ ...components ]
}

### Text Component (Supports Nested Inline Formatting)
Usage: Display textual content. Use 'span' variants for inline formatting inside other text.
{
  "type": "text",
  "variant": "header" | "subheader" | "paragraph" | "span" | "span-bold" | "span-italic" | "span-underline",
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
Usage: Visualize data. Choose correct x_axis and y_axis from provided data.
{
  "type": "chart",
  "variant": "line" | "bar",
  "x_axis": "string",
  "y_axis": "string",
  "title": "string",
  "dataKey": "chart_data_key"
}

### Data Table
Usage: Display tabular data. Use 'dataKey' for large datasets
{
  "type": "data-table",
  "title": "string",
  "dataKey": "table_data_key", //A key referencing the dataset returned by a tool
}

### Embed Table
Usage: Display small/static tabular data inline
{
  "type": "embed-table",
  "title": "string",
  "columns": [
    {
      "header": "string",
      "key": "string"
    }, ...
  ],
  "rows": [
    { "column_key": "value", ... }, ...
  ]
}


### Card
Usage: Present concise information.
{
  "type": "card",
  "title": "string",
  "content": "string"
}

### Button
Usage: Trigger an action or event.
{
  "type": "button",
  "label": "string",
  "action": "string"
}

### Image
Usage: Display visual content.
{
  "type": "image",
  "src": "image_url",
  "alt": "string"
}

### List
Usage: Display a collection of items.
{
  "type": "list",
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
- Use `data-table` ONLY when the dataset is referenced using a `dataKey`.
- Use `embed-table` ONLY when the tabular data is provided inline as arrays (`columns` and `rows`).
- NEVER mix fields between these two table types.
- A `data-table` MUST NOT contain `columns` or `rows`.
- An `embed-table` MUST NOT contain `dataKey`.

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
