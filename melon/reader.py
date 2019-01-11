import os
from abc import ABC, abstractmethod


class Reader(ABC):

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def _validate_file(self, file):
        pass

    def _list_and_validate(self, source_dir):
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        valid_files = []
        for f in files:
            file = source_dir / f
            if self._validate_file(file):
                valid_files.append(file)

        return valid_files
