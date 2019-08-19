from dataclasses import dataclass, field
from typing import List


@dataclass
class Channel:
    """
    Helper class for storing OH things
    """

    type: str = ''
    channel: str = ''
    name: str = ''
    ga: str = ''


    def __str__(self):
        return (
        f'Channel [{self.name}]\n\n'
        f'  type            :\t{self.type}\n'
        f'  name            :\t{self.name}\n'
        f'  channel         :\t{self.channel}\n'
        f'  ga              :\t{self.ga}\n'
        )

    def __eq__(self, other):
        return self.name == other.name and self.ga == other.ga

    def get_item_attributes(self):
        return (self.type, self.name, self.channel, self.ga)

@dataclass
class Device:
    """
    Helper class to store OH things
    """
    all_items = []

    name: str = ''
    channels: List[Channel] = field(default_factory=list)

    def __str__(self):
        return (
        f'Openhab Device\n\n'
        f'  name            :\t{self.name}\n'
        f'  -----------------------channels-----------------------------\n{self.get_channels()}\n'
        )

    def __post_init__(self):
        Device.add(self)

    @classmethod
    def add(cls, self):
        '''Add item to list of all items.
        '''
        search = list(filter(lambda x: self == x, cls.all_items))
        if len(search) == 0:
            cls.all_items.append(self)
        else:
            print("ERROR: The following address is assigned twice in your item files:")

    def add_channel(self, type, name, channel, ga):
        self.channels.append(Channel(type=type, name=name, channel=channel, ga=ga))

    def get_channels(self):
        return "\n".join([str(channel) for channel in self.channels])

    def get_channels_list(self):
        # return [channel for channel in self.channels]
        return self.channels

    @classmethod
    def items(cls):
        return cls.all_items