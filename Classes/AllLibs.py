from typing import List
from typing import Any
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    server_id: str
    id: str
    channel_id: str
    is_folder: str
    type: str
    collection_type: str
    location_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        _Name = str(obj.get("Name"))
        _ServerId = str(obj.get("ServerId"))
        _Id = str(obj.get("Id"))
        _ChannelId = str(obj.get("ChannelId"))
        _IsFolder = str(obj.get("IsFolder"))
        _Type = str(obj.get("Type"))
        _CollectionType = str(obj.get("CollectionType"))
        _LocationType = str(obj.get("LocationType"))
        return Item(_Name, _ServerId, _Id, _ChannelId, _IsFolder, _Type, _CollectionType, _LocationType)

@dataclass
class AllLibs:
    Items: List[Item]
    TotalRecordCount: int
    StartIndex: int

    @staticmethod
    def from_dict(obj: Any) -> 'AllLibs':
        _Items = [Item.from_dict(y) for y in obj.get("Items")]
        _TotalRecordCount = int(obj.get("TotalRecordCount"))
        _StartIndex = int(obj.get("StartIndex"))
        return AllLibs(_Items, _TotalRecordCount, _StartIndex)
