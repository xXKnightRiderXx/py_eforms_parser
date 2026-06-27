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

    def _get_optional_text(
        self, element: xml.etree.ElementTree.Element, xpath_expression: str, default: str | None = None
    ) -> str | None:
        """Search an element with an XPath expression and return its text value or default if the node does not exist

        This function takes an element that is part of the overall tree and searches for a specific subnode according to
        the given XPath expression. If such a node can be found and has a text value the function returns it. If the
        searched node does no exist or if the node is empty the function will return the given default value or None if
        no value is passed. Intended for fields that are optional in the eForms file as a missing element is treated as
        a normal condition and will not raise an exception.

        Args:
            element (xml.etree.ElementTree.Element): Element of the tree in which the find operation should be performed
            xpath_expression (str): The XPath expression of the sub-object that should be returned
            default (str | None, optional): _description_. Defaults to None.

        Returns:
            str | None: The text value of the requested object or the default value if it's not found
        """
        logger.debug(f"Searching in element {element.tag} with path {xpath_expression}")
        node = element.find(xpath_expression, NAMESPACES)
        if node is None:
            logger.debug(f"Node could not be found. Returning default value: {default}")
            return default
        # The node can be present but empty. in such cases node.text is None
        # We return the default value for now but theoretically an empty string would also be possible
        elif node.text is None:
            logger.debug(f"Node found but it has no content. Returning default value {default}")
            return default
        else:
            logger.debug(f"Node found. Returning its content: {node.text}")
            return node.text

    def _get_required_text(self, element: xml.etree.ElementTree.Element, xpath_expression: str) -> str:
        """Search an element with an XPath expression and return its text value

        This function takes an element that is part of the overall tree and searches for a specific subnode according to
        the given XPath expression. If such a node can be found and has a text value the function returns it. If the
        searched node does no exist a ValueError is raised. Intended for fields that are required in the eForms file and
        a missing element should lead to abortion of the parsing process.

        Args:
            element (xml.etree.ElementTree.Element): Element of the tree in which the find operation should be performed
            xpath_expression (str): The XPath expression of the sub-object that should be returned

        Raises:
            ValueError: If the given XPath expression can not be found in the given element

        Returns:
            str: The text value of the requested object
        """
        node_text = self._get_optional_text(element, xpath_expression)
        if node_text is None:
            logger.error(f"Required path {xpath_expression} could not be found in {element.tag}. Raising ValueError")
            raise ValueError(f"Required element {xpath_expression} not found in {element.tag}")
        return node_text

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
