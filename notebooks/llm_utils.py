from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
import pickle
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from pydantic import RootModel
from pydantic import BaseModel
from typing import Any, Dict
import faker
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, JsonValue
import functools
from langchain.tools import tool
import yfinance as yf
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import os
load_dotenv()


load_dotenv()


ui_generation_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aibe.mygreatlearning.com/openai/v1",
    model='gpt-4o',
    temperature=0,
    streaming=True
)


# --- Base and Auxiliary Models ---


class BaseComponent(BaseModel):
    # This must be defined as str first, and then overridden by Literals in subclasses
    type: str
    # usage: Optional[str] = None

    model_config = {
        "extra": "forbid"
    }


class TableCell(BaseModel):
    key: str
    # Note: Using `str | int | float | bool | None` is the modern Pydantic/Python way
    value: str | int | float | bool | None


class TableRow(BaseModel):
    cells: List[TableCell]

# --- Component Definitions (Uses string literal "Component" for recursion) ---


class Container(BaseComponent):
    type: Literal["container"]
    variant: Literal["vertical", "horizontal"]
    children: List["Component"]


class Text(BaseComponent):
    type: Literal["text"]
    variant: Literal["header", "subheader", "paragraph"]
    value: str


class Chart(BaseComponent):
    type: Literal["chart"]
    variant: Literal["line", "bar"]
    x_axis: str
    y_axis: str
    title: str
    dataKey: str


class Table(BaseComponent):
    type: Literal["table"]
    title: str
    # columns: List[str]
    # rows: List[TableRow]
    dataKey: str


class Card(BaseComponent):
    type: Literal["card"]
    title: str
    content: str


class Button(BaseComponent):
    type: Literal["button"]
    label: str
    action: str


class Image(BaseComponent):
    type: Literal["image"]
    src: str
    alt: str


class ListComponent(BaseComponent):
    type: Literal["list"]
    children: List["Component"]


class Root(BaseComponent):
    type: Literal["root"]
    children: List["Component"]

# --- Component Union Definition ---


# Define the Union using the model classes
Component = Union[
    Root,
    Container,
    Text,
    Chart,
    Table,
    Card,
    Button,
    Image,
    ListComponent,
]

# --- Resolve Forward References ---

# The rebuild calls are ESSENTIAL to link the string "Component"
# to the actual Component Union type.
Root.model_rebuild()
Container.model_rebuild()
# Card.model_rebuild()
ListComponent.model_rebuild()

# --- Final Output Schema ---


class UISpec(BaseModel):
    root: Root

    model_config = {
        "extra": "forbid"
    }


basic_ui_spec = """
{
    "type": "root",
    "usage": "Use 'root' as the top-level container for the entire UI.",
    "children": [ ...components ]
},
{
  "type": "container",
  "usage": "Use 'container' to group related components together.",
  "variant": "vertical" | "horizontal",
  "children": [ ...components ]
},
{
  "type": "text",
  "variant": "header" | "subheader" | "paragraph",
  "usage": "Use 'text' to display static text content.",
  "value": "string"
},
{
  "type": "chart",
  "usage": "Use 'chart' to visualize data in different formats. Choose the column names for x_axis and y_axis based on the data provided.",
  "variant": "line" | "bar",
  "x_axis": "string",
  "y_axis": "string",
  "title": "string",
  "dataKey": "chart_data_key"
},
{
  "type": "table",
  "usage": "Use 'table' to display tabular data. Depending on the data, you can have different columns and rows.",
  "title": "string",
  "dataKey": "table_stock_data"
},
{
  "type": "card",
  "usage": "Use 'card' to present information in a concise format.",
  "title": "string",
  "content": "string"
},
{
  "type": "button",
  "usage": "Use 'button' to trigger actions or events.",
  "label": "string",
  "action": "string"
},
{
  "type": "image",
  "usage": "Use 'image' to display visual content.",
  "src": "image_url",
  "alt": "string"
},
{
  "type": "list",
  "usage": "Use 'list' to display a collection of items.",
  "children": [ ...components ]
}
"""

ui_generation_system_message = f"""
You are a highly specialized **UI Generation Agent** designed to create high-fidelity UI specifications. Your primary task is to translate user requirements and provided JSON data into a structured, executable UI definition.

**Core Instruction:** Generate a single, comprehensive JSON object that represents the complete UI specification.

### Component Library & Structure Rules

Use only the following components and determine when to use each based on the component 'usage' description provided below:
{basic_ui_spec}

### Output Principles

1.  **Structure:** The final JSON object **MUST** strictly adhere to the defined Pydantic schema (the `UISpec` model). The top-level key must be `root`. And output MUST be compacted, containing no extraneous whitespace, newlines, or indentation.
2.  **Data Integration:** When data is required for a `chart` or `table`, utilize the `dataKey` field to specify the required data set. Do **NOT** invent row/cell data in the output unless it is for static examples.
3.  **Hierarchy:** Components must be organized logically within nested `container` and `root` elements to enhance clarity and visual grouping.
4.  **Actionability:** Every `button` must have an explicit, clear `label` that indicates its purpose.
"""

structured_ui_gen_llm = ui_generation_llm.with_structured_output(
    UISpec, method="function_calling")


