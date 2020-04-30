import os
import pickle




def read_file(filename, rp):
    """
    :argument:
        :param filename: A string which represents the raw data file, in properties.conf,
                          used for the process (experiment).
        :param rp: Absolute path of the root directory of the project
        # Note: File should be using UTF-8 encoding. Change the encoding as needed.
    :exception:
        :except IOError: This may occur because of many reasons. e.g file is missing or corrupt file or wrong file path
    :return:
        boolean_flag: True for successful read operation.
        file: TextIOWrapper for the file corresponding to the `file_name` key in properties.conf
    """
    text_file_encoding = 'utf8'
    try:
        file = open(filename, "r", encoding=text_file_encoding)
        return True, file
    except IOError as e:
        print("File IO Error :: Cannot open " + filename + "\n" + str(e))
        return False


def write_obj(obj, filename, rp):
    """
    :argument:
        :param obj: Object to br written to the disk at the given location
        :param filename: String which represents the file from properties.conf
        :param rp: Absolute path of the root directory of the project
    :return:
        boolean flag: True for successful operation.
    """

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as err:
            print("Error creating director " + filename + "\n" + str(err))
            return False
    try:
        with open(filename, "wb") as file:
            pickle.dump(obj, file, protocol=pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print("File IO Error :: Cannot write object to " + filename + "\n" + str(e))
        return False
    return True


def read_obj(filename, rp):
    """
    :argument:
        :param filename: A string which represents the raw data file, in properties.conf,
                          used for the process (experiment).
        :param rp: Absolute path of the root directory of the project
        # Note: File should be using UTF-8 encoding. Change the encoding as needed.
    :exception:
        :except IOError: This may occur because of many reasons. e.g file is missing or corrupt file or wrong file path
    :return:
        boolean_flag: True for successful read operation.
        file: TextIOWrapper for the file corresponding to the `file_name` key in properties.conf
    """
    try:
        file = open(filename, "rb")
        obj = pickle.load(file)
        return True, obj
    except IOError as e:
        print("File IO Error :: Cannot open " + filename + "\n" + str(e))
        return False