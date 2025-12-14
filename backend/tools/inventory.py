from typing import Any, Dict
from faker import Faker
import faker_commerce
from langchain.tools import tool


fake = Faker()
fake.add_provider(faker_commerce.Provider)
