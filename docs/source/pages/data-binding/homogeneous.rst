.. _homogeneous:


Homogeneous collections
_______________________

Homogeneous collection is a collection of same type elements.
The most common homogeneous collections are :py:obj:`typing.List`, :py:obj:`typing.Set` and
variable-length tuple :py:obj:`typing.Tuple` (like ``Tuple[int, ...]``)


Primitive homogeneous collection
********************************

Field of a primitive homogeneous collection type marked as :py:func:`pydantic_xml.element` is bound
to sub-elements text.

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/homogeneous_primitives.py
            :language: python
            :start-after: model-start
            :end-before: model-end

    .. grid-item-card:: Document

        .. tab-set::

            .. tab-item:: XML

                .. literalinclude:: ../../../../examples/snippets/homogeneous_primitives.py
                    :language: xml
                    :lines: 2-
                    :start-after: xml-start
                    :end-before: xml-end

            .. tab-item:: JSON

                .. literalinclude:: ../../../../examples/snippets/homogeneous_primitives.py
                    :language: json
                    :lines: 2-
                    :start-after: json-start
                    :end-before: json-end


Model homogeneous collection
****************************

Field of a model homogeneous collection type is bound to sub-elements. Then the sub-element is used
as a root for that sub-model. For more information see :ref:`model data binding <pages/data-binding/models:model>`.
Parameter ``tag`` is used to declare sub-elements tag to which the sub-models are bound.
If it is omitted the sub-model ``tag`` parameter is used.
If it is omitted too field name is used (respecting ``pydantic`` field aliases).

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/homogeneous_models.py
            :language: python
            :start-after: model-start
            :end-before: model-end

    .. grid-item-card:: Document

        .. tab-set::

            .. tab-item:: XML

                .. literalinclude:: ../../../../examples/snippets/homogeneous_models.py
                    :language: xml
                    :lines: 2-
                    :start-after: xml-start
                    :end-before: xml-end

            .. tab-item:: JSON

                .. literalinclude:: ../../../../examples/snippets/homogeneous_models.py
                    :language: json
                    :lines: 2-
                    :start-after: json-start
                    :end-before: json-end


Dict homogeneous collection
***************************

Field of a mapping homogeneous collection type is bound to sub-elements attributes:

.. grid:: 2
    :gutter: 2

    .. grid-item-card:: Model

        .. literalinclude:: ../../../../examples/snippets/homogeneous_dicts.py
            :language: python
            :start-after: model-start
            :end-before: model-end

    .. grid-item-card:: Document

        .. tab-set::

            .. tab-item:: XML

                .. literalinclude:: ../../../../examples/snippets/homogeneous_dicts.py
                    :language: xml
                    :lines: 2-
                    :start-after: xml-start
                    :end-before: xml-end

            .. tab-item:: JSON

                .. literalinclude:: ../../../../examples/snippets/homogeneous_dicts.py
                    :language: json
                    :lines: 2-
                    :start-after: json-start
                    :end-before: json-end
