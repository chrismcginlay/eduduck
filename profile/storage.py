#profile/storage.py
from os import path, remove
from django.core.files.storage import FileSystemStorage

class OverwriteFSStorage(FileSystemStorage):
    def get_available_name(self, name):
        if path.exists(self.path(name)):
            remove(self.path(name))
        return name 
