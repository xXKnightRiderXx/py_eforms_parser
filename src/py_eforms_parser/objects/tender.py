import logging
import pydantic

from py_eforms_parser.objects.types import DocumentType

logger = logging.getLogger(__name__)


class Tender(pydantic.BaseModel):
    type: DocumentType
