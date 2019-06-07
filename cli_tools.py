import argparse
parser = argparse.ArgumentParser(prog='drive-client',description="Command line script to upload files to google drive")
operations = parser.add_mutually_exclusive_group(required=True)


parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')

operations.add_argument(
    '-s','--search',
    help='Search for a file or directory in your drive',
    dest='search',
    )
operations.add_argument(
    '-u','--upload',
    help='Upload a file or a directory to google drive. If a directory is '
    'provided, a folder with the same name will be created in your drive with '
    'all its contents and those of its descendants',
    dest='upload',
    )
operations.add_argument(
    '-d','--download',
    help='Download a file from your drive',
    dest='download',
    )