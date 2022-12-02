from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)

    @classmethod
    def default(cls):
        return list(cls)[0].name

    @classmethod
    def get(cls, payload: str):
        return next(
            iter(
                filter(
                    lambda el: getattr(el, 'name') == payload
                    or getattr(el, 'value') == payload,
                    cls,
                )
            )
        )
