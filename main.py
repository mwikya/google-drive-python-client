
# from __future__ import print_function
# import httplib2
import os,io,pdb

# from apiclient import discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage
# from apiclient.http import MediaFileUpload, MediaIoBaseDownload
# try:
#     import argparse
#     parser = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
# #     parser = argparse.ArgumentParser()
# import auth
# import logging


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/google-drive-credentials.json
# SCOPES = 'https://www.googleapis.com/auth/drive'
# CLIENT_SECRET_FILE = 'client_secret.json'
# APPLICATION_NAME = 'Drive API Python'
# authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
# credentials = authInst.getCredentials()

# http = credentials.authorize(httplib2.Http())
# drive_service = discovery.build('drive', 'v3', http=http)

# cwd_dir = os.getcwd()
# logs_dir = os.path.join(cwd_dir, '.logs')
# if not os.path.exists(logs_dir):
#     os.makedirs(logs_dir)
# logging.basicConfig(filename=os.path.join(logs_dir,'logs.log'), filemode='a',format='%(asctime)s %(levelname)s %(message)s',)

from cli_tools import parser

def list_files(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def upload_file(filename,filepath,mimetype,parent_id=None):
    file_metadata = {
                'name': filename,
                'parents': [parent_id],
    }
    media = MediaFileUpload(filepath,mimetype=mimetype,resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    return file.get('id')

def download_file(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def create_folder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get('id')

def search_file(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

def upload_dir(dirname):
    if not os.path.isdir(dirname):
        raise Exception("Not a Valid Directory :%s"%(dirname))
    else:
        base_dire_name = os.path.basename(dirname)
        base_dire_id = create_folder(base_dire_name)
        print("All files will be uploaded to the root folder: %s"%base_dire_name)
        count = 0
        for (root, dirs, filenames) in os.walk(top=dirname,topdown=True):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    file_id = upload_file(filename=filename,filepath=filepath,mimetype=None,parent_id=base_dire_id)
                    print("File : %s has been Uploaded Successfully"%filename)
                    count += 1            
                except Exception as e:
                    logging.error('FilePath: %s'%filepath,exc_info=True)
                    continue
        
        print("Total number of files uploaded: %d."%count)
        
def main():
    args = parser.parse_args()
    # if os.path.isdir(args.target):
    #     upload_dir(dirname=os.path.abspath(args.target))
    # else:
    #     filename = os.path.basename(args.target)
    #     full_path = os.path.abspath(args.target)
    #     upload_file(filename=filename,filepath=full_path,mimetype=None)
    argparse.Action

if __name__ == '__main__':
    main()