import dataclasses as dc
import typing
from typing import Any, Callable, ClassVar, Dict, Generic, Optional, Tuple, Type, TypeVar, Union

import pydantic as pd
import pydantic_core as pdc
from pydantic import BaseModel, RootModel
from pydantic._internal._model_construction import ModelMetaclass  # noqa

from . import config, errors, utils
from .element import SearchMode
from .element.native import ElementT, XmlElement, etree
from .serializers.factories.model import BaseModelSerializer
from .serializers.serializer import Serializer, XmlEntityInfoP
from .typedefs import EntityLocation
from .utils import NsMap

__all__ = (
    'attr',
    'element',
    'wrapped',
    'computed_attr',
    'computed_element',
    'BaseXmlModel',
    'RootXmlModel',
)


@dc.dataclass
class ComputedXmlEntityInfo(pd.fields.ComputedFieldInfo):
    """
    Computed field xml meta-information.
    """

    __slots__ = ('location', 'path', 'ns', 'nsmap', 'wrapped')

    location: Optional[EntityLocation]
    path: Optional[str]
    ns: Optional[str]
    nsmap: Optional[NsMap]
    wrapped: Optional[XmlEntityInfoP]  # to be compliant with XmlEntityInfoP protocol

    def __post_init__(self) -> None:
        if config.REGISTER_NS_PREFIXES and self.nsmap:
            utils.register_nsmap(self.nsmap)


PropertyT = typing.TypeVar('PropertyT')


def computed_entity(
        location: EntityLocation,
        prop: Optional[PropertyT] = None,
        **kwargs: Any,
) -> Union[PropertyT, Callable[[PropertyT], PropertyT]]:
    def decorator(prop: Any) -> Any:
        path = kwargs.pop('path', None)
        ns = kwargs.pop('ns', None)
        nsmap = kwargs.pop('nsmap', None)

        descriptor_proxy = pd.computed_field(**kwargs)(prop)
        descriptor_proxy.decorator_info = ComputedXmlEntityInfo(
            location=location,
            path=path,
            ns=ns,
            nsmap=nsmap,
            wrapped=None,
            **dc.asdict(descriptor_proxy.decorator_info),
        )

        return descriptor_proxy

    if prop is None:
        return decorator
    else:
        return decorator(prop)


def computed_attr(
        prop: Optional[PropertyT] = None,
        *,
        name: Optional[str] = None,
        ns: Optional[str] = None,
        **kwargs: Any,
) -> Union[PropertyT, Callable[[PropertyT], PropertyT]]:
    """
    Marks a property as an xml attribute.

    :param prop: decorated property
    :param name: attribute name
    :param ns: attribute xml namespace
    :param kwargs: pydantic computed field arguments. See :py:class:`pydantic.computed_field`
    """

    return computed_entity(EntityLocation.ATTRIBUTE, prop, path=name, ns=ns, **kwargs)


def computed_element(
        prop: Optional[PropertyT] = None,
        *,
        tag: Optional[str] = None,
        ns: Optional[str] = None,
        nsmap: Optional[NsMap] = None,
        **kwargs: Any,
) -> Union[PropertyT, Callable[[PropertyT], PropertyT]]:
    """
    Marks a property as an xml element.

    :param prop: decorated property
    :param tag: element tag
    :param ns: element xml namespace
    :param nsmap: element xml namespace map
    :param kwargs: pydantic computed field arguments. See :py:class:`pydantic.computed_field`
    """

    return computed_entity(EntityLocation.ELEMENT, prop, path=tag, ns=ns, nsmap=nsmap, **kwargs)


class XmlEntityInfo(pd.fields.FieldInfo):
    """
    Field xml meta-information.
    """

    __slots__ = ('location', 'path', 'ns', 'nsmap', 'wrapped')

    def __init__(
            self,
            location: Optional[EntityLocation],
            /,
            path: Optional[str] = None,
            ns: Optional[str] = None,
            nsmap: Optional[NsMap] = None,
            wrapped: Optional[pd.fields.FieldInfo] = None,
            **kwargs: Any,
    ):
        if wrapped is not None:
            # copy arguments from the wrapped entity to let pydantic know how to process the field
            for entity_field_name in utils.get_slots(wrapped):
                kwargs[entity_field_name] = getattr(wrapped, entity_field_name)

        if kwargs.get('serialization_alias') is None:
            kwargs['serialization_alias'] = kwargs.get('alias')

        if kwargs.get('validation_alias') is None:
            kwargs['validation_alias'] = kwargs.get('alias')

        super().__init__(**kwargs)
        self.location = location
        self.path = path
        self.ns = ns
        self.nsmap = nsmap
        self.wrapped: Optional[XmlEntityInfoP] = wrapped if isinstance(wrapped, XmlEntityInfo) else None

        if config.REGISTER_NS_PREFIXES and nsmap:
            utils.register_nsmap(nsmap)


