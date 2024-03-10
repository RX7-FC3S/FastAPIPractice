from common.model import DataModelBase, Field
from sqlmodel import Relationship


class BinSpec(DataModelBase, table=True):
    bin_spec_name: str = Field()

    length: int = Field()
    width: int = Field()
    height: int = Field()

    weight_capacity: int = Field()
    volume_capacity: int = Field()

    pieces_capacity: int = Field()
    carton_capacity: int = Field()
    pallet_capacity: int = Field()

    bin_list: list["BinInfo"] = Relationship(back_populates="bin_spec")
