import defusedxml.ElementTree
import logging
import typing
import xml.etree.ElementTree

from py_eforms_parser.objects.tender import Tender
from py_eforms_parser.objects.types import DocumentType

logger = logging.getLogger(__name__)

NAMESPACES = {
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
    "efac": "http://data.europa.eu/p27/eforms-ubl-extension-aggregate-components/1",
    "efbc": "http://data.europa.eu/p27/eforms-ubl-extension-basic-components/1",
    "efext": "http://data.europa.eu/p27/eforms-ubl-extensions/1",
}


class EformsParser:

    def __init__(self, eforms_file: str | typing.IO[str]):
        logger.debug(f"Trying to parse file: {eforms_file}")
        self.xml_tree = defusedxml.ElementTree.parse(eforms_file)

    def _parse_document_type(self, root_element: xml.etree.ElementTree.Element) -> DocumentType:
        """Parse the document type of the eForms file

        Parse the document type of the eForms file from the root element tag of the XML tree.

        Args:
            root_element (xml.etree.ElementTree.Element): Root element of the XML tree

        Returns:
            DocumentType: Document Type of the eForms file
        """
        logger.debug(f"Trying to extract document type from root element tag: {root_element.tag}")
        # The root tag typically looks like this: "{namespace}DocumentType", hence strip the namespace
        document_type = root_element.tag.split("}")[-1]
        logger.info(f"Extracted document type string: {document_type}")
        return DocumentType(document_type)

    def parse(self) -> Tender:
        root_element = self.xml_tree.getroot()
        if root_element is None:
            raise ValueError("Could not retrieve root element from XML document!")
        document_type = self._parse_document_type(root_element)
        return Tender(type=document_type)
