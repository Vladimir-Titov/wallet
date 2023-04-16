from typing import List, Optional, Mapping

from fastapi_utils.utils.misc import camel_case_to_snake_case


class AppError(Exception):
    default_message = 'Application error'
    status_code = 500

    def __init__(self, message: Optional[str] = None, errors: Optional[List[Mapping]] = None):
        self.message = message or self.default_message
        self.errors = errors
        self.code = camel_case_to_snake_case(self.__class__.__name__)
        super().__init__(
            'AppError %s: message="%s", errors=%s' % (self.code, self.message, str(errors)),
        )
