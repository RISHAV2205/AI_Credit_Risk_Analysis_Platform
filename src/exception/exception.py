"""
Custom Exception Module

Provides a reusable exception class that captures
the original exception along with the file name
and line number where it occurred.
"""

import sys
class CreditRiskException(Exception):
    """
    Custom exception class for the project.
    """

    def __init__(self, error_message, error_detail: sys):
        """
        Parameters
        ----------
        error_message : Exception
            Original exception object.
        error_detail : sys
            Python sys module used to extract traceback information.
        """

        _, _, exc_tb = error_detail.exc_info()
        # extract file name from traceback object
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_number = exc_tb.tb_lineno

        self.error_message = str(error_message)

        super().__init__(self.error_message)
        
    def __str__(self):

        return (
            f"\nError occurred in python script: [{self.file_name}]"
            f"\nLine Number: [{self.line_number}]"
            f"\nError Message: {self.error_message}"
        )