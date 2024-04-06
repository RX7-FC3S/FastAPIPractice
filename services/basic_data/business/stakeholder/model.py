from common.model import DataModelBase, Field


class Stakeholder(DataModelBase, table=True):
    stakeholder_code: str = Field()
    stakeholder_name: str = Field()
    
    company: str
    contact: str
    phone: str
    email: str
    address: str
    country: str

    is_sender: bool
    is_receiver: bool