Changelog
=========

2.2.3 (2023-09-20)
------------------

- raw element missing tail bug fixed. See https://github.com/dapper91/pydantic-xml/issues/118.


2.2.2 (2023-09-15)
------------------

- model validator 'before' mode support added.


2.2.1 (2023-09-12)
------------------

- model level `skip_empty` parameter added.
- wrapped element extra entities checking bugs fixed.


2.2.0 (2023-09-07)
------------------

- pydantic extra='forbid' parameter is being applied to xml elements too. See https://github.com/dapper91/pydantic-xml/pull/106.



2.1.0 (2023-08-24)
------------------

- raw element typed fields support added. See https://github.com/dapper91/pydantic-xml/issues/14.
- pydantic field exclude flag bug fixed (works only for serialization now).


2.0.0 (2023-08-19)
------------------

- library upgraded to pydantic version 2. See https://docs.pydantic.dev/2.0/migration/
- generic models are no longer inherited from BaseGenericXmlModel but from BaseXmlModel.
- custom root type declaration has been changed. It must inherit RootXmlModel from now on.
- encoding customization api has been changed. See https://pydantic-xml.readthedocs.io/en/v2.0.0/pages/misc.html#encoding
- element attributes can be bound to TypedDict. See https://pydantic-xml.readthedocs.io/en/v2.0.0/pages/data-binding/mappings.html#typed-dict
- tagged unions support added. See https://pydantic-xml.readthedocs.io/en/v2.0.0/pages/data-binding/unions.html#discriminated-unions
- computed entities support added. See https://pydantic-xml.readthedocs.io/en/v2.0.0/pages/misc.html#computed-entities


2.0.0b3 (2023-08-18)
--------------------

- decimal type support added.
- unparameterized root models serializer generation bug fixed. Affected by https://github.com/pydantic/pydantic/pull/7119.


2.0.0b2 (2023-08-06)
--------------------

- XmlModelMeta accepts ModelMetaclass directly. See https://github.com/dapper91/pydantic-xml/pull/90.


2.0.0b1 (2023-07-30)
--------------------

- tagged unions support added.


2.0.0a2 (2023-07-24)
--------------------

- pydantic validation context support added.


2.0.0a1 (2023-07-15)
--------------------

- library upgraded to pydantic version 2. See https://docs.pydantic.dev/2.0/migration/


1.0.0 (2023-07-14)
------------------

- library api stabilized
- custom root type serialization format changed.

0.7.0 (2023-06-24)
------------------

- from_xml, from_xml_tree methods return type bound to cls type. This resolves the problem with mypy checker.
  See https://github.com/dapper91/pydantic-xml/issues/65
- wrapped sub-elements serialization bug fixed. See https://github.com/dapper91/pydantic-xml/pull/70


0.6.3 (2023-06-19)
------------------

- forward refs support added. See https://github.com/dapper91/pydantic-xml/pull/61


0.6.2 (2023-06-10)
------------------

- piped union typehints support added. See https://github.com/dapper91/pydantic-xml/issues/56


0.6.1 (2023-04-15)
------------------

- model parameters inheritance bug fixed. See https://github.com/dapper91/pydantic-xml/issues/51


0.6.0 (2023-02-05)
------------------

- union types support added
- xml model encoding api unified with pydantic json encoding api
- root model validation raises exception instead of returning None
- xml model params inheritance implemented
- multiple element search strategies implemented


0.5.0 (2023-01-11)
------------------

- ipaddress objects serialization support added
- py.typed file added
- distutils dependency removed
- default namespace redefinition during serialization fixed (for lxml only). See https://github.com/dapper91/pydantic-xml/issues/27.


0.4.0 (2022-12-19)
------------------

- field default parameter support added.
- field default_factory parameter support added.
- root model validation added.
- pydantic field alias support implemented.


0.3.0 (2022-11-10)
------------------

- recursive (self-referencing) models support added.
- inherit_ns flag dropped due to recursive models implementation details.


0.2.2 (2022-10-07)
------------------

- attribute default namespace bug fixed.


0.2.1 (2022-10-06)
------------------

- default namespace support added.


0.2.0 (2022-08-19)
------------------

- generic models support
- namespace inheritance bug fixed.


0.1.0 (2022-08-17)
------------------

- Initial release