messages = [{'role': 'system',
             'content': '\nYou are a highly specialized **UI Generation Agent** designed to create high-fidelity UI specifications. Your primary task is to translate user requirements and provided JSON data into a structured, executable UI definition.\n\n**Core Instruction:** Generate a single, comprehensive JSON object that represents the complete UI specification.\n\n### Component Library & Structure Rules\n\nUse only the following components and determine when to use each based on the component \'usage\' description provided below:\n\n{\n    "type": "root",\n    "usage": "Use \'root\' as the top-level container for the entire UI.",\n    "children": [ ...components ]\n},\n{\n  "type": "container",\n  "usage": "Use \'container\' to group related components together.",\n  "variant": "vertical" | "horizontal",\n  "children": [ ...components ]\n},\n{\n  "type": "text",\n  "variant": "header" | "subheader" | "paragraph",\n  "usage": "Use \'text\' to display static text content.",\n  "value": "string"\n},\n{\n  "type": "chart",\n  "usage": "Use \'chart\' to visualize data in different formats. Choose the column names for x_axis and y_axis based on the data provided.",\n  "variant": "line" | "bar",\n  "x_axis": "string",\n  "y_axis": "string",\n  "title": "string",\n  "dataKey": "chart_data_key"\n},\n{\n  "type": "table",\n  "usage": "Use \'table\' to display tabular data. Depending on the data, you can have different columns and rows.",\n  "title": "string",\n  "dataKey": "table_stock_data"\n},\n{\n  "type": "card",\n  "usage": "Use \'card\' to present information in a concise format.",\n  "title": "string",\n  "content": "string"\n},\n{\n  "type": "button",\n  "usage": "Use \'button\' to trigger actions or events.",\n  "label": "string",\n  "action": "string"\n},\n{\n  "type": "image",\n  "usage": "Use \'image\' to display visual content.",\n  "src": "image_url",\n  "alt": "string"\n},\n{\n  "type": "list",\n  "usage": "Use \'list\' to display a collection of items.",\n  "children": [ ...components ]\n}\n\n\n### Output Principles\n\n1.  **Structure:** The final JSON object **MUST** strictly adhere to the defined Pydantic schema (the `UISpec` model). The top-level key must be `root`. And output MUST be compacted, containing no extraneous whitespace, newlines, or indentation.\n2.  **Data Integration:** When data is required for a `chart` or `table`, utilize the `dataKey` field to specify the required data set. Do **NOT** invent row/cell data in the output unless it is for static examples.\n3.  **Hierarchy:** Components must be organized logically within nested `container` and `root` elements to enhance clarity and visual grouping.\n4.  **Actionability:** Every `button` must have an explicit, clear `label` that indicates its purpose.\n'},
            {'role': 'user',
             'content': 'Generate a UI specification for the following data:\n  [{"task_description": "Show the list of all products available in the store", "tool_name": "get_products", "args": {}, "tool_result": [{"name": "Phone", "price": 8, "description": "Alone art class size pull where improve drive change seem without leg against.", "image_url": "https://dummyimage.com/340x520"}, {"name": "Consumer", "price": 52, "description": "Rather various reach above type bit southern.", "image_url": "https://placekitten.com/653/601"}, {"name": "Everything", "price": 5, "description": "Drop product industry hundred system example couple attack.", "image_url": "https://placekitten.com/965/461"}, {"name": "Stage", "price": 1, "description": "Dinner investment seem probably call marriage gas first program stop act.", "image_url": "https://placekitten.com/227/383"}, {"name": "Matter", "price": 24, "description": "Build economic future prove they pass couple seem avoid final.", "image_url": "https://dummyimage.com/221x23"}, {"name": "Second", "price": 54, "description": "Southern great magazine marriage church throughout end I somebody.", "image_url": "https://picsum.photos/910/85"}, {"name": "Than", "price": 67, "description": "At paper build card including cover you talk.", "image_url": "https://placekitten.com/133/212"}, {"name": "Better", "price": 29, "description": "Soon off special factor organization current power little something available information case individual.", "image_url": "https://picsum.photos/964/1019"}, {"name": "About", "price": 47, "description": "Laugh participant worker American character public section book law pressure read drop.", "image_url": "https://picsum.photos/880/385"}, {"name": "From", "price": 98, "description": "Truth hospital season five show store management now trial some.", "image_url": "https://picsum.photos/629/485"}]}, {"task_description": "Provide details of the top 5 products based on customer ratings", "tool_name": "get_top_n_selling_products", "args": {"n": 5}, "tool_result": [{"name": "Particularly", "price": 68, "description": "Prove social put born want sort.", "image_url": "https://picsum.photos/29/503", "units_sold": 703}, {"name": "Environmental", "price": 62, "description": "Per professor food agency young treatment.", "image_url": "https://dummyimage.com/632x352", "units_sold": 495}, {"name": "Campaign", "price": 95, "description": "Peace training bring condition glass office leader center mission member everyone season bank.", "image_url": "https://dummyimage.com/538x310", "units_sold": 400}, {"name": "Skin", "price": 40, "description": "Receive sister generation because thank college dark.", "image_url": "https://picsum.photos/380/377", "units_sold": 319}, {"name": "Exist", "price": 56, "description": "Throw develop show fire recognize pick capital cause everyone hand.", "image_url": "https://placekitten.com/973/464", "units_sold": 60}]}]'}]
