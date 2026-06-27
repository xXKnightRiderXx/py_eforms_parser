import enum


class DocumentType(enum.StrEnum):
    """
    Enum for the three different document types that the eForms standard defines:
    https://docs.ted.europa.eu/eforms/latest/schema/documents-forms-and-notices.html#documentAndDocumentTypeSection
    """

    CONTRACT = "ContractNotice"
    CONTRACT_AWARD = "ContractAwardNotice"
    PRIOR_INFORMATION = "PriorInformationNotice"


class NoticeType(enum.StrEnum):
    """
    Enum for the different notice types that the eForms standard defines:
    https://docs.ted.europa.eu/eforms/latest/reference/code-lists/notice-type.html

    We add the description of the notice type as an additional attribute to the enum. Idea taken from here:
    https://rednafi.com/python/add-attributes-to-enum-members/
    """
    description: str

    def __new__(cls, value: str, description: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    # Prior Information Notices
    PIN_ONLY = ("pin-only", "Prior information notice or a periodic indicative notice used only for information")
    PIN_BUYER = (
        "pin-buyer",
        "Notice of the publication of a prior information notice or a periodic information notice on a buyer profile",
    )
    PIN_CFC_STANDARD = (
        "pin-cfc-standard",
        "Prior information notice or a periodic indicative notice used as a call for competition - standard regime",
    )
    PIN_CFC_SOCIAL = (
        "pin-cfc-social",
        "Prior information notice or a periodic indicative notice used as a call for competition - light regime",
    )
    PIN_RTL = (
        "pin-rtl",
        "Prior information notice or a periodic indicative notice used to shorten time limits for receipt of tenders",
    )
    PIN_TRAN = ("pin-tran", "Prior information notice for public passenger transport services")

    # Contract Notices
    CN_STANDARD = ("cn-standard", "Contract or concession notice - standard regime")
    CN_SOCIAL = ("cn-social", "Contract notice - light regime")
    CN_DESG = ("cn-desg", "Design contest notice")

    # Contract Award Notices
    CAN_STANDARD = ("can-standard", "Contract or concession award notice - standard regime")
    CAN_SOCIAL = ("can-social", "Contract or concession award notice - light regime")
    CAN_DESG = ("can-desg", "Design contest result notice")
    CAN_MODIF = ("can-modif", "Contract modification notice")
    CAN_TRAN = ("can-tran", "Contract award notice for public passenger transport services")

    # Other
    BRIN_ECS = ("brin-ecs", "European Company / European Cooperative Society notice")
    BRIN_EEIG = ("brin-eeig", "European Economic Interest Grouping notice")
    COMPL = ("compl", "Contract completion notice")
    PMC = ("pmc", "Pre-market consultation notice")
    QU_SY = ("qu-sy", "Notice on the existence of a qualification system")
    SUBCO = ("subco", "Subcontracting notice")
    VEAT = ("veat", "Voluntary ex-ante transparency notice")