def attr(name: Optional[str] = None, ns: Optional[str] = None, **kwargs: Any) -> Any:
    """
    Marks a pydantic field as an xml attribute.

    :param name: attribute name
    :param ns: attribute xml namespace
    :param kwargs: pydantic field arguments. See :py:class:`pydantic.Field`
    """

    return XmlEntityInfo(EntityLocation.ATTRIBUTE, path=name, ns=ns, **kwargs)


def element(tag: Optional[str] = None, ns: Optional[str] = None, nsmap: Optional[NsMap] = None, **kwargs: Any) -> Any:
    """
    Marks a pydantic field as an xml element.

    :param tag: element tag
    :param ns: element xml namespace
    :param nsmap: element xml namespace map
    :param kwargs: pydantic field arguments. See :py:class:`pydantic.Field`
    """

    return XmlEntityInfo(EntityLocation.ELEMENT, path=tag, ns=ns, nsmap=nsmap, **kwargs)


def wrapped(
        path: str,
        entity: Optional[pd.fields.FieldInfo] = None,
        ns: Optional[str] = None,
        nsmap: Optional[NsMap] = None,
        **kwargs: Any,
) -> Any:
    """
    Marks a pydantic field as a wrapped xml entity.

    :param entity: wrapped entity
    :param path: entity path
    :param ns: element xml namespace
    :param nsmap: element xml namespace map
    :param kwargs: pydantic field arguments. See :py:class:`pydantic.Field`
    """

    return XmlEntityInfo(EntityLocation.WRAPPED, path=path, ns=ns, nsmap=nsmap, wrapped=entity, **kwargs)


class XmlModelMeta(ModelMetaclass):
    """
    Xml model metaclass.
    """

    def __new__(
            mcls,
            name: str,
            bases: Tuple[type],
            namespace: Dict[str, Any],
            **kwargs: Any,
    ) -> Type['BaseXmlModel']:
        is_abstract: bool = kwargs.pop('__xml_abstract__', False)

        cls = typing.cast(Type['BaseXmlModel'], super().__new__(mcls, name, bases, namespace, **kwargs))
        if not is_abstract:
            cls.__build_serializer__()

        return cls


ModelT = TypeVar('ModelT', bound='BaseXmlModel')


