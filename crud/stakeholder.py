from common.crud import CRUDBase
from models.stakeholder import Stakeholder as ModelStakeholder


class CRUDStakeholder(CRUDBase[ModelStakeholder]):
    pass


Stakeholder = CRUDStakeholder(ModelStakeholder)
