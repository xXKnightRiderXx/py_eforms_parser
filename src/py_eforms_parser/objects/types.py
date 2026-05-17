import enum


class DocumentType(enum.StrEnum):
    """
    Enum for the three different document types that the eForms standard defines:
    https://docs.ted.europa.eu/eforms/latest/schema/documents-forms-and-notices.html#documentAndDocumentTypeSection
    """

    CONTRACT = "ContractNotice"
    CONTRACT_AWARD = "ContractAwardNotice"
    PRIOR_INFORMATION = "PriorInformationNotice"
