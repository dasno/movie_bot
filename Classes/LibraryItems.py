from typing import List
from typing import Any
from dataclasses import dataclass

@dataclass
class UserData:
    PlaybackPositionTicks: str
    PlayCount: str
    IsFavorite: str
    Played: str
    Key: str

    @staticmethod
    def from_dict(obj: Any) -> 'UserData':
        _PlaybackPositionTicks = str(obj.get("PlaybackPositionTicks"))
        _PlayCount = str(obj.get("PlayCount"))
        _IsFavorite = str(obj.get("IsFavorite"))
        _Played = str(obj.get("Played"))
        _Key = str(obj.get("Key"))
        return UserData(_PlaybackPositionTicks, _PlayCount, _IsFavorite, _Played, _Key)

@dataclass
class Item:
    Name: str
    ServerId: str
    Id: str
    HasSubtitles: str
    Container: str
    PremiereDate: str
    CriticRating: str
    OfficialRating: str
    ChannelId: str
    CommunityRating: str
    RunTimeTicks: str
    ProductionYear: str
    IsFolder: str
    Type: str
    UserData: UserData
    VideoType: str
    LocationType: str
    MediaType: str

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        _Name = str(obj.get("Name"))
        _ServerId = str(obj.get("ServerId"))
        _Id = str(obj.get("Id"))
        _HasSubtitles = str(obj.get("HasSubtitles"))
        _Container = str(obj.get("Container"))
        _PremiereDate = str(obj.get("PremiereDate"))
        _CriticRating = str(obj.get("CriticRating"))
        _OfficialRating = str(obj.get("OfficialRating"))
        _ChannelId = str(obj.get("ChannelId"))
        _CommunityRating = str(obj.get("CommunityRating"))
        _RunTimeTicks = str(obj.get("RunTimeTicks"))
        _ProductionYear = str(obj.get("ProductionYear"))
        _IsFolder = str(obj.get("IsFolder"))
        _Type = str(obj.get("Type"))
        _UserData = UserData.from_dict(obj.get("UserData"))
        _VideoType = str(obj.get("VideoType"))
        _LocationType = str(obj.get("LocationType"))
        _MediaType = str(obj.get("MediaType"))
        return Item(_Name, _ServerId, _Id, _HasSubtitles, _Container, _PremiereDate, _CriticRating, _OfficialRating, _ChannelId, _CommunityRating, _RunTimeTicks, _ProductionYear, _IsFolder, _Type, _UserData, _VideoType, _LocationType, _MediaType)


@dataclass
class LibraryItems:
    Items: List[Item]

    @staticmethod
    def from_dict(obj: Any) -> 'LibraryItems':
        _Items = [Item.from_dict(y) for y in obj.get("Items")]
        return LibraryItems(_Items)



# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
