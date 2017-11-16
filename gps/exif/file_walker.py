from os import walk


class FileManager:
    @staticmethod
    def get_all_files(path):
        for (dirpath, dirnames, filenames) in walk(path):
            for i in range(len(filenames)):
                filenames[i] = path +'/'+ filenames[i]
            return filenames
            break

