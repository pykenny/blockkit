from typing import List, Optional, Union

from pydantic.networks import HttpUrl

from blockkit.components import NewComponent
from blockkit.objects import MarkdownText, PlainText
from blockkit.validators import (
    validate_list_size,
    validate_string_length,
    validate_text_length,
    validator,
)

from . import Text
from .components import Component
from .elements import (
    Button,
    ChannelsSelect,
    Checkboxes,
    ConversationsSelect,
    DatePicker,
    Element,
    ExternalSelect,
    Image,
    MultiChannelsSelect,
    MultiConversationsSelect,
    MultiExternalSelect,
    MultiStaticSelect,
    MultiUsersSelect,
    Overflow,
    PlainTextInput,
    RadioButtons,
    Select,
    StaticSelect,
    Timepicker,
    UsersSelect,
)
from .fields import (
    ArrayField,
    BooleanField,
    ObjectField,
    StringField,
    TextField,
    UrlField,
    ValidationError,
)


class Block(Component):
    type = StringField()
    block_id = StringField(max_length=255)


Element = Union[
    Button,
    Checkboxes,
    DatePicker,
    StaticSelect,
    MultiStaticSelect,
    ExternalSelect,
    MultiExternalSelect,
    UsersSelect,
    MultiUsersSelect,
    ConversationsSelect,
    MultiConversationsSelect,
    ChannelsSelect,
    MultiChannelsSelect,
    Overflow,
    RadioButtons,
    Timepicker,
]


class NewBlock(NewComponent):
    block_id: Optional[str] = None

    _validate_block_id = validator("block_id", validate_string_length, max_len=255)


class Actions(NewBlock):
    type: str = "actions"
    elements: List[Element]

    def __init__(self, *, elements: List[Element], block_id: Optional[str] = None):
        super().__init__(elements=elements, block_id=block_id)

    _validate_elements = validator("elements", validate_list_size, min_len=1, max_len=5)


class Context(NewBlock):
    type: str = "context"
    elements: List[Union[Image, PlainText, MarkdownText]]

    def __init__(
        self,
        *,
        elements: List[Union[Image, PlainText, MarkdownText]],
        block_id: Optional[str] = None
    ):
        super().__init__(elements=elements, block_id=block_id)

    _validate_elements = validator(
        "elements", validate_list_size, min_len=1, max_len=10
    )


class Divider(NewBlock):
    type: str = "divider"

    def __init__(self, *, block_id: Optional[str] = None):
        super().__init__(block_id=block_id)


class Header(NewBlock):
    type: str = "header"
    text: PlainText

    def __init__(self, *, text: PlainText, block_id: Optional[str] = None):
        super().__init__(text=text, block_id=block_id)

    _validate_text = validator("text", validate_text_length, max_len=150)


class ImageBlock(NewBlock):
    type: str = "image"
    image_url: HttpUrl
    alt_text: PlainText
    title: Optional[PlainText] = None

    def __init__(
        self,
        *,
        image_url: HttpUrl,
        alt_text: PlainText,
        title: Optional[PlainText] = None,
        block_id: Optional[str] = None
    ):
        super().__init__(
            image_url=image_url, alt_text=alt_text, title=title, block_id=block_id
        )

    _validate_alt_text = validator("alt_text", validate_text_length, max_len=2000)
    _validate_title = validator("title", validate_text_length, max_len=2000)


class Section(Block):
    text = TextField(max_length=3000)
    fields = ArrayField(Text, max_items=10)
    accessory = ObjectField(Element)

    def __init__(self, text=None, block_id=None, fields=None, accessory=None):
        if not any((text, fields)):
            raise ValidationError("Provide either text or fields.")

        super().__init__("section", block_id, text, fields, accessory)


class Input(Block):
    label = TextField(plain=True, max_length=2000)
    element = ObjectField(PlainTextInput, Select, DatePicker, Checkboxes, RadioButtons)
    dispatch_action = BooleanField()
    hint = TextField(plain=True, max_length=2000)
    optional = BooleanField()

    def __init__(
        self,
        label,
        element,
        dispatch_action=None,
        block_id=None,
        hint=None,
        optional=None,
    ):
        super().__init__(
            "input", block_id, label, element, dispatch_action, hint, optional
        )