class BaseXmlModel(BaseModel, __xml_abstract__=True, metaclass=XmlModelMeta):
    """
    Base pydantic-xml model.
    """

    __xml_tag__: ClassVar[Optional[str]]
    __xml_ns__: ClassVar[Optional[str]]
    __xml_nsmap__: ClassVar[Optional[NsMap]]
    __xml_ns_attrs__: ClassVar[bool]
    __xml_skip_empty__: ClassVar[Optional[bool]]
    __xml_search_mode__: ClassVar[SearchMode]
    __xml_serializer__: ClassVar[Optional[BaseModelSerializer]] = None

    def __init_subclass__(
            cls,
            tag: Optional[str] = None,
            ns: Optional[str] = None,
            nsmap: Optional[NsMap] = None,
            ns_attrs: Optional[bool] = None,
            skip_empty: Optional[bool] = None,
            search_mode: Optional[SearchMode] = None,
            **kwargs: Any,
    ):
        """
        Initializes a subclass.

        :param tag: element tag
        :param ns: element namespace
        :param nsmap: element namespace map
        :param ns_attrs: use namespaced attributes
        :param search_mode: element search mode
        """

        super().__init_subclass__(**kwargs)

        cls.__xml_tag__ = tag if tag is not None else getattr(cls, '__xml_tag__', None)
        cls.__xml_ns__ = ns if ns is not None else getattr(cls, '__xml_ns__', None)
        cls.__xml_nsmap__ = nsmap if nsmap is not None else getattr(cls, '__xml_nsmap__', None)
        cls.__xml_ns_attrs__ = ns_attrs if ns_attrs is not None else getattr(cls, '__xml_ns_attrs__', False)
        cls.__xml_skip_empty__ = skip_empty if skip_empty is not None else getattr(cls, '__xml_skip_empty__', None)
        cls.__xml_search_mode__ = search_mode if search_mode is not None \
            else getattr(cls, '__xml_search_mode__', SearchMode.STRICT)

    @classmethod
    def __build_serializer__(cls) -> None:
        if cls is BaseXmlModel:
            return

        # checks that all generic parameters are provided
        if cls.__pydantic_root_model__:
            if cls.__pydantic_generic_metadata__['parameters']:
                if cls.model_fields.get('root') is None or isinstance(cls.model_fields['root'].annotation, TypeVar):
                    cls.__xml_serializer__ = None
                    return
        else:
            if cls.__pydantic_generic_metadata__['parameters']:
                cls.__xml_serializer__ = None
                return

        if config.REGISTER_NS_PREFIXES and cls.__xml_nsmap__:
            utils.register_nsmap(cls.__xml_nsmap__)

        if cls.__pydantic_complete__:  # checks that all forward refs are resolved
            serializer = Serializer.parse_core_schema(
                schema=cls.__pydantic_core_schema__,
                ctx=Serializer.Context(
                    model_name=cls.__name__,
                    namespaced_attrs=cls.__xml_ns_attrs__,
                    search_mode=cls.__xml_search_mode__,
                    entity_info=XmlEntityInfo(
                        EntityLocation.ELEMENT,
                        path=cls.__xml_tag__,
                        ns=cls.__xml_ns__,
                        nsmap=cls.__xml_nsmap__,
                    ),
                ),
            )
            assert isinstance(serializer, BaseModelSerializer), "unexpected serializer type"
            cls.__xml_serializer__ = serializer
        else:
            cls.__xml_serializer__ = None

    @classmethod
    def model_rebuild(cls, **kwargs: Any) -> None:
        super().model_rebuild(**kwargs)

        if cls.__xml_serializer__ is None and cls.__pydantic_complete__:
            cls.__build_serializer__()

    @classmethod
    def from_xml_tree(cls: Type[ModelT], root: etree.Element, context: Optional[Dict[str, Any]] = None) -> ModelT:
        """
        Deserializes an xml element tree to an object of `cls` type.

        :param root: xml element to deserialize the object from
        :param context: pydantic validation context
        :return: deserialized object
        """

        assert cls.__xml_serializer__ is not None, f"model {cls.__name__} is partially initialized"

        if root.tag == cls.__xml_serializer__.element_name:
            obj = typing.cast(ModelT, cls.__xml_serializer__.deserialize(XmlElement.from_native(root), context=context))
            return obj
        else:
            raise errors.ParsingError(
                f"root element not found (actual: {root.tag}, expected: {cls.__xml_serializer__.element_name})",
            )

    @classmethod
    def from_xml(cls: Type[ModelT], source: Union[str, bytes], context: Optional[Dict[str, Any]] = None) -> ModelT:
        """
        Deserializes an xml string to an object of `cls` type.

        :param source: xml string
        :param context: pydantic validation context
        :return: deserialized object
        """

        return cls.from_xml_tree(etree.fromstring(source), context=context)

    def to_xml_tree(self, *, skip_empty: bool = False) -> etree.Element:
        """
        Serializes the object to an xml tree.

        :param skip_empty: skip empty elements (elements without sub-elements, attributes and text, Nones)
        :return: object xml representation
        """

        assert self.__xml_serializer__ is not None, f"model {type(self).__name__} is partially initialized"

        root = XmlElement(tag=self.__xml_serializer__.element_name, nsmap=self.__xml_serializer__.nsmap)
        self.__xml_serializer__.serialize(
            root, self, pdc.to_jsonable_python(
                self,
                by_alias=False,
                fallback=lambda obj: obj if not isinstance(obj, ElementT) else None,  # for raw fields support
            ), skip_empty=skip_empty,
        )

        return root.to_native()

    def to_xml(self, *, skip_empty: bool = False, **kwargs: Any) -> Union[str, bytes]:
        """
        Serializes the object to an xml string.

        :param skip_empty: skip empty elements (elements without sub-elements, attributes and text, Nones)
        :param kwargs: additional xml serialization arguments
        :return: object xml representation
        """

        return etree.tostring(self.to_xml_tree(skip_empty=skip_empty), **kwargs)


RootModelRootType = TypeVar('RootModelRootType')


class RootXmlModel(
    RootModel[RootModelRootType],
    BaseXmlModel,
    Generic[RootModelRootType],
    __xml_abstract__=True,
):
    """
    Base pydantic-xml root model.
    """

    @classmethod
    def __build_serializer__(cls) -> None:
        if cls is RootXmlModel:
            return

        super().__build_serializer__()
