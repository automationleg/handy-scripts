from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class KnxItem:
    """
    Helper class for storing OH knx1 items
    """
    all_items = []

    line: str = ''
    type: str = ''
    name: str = ''
    description: str = ''
    icon: str = ''
    groups: str = ''
    ga: str = ''


    def __str__(self):
        return (
        f'Openhab KNX1 item\n\n'
        f'  type            :\t{self.type}\n'
        f'  name            :\t{self.name}\n'
        f'  description     :\t{self.description}\n'
        f'  icon            :\t{self.icon}\n'
        f'  groups          :\t{self.groups}\n'
        f'  knx addresses   :\t{self.ga}\n'
        )

    def __eq__(self, other):
        return self.ga == other.ga and self.name == other.name

    def __post_init__(self):
        self.parse_knx_itemline()
        KnxItem.add(self)

    @classmethod
    def add(cls, self):
        '''Add item to list of all items.
        '''
        search = list(filter(lambda x: self == x, cls.all_items))
        if len(search) == 0:
            cls.all_items.append(self)
        else:
            print("ERROR: The following address is assigned twice in your item files:")
            print(duplicate)
            print(self)
            sys.exit(1)
    
    @classmethod
    def find_item(cls, item_name):
        for item in cls.all_items:
            if item.name == item_name:
                return item


    def parse_knx_itemline(self):
        """
        Extract parts of the item from text line
        """

        self.type, self.name = self.line.split()[:2]
        self.description = re.search(r'"(.+?)"',self.line).group(1)
        icon = re.search(r'<(\D*?)>',self.line)
        if icon:
            self.icon = icon.group(1)
        groups = re.search(r'\(\s?(.*?)\)\s?',self.line)
        if groups:
            self.groups = groups.group(1)
        knx_addr = re.search(r'{\s?knx="(.*?)"',self.line)
        if knx_addr:
            self.ga = knx_addr.group(1)
        # print(self.type, self.name, self.icon, self.knx_addresses)
        
