from common.model import DataModelBase, Field


class Stakeholder(DataModelBase, table=True):
    stakeholder_code: str = Field(nullable=False, max_length=16)
    stakeholder_name: str = Field(nullable=False, max_length=8)
    