import sys
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery

scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/programs/klima2_Grpi_secret.json', scopes=scopes)
http_auth = credentials.authorize(Http())
drive_service = discovery.build('drive', 'v3', http=http_auth)


def update_google_graph(file_id, new_filesource):
    media = MediaFileUpload(new_filesource, mimetype='image/png')
    file_metadata = file_id
    file = drive_service.files().update(fileId=file_id, media_body=media, fields='id').execute()
    file_id = file.get('id')
    print('File ID: %s' % file_id)
    return file_id


def main():
    file_id = '0B0-B_cA9RPAOSlNZRFc5cjNKRUU'
    new_filesource = '/home/pi/programs/temperature.png'
    update_google_graph(file_id, new_filesource)
    sys.exit(0)

if __name__ == "__main__":
    main()



