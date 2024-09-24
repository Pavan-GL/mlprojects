import sys

def error_message_details(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_fname.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line_number [{1}]  error message[{2}]".format(file_name,
                                                                                                             exc_tb.tb_lineno,
                                                                                                             str(error))
    return error_message


class CustomException(Exception):
    def __init__(self, error_messsage, error_detail: sys):
        super().__init__(error_messsage)
        self.error_message = error_message_details(error_messsage, error_detail)

    def __str__(self):
        return self.error_message
