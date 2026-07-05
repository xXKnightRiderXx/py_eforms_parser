import xml.etree.ElementTree
import pytest

from py_eforms_parser.parser.eformsparser import EformsParser
from py_eforms_parser.objects.types import DocumentType, NoticeType

TEST_NAMESPACES = (
    'xmlns="urn:oasis:names:specification:ubl:schema:xsd:ContractNotice-2" '
    'xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" '
    'xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" '
    'xmlns:efac="http://data.europa.eu/p27/eforms-ubl-extension-aggregate-components/1" '
    'xmlns:efbc="http://data.europa.eu/p27/eforms-ubl-extension-basic-components/1" '
    'xmlns:efext="http://data.europa.eu/p27/eforms-ubl-extensions/1" '
    'xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" '
)


@pytest.fixture
def parser() -> EformsParser:
    """
    Create EformsParser instance for testing purposes

    Most tests verify the internal methods of the EformsParser class and we need to pass them the relevant element of
    the XML tree explicitly. We therefore don't want to pass an XML file in the constructor as it will never be relied
    on during the tests. Hence we use __new__ which avoids calling __init__

    Returns:
        EformsParser: An instance of the EformsParser class
    """
    return EformsParser.__new__(EformsParser)


def make_root_element(document_type: str = "ContractNotice", body: str = "") -> xml.etree.ElementTree.Element:
    """
    Build a synthetic XML root element with custom body for testing purposes

    Allow the tests to dynamically create a synthetic XML tree with a custom body. This makes it possible for the tests
    to model different parts of the eForms files which means we don't have to use full eForms documents for testing
    purposes.

    Args:
        document_type (str, optional): Main document type such as ContractNotice, ContractAwardNotice or
        PriorInformationNotice. Defaults to "ContractNotice".
        body (str, optional): Optional content of the XML body. Defaults to "".

    Returns:
        xml.etree.ElementTree.Element: Root element of the synthetic XML tree
    """
    return xml.etree.ElementTree.fromstring(f"<{document_type} {TEST_NAMESPACES}>{body}</{document_type}>")


class TestParseDocumentType:

    @pytest.mark.parametrize(
        "tag_name,expected_type",
        [
            ("ContractNotice", DocumentType.CONTRACT),
            ("ContractAwardNotice", DocumentType.CONTRACT_AWARD),
            ("PriorInformationNotice", DocumentType.PRIOR_INFORMATION),
        ],
    )
    def test_parse_known_document_types(self, parser: EformsParser, tag_name: str, expected_type: DocumentType):
        element = make_root_element(document_type=tag_name)
        assert parser._parse_document_type(element) is expected_type  # type: ignore

    def test_unknown_type_raises_value_error(self, parser: EformsParser):
        element = make_root_element(document_type="UnknownType")
        with pytest.raises(ValueError):
            parser._parse_document_type(element)  # type: ignore


class TestParseNoticeType:

    @pytest.mark.parametrize(
        "code,notice_type", [("pin-only", NoticeType.PIN_ONLY), ("pin-buyer", NoticeType.PIN_BUYER)]
    )
    def test_parse_notice_type(self, parser: EformsParser, code: str, notice_type: NoticeType):
        element = make_root_element(body=f'<cbc:NoticeTypeCode listName="notice-type">{code}</cbc:NoticeTypeCode>')
        assert parser._parse_notice_type(element) is notice_type  # type: ignore

    def test_unknown_notice_type_raises_value_error(self, parser: EformsParser):
        element = make_root_element(body='<cbc:NoticeTypeCode listName="notice-type">UNKNOWN</cbc:NoticeTypeCode>')
        with pytest.raises(ValueError):
            parser._parse_notice_type(element)  # type: ignore

    def test_missing_notice_type_raises_value_error(self, parser: EformsParser):
        element = make_root_element()
        with pytest.raises(ValueError):
            parser._parse_notice_type(element)  # type: ignore


class TestParseNoticeId:

    @pytest.mark.parametrize(
        "expected_id,notice_id",
        [("d503ead5-0e2e-492f-973e-6541c9e88180", "d503ead5-0e2e-492f-973e-6541c9e88180"), ("24061260", "24061260")],
    )
    def test_parse_notice_id(self, parser: EformsParser, expected_id: str, notice_id: str):
        element = make_root_element(body=f"<cbc:ID>{expected_id}</cbc:ID>")
        assert parser._parse_notice_id(element) == notice_id  # type: ignore

    def test_empty_notice_id_raises_value_error(self, parser: EformsParser):
        element = make_root_element(body=f"<cbc:ID></cbc:ID>")
        with pytest.raises(ValueError):
            parser._parse_notice_id(element)  # type: ignore

    def test_missing_notice_id_raises_value_error(self, parser: EformsParser):
        element = make_root_element()
        with pytest.raises(ValueError):
            parser._parse_notice_id(element)  # type: ignore


class TestParseNoticeVersion:

    @pytest.mark.parametrize(
        "expected_version,notice_version",
        [("01", 1), ("03", 3), ("4", 4)],
    )
    def test_parse_notice_id(self, parser: EformsParser, expected_version: str, notice_version: str):
        element = make_root_element(body=f"<cbc:VersionID>{expected_version}</cbc:VersionID>")
        assert parser._parse_notice_version(element) == notice_version  # type: ignore

    @pytest.mark.parametrize(
        "invalid_version",
        [("00"), ("0"), ("-1"), ("-10")],
    )
    def test_invalid_notice_id_raises_value_error(self, parser: EformsParser, invalid_version: str):
        element = make_root_element(body=f"<cbc:VersionID>{invalid_version}</cbc:VersionID>")
        with pytest.raises(ValueError):
            parser._parse_notice_version(element)  # type: ignore

    def test_empty_notice_version_raises_value_error(self, parser: EformsParser):
        element = make_root_element(body=f"<cbc:VersionID></cbc:VersionID>")
        with pytest.raises(ValueError):
            parser._parse_notice_version(element)  # type: ignore

    def test_missing_notice_version_raises_value_error(self, parser: EformsParser):
        element = make_root_element()
        with pytest.raises(ValueError):
            parser._parse_notice_version(element)  # type: ignore
