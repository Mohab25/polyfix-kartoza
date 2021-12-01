import fiona
from pathlib import PurePosixPath

class polyfixIO():
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.driver = ''
        self.crs = ''
        self.schema = ''

    def get_features(self):
        with fiona.open(self.file_path) as f:
            self.driver = f.driver
            self.crs = f.crs
            self.schema = f.schema
            self.features = list(f)
            return self.features

    def get_input_features(self):
        input_features = []
        [input_features.append({'id':index, 'feat': i}) for index, i in enumerate(self.features)]
        return input_features

    def output_to_file(self, output, output_path :str = '', output_name :str = '' ):
        """
            outputs the refined geometry to a file.

            params:
            -----
            output (collection): objects holding spatial data
            which to be output to a file
            output_path(str): a path holds the information about
            the output file (path, name and extension)
        """
        output_path = str(output_path)
        if output_path == '':
            output_path_parent = PurePosixPath(self.file_path).parent
            suffix = PurePosixPath(self.file_path).suffixes[0]
            if output_name == '':
                stem = PurePosixPath(self.file_path).stem
                file_output_name = stem+'_corrected'
            else:
                file_output_name = output_name
            output_path = PurePosixPath(output_path_parent).joinpath(f'{file_output_name}{suffix}')
            output_path = str(output_path)
        with fiona.open(output_path, 'w', driver=self.driver, crs=self.crs,
                        schema=self.schema) as f:
            f.writerecords(output)

        