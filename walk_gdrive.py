# walk_gdrive.py - os.walk variation with Google Drive API
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, json
from apiclient.discovery import build  # pip install google-api-python-client


FOLDER = 'application/vnd.google-apps.folder'

def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/kkonwar/.ssh/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


creds = get_credentials()
service = build('drive', version='v3', credentials=creds)

def iterfiles(name=None, is_folder=None, parent=None, order_by='folder,name,createdTime'):
    """ Iterate though the folders and 
    """
    q = []
    if name is not None:
        q.append("name = '%s'" % name.replace("'", "\\'"))
    if is_folder is not None:
        q.append("mimeType %s '%s'" % ('=' if is_folder else '!=', FOLDER))
    if parent is not None:
        q.append("'%s' in parents" % parent.replace("'", "\\'"))
    params = {'pageToken': None, 'orderBy': order_by}
    if q:
        params['q'] = ' and '.join(q)
    while True:
        response = service.files().list(**params).execute()
        for f in response['files']:
            yield f
        try:
            params['pageToken'] = response['nextPageToken']
        except KeyError:
            return

def walk(top):
    "walk though the files"
    top, = iterfiles(name=top, is_folder=True)
    stack = [((top['name'],), top)]
    while stack:
        path, top = stack.pop()
        dirs, files = is_file = [], []
        for f in iterfiles(parent=top['id']):
            is_file[f['mimeType'] != FOLDER].append(f)
        yield path, top, dirs, files
        if dirs:
            stack.extend((path + (d['name'],), d) for d in dirs)


for testdir in ['HCA']:
    for path, root, dirs, files in walk(testdir):
        print('%s\t%d %d' % ('/'.join(path), len(dirs), len(files)))
