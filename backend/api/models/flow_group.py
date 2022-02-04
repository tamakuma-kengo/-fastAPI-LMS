
# フローグループ(フローの構成要素)を示すテーブル群
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from api.db import Base

# フローグループ情報
class FlowGroup(Base):
    __tablename__ = "flowgroups"

    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False)
    order = Column(Integer, nullable=False, comment="フロー内の表示順序. 値が小さいものから順に表示される. 同じフロー内で一意")
    shuffle = Column(Boolean, default=False, comment="表示時にフローグループ内でシャッフルを行うか否か.")
    num_of_show = Column(Integer, comment="表示にフローグループ内で何問出題するか. shuffle=Trueのときに有効. NULLの際にはすべて出題する.")

# フローとフローグループの対応情報
class FlowGroupFlowPages(Base):
    __tablename__ = "flowgroup_flow_pages"

    flowgroup_id = Column(Integer, ForeignKey("flowgroups.id"), primary_key= True)
    flowpage_id = Column(Integer, ForeignKey("flowpages.id"), primary_key= True)

    flow_group = relationship("FlowGroup")
    flowpage = relationship("FlowPage")
