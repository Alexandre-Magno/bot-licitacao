from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleDrive:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/drive"]
        self.SERVICE_ACCOUNT_FILE = "service_account.json"
        self.robo_folder_id = "1zPJfkduR-9_27LFP7gUOTjoWC08t4Ir4"

    def authenticate(self):
        creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
        )
        return creds

    def upload_file(self, file_path, parent_folder_id, name_file):

        creds = self.authenticate()
        service = build("drive", "v3", credentials=creds)
        file_metadata = {
            "name": name_file,
            "parents": [parent_folder_id],
        }

        file = (
            service.files()
            .create(
                body=file_metadata,
                media_body=file_path,
            )
            .execute()
        )
        print(f"File ID: {file.get('id')}")
        return file.get("id")

    def create_folder(self, folder_name, parent_folder_id):
        creds = self.authenticate()
        service = build("drive", "v3", credentials=creds)
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_folder_id],
        }

        file = service.files().create(body=file_metadata, fields="id").execute()
        print(f'Folder ID: "{file.get("id")}".')
        return file.get("id")


if __name__ == "__main__":
    drive = GoogleDrive()
    folder_id = drive.create_folder("04/01 - Brasilia - Rádio", drive.robo_folder_id)
    drive.upload_file("scammer-agent.pdf", folder_id, "edital")
