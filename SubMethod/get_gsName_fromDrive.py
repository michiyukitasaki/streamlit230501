from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



def load_user_credentials():
    gauth = GoogleAuth()
    # Replace with the path to your client_secrets.json file

    client_secrets_file = '/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/SubMethod/client_secret_55056233712-9caqb3e4j3dpru92l7nes61afkmhr73f.apps.googleusercontent.com (2).json'

    gauth.LoadClientConfigFile(client_secrets_file)
    gauth.LocalWebserverAuth()
    return gauth

def list_google_drive_files(choice):
    gauth = load_user_credentials()
    drive = GoogleDrive(gauth)

    # Google Document, Google Spreadsheets, Google SlidesのMIMEタイプ
    # all_mime_types = ["application/vnd.google-apps.document", "application/vnd.google-apps.spreadsheet",
    #               "application/vnd.google-apps.presentation"]

    # 取得するファイルのMIMEタイプを指定します。
    if choice == "スプレッドシート":
        mime_type = "application/vnd.google-apps.spreadsheet"
    elif choice == "ドキュメント":
        mime_type = "application/vnd.google-apps.document"
    elif choice == "スライド":
        mime_type = "application/vnd.google-apps.presentation"


    file_list = drive.ListFile({'q': f"'root' in parents and mimeType='{mime_type}' and trashed=false"}).GetList()

    # Auto-iterate through all files in the root folder.
    # file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
    # for file1 in file_list:
    #     print('title: %s, id: %s' % (file1['title'], file1['id']))


    return file_list


if __name__ == '__main__':
    list_google_drive_files()
