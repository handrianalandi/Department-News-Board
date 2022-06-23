from nameko.rpc import rpc
import gateway.dependencies.database as database

class FileService:

    name = "file_service"

    database=database.Database()

    @rpc
    def upload_file(self, filename,filepath):
        return self.database.upload_file(filename, filepath)

    @rpc
    def download_file(self,file_id):
        return self.database.download_file(file_id)

    @rpc
    def get_file_id(self,filename,filepath):
        return self.database.get_file_id(filename,filepath)