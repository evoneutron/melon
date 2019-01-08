from abc import ABC, abstractmethod
import os


class Melon(ABC):
    @abstractmethod
    def interpret(self, source_dir):
        pass

    @abstractmethod
    def _validate_file(self, labels, file):
        pass

    def _list_and_validate(self, labels, dir):
        files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        valid_files = []
        for f in files:
            file = dir / f
            if self._validate_file(labels, file):
                valid_files.append(file)

        return valid_files
