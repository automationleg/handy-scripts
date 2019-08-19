import os
import sys
import re
from pathlib import Path
from knxitems import KnxItem
from knxthings import Device, Channel
import argparse

output_dir = 'knx2_output'

def read_file(filename):
    with open(filename, encoding="utf8") as f:
        return f.read()


def parse_knx_items_from_file(file_name):
    items_file = read_file(file_name)
    
    for line in items_file.splitlines():
        if "knx=" in line and not line.strip().startswith('//'):

            items = KnxItem(line=line)

            # item_name = line.split()[1]
            # left_index = line.find('knx="')+5
            # right_index = line.find('"',left_index)
            # knx_addr = line[left_index:right_index]
            # item_name = item.name
            # knx_addr = item.ga
            # items[item_name] = knx_addr
            # print(f'"{item_name}" : "{knx_addr}"')
    return items

def update_things_file(items :KnxItem, things_file, outfile):
    things = read_file(things_file)

    updated_things = []
    for line in things.splitlines():
        if 'Type' in line:
            # get knx value by item_name
            # print(re.search(r'"(.*?)"', line).group(1))
            item_name = re.search(r'"(.*?)"', line).group(1)
            # print(f'looking for object with name {item_name}: {items.find_item(item_name)}')
            knx_value = items.find_item(item_name).ga
            line = re.sub(r'"(\d+.\d+:)?\d/\d+/\d+.+\d/\d+/\d+"',f'"{knx_value}"',line)
        updated_things.append(line)


    # new_filename = things_file.replace('.things','_knx2.things')
    new_filename = outfile
    with open(new_filename, 'w') as updated_file:
        updated_file.write("\n".join(updated_things))



def create_items_file(knx_items: KnxItem, file_name: str, outfile: str):
    things_str = read_file(file_name)

    for line in things_str.splitlines():
        if line and line.split()[0].startswith('Thing'):
            things = Device(name=line.split()[2])
        if line and line.split()[0].startswith('Type'):
            _, type, _, channel, name = line.split()[:5]
            ga = re.search(r'ga="(.*?)"',line).group(1)
            # print(f'{type}, {channel}, {name}, {ga}')
            things.add_channel(type=type, name=name.strip('"'), channel=channel,ga=ga)

    updated_items = []
    for device in things.items():
        # print(device)
        for channel_item in device.get_channels_list():
            knx_item = knx_items.find_item(channel_item.name)
            channel_text = '{ '+f'channel="knx:device:MDTRouter:{device.name}:{channel_item.channel}'+'" }'
            icon = f'<{knx_item.icon}>' if knx_item.icon else ''
            description = f'"{knx_item.description}"'
            groups = f'({knx_item.groups})' if knx_item.groups else ''
            # print(f'{channel_item.type}\t{channel_item.name}\t\t"{knx_item.description}"\t\t{knx_item.icon}\t\t({knx_item.groups})\t\t'+channel_text)
            item_line = f'{knx_item.type:<16} {channel_item.name:<40} {description:<35} {icon:<17} {groups:<75} {channel_text:<50}'
            updated_items.append(item_line)

    # new_filename = itemsfile.replace('.items','_new.items')
    new_filename = outfile
    with open(new_filename, 'w',encoding='utf-8') as updated_file:
        updated_file.write("\n".join(updated_items))     

def main():
    my_parser = argparse.ArgumentParser(
        usage='%(prog)s things_file items_file',
        description='update knx group addresses in things file based on knx1 items file and create knx2 binding supported items file')
    my_parser.add_argument('--things',
                       metavar='things',
                       type=str,
                       # nargs=1,
                       help='the path to things file')
    my_parser.add_argument('--items',
                       metavar='items',
                       type=str,
                       nargs='+',
                       help='the path to items file')

    # exit when no arguments
    if len(sys.argv[1:])==0:
        my_parser.print_usage()
        my_parser.exit()

    args = my_parser.parse_args()
    thingsfile = args.things
    itemfiles = args.items

    if not os.path.isfile(thingsfile):
        print('The path specified to things file does not exist')
        sys.exit()


    for filename in itemfiles:
        if not os.path.isfile(filename):
            print('The path specified to items file does not exist')
            sys.exit()
        knx_items = parse_knx_items_from_file(filename)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    output_things_file = os.path.basename(thingsfile).replace('.things','_knx2.things')
    updated_things_file = f'{output_dir}/{output_things_file}'

    print(f'Creating {updated_things_file} Thing file with updated knx addresses')
    update_things_file(knx_items, thingsfile, updated_things_file)
    output_items_file = 'generated_knx2.items'

    updated_items_file = f'{output_dir}/{output_items_file}'

    print(f'Creating KNX2 supported items file with name: {updated_items_file}')
    create_items_file(knx_items, updated_things_file, updated_items_file)

if __name__ == "__main__":
    main()

            
