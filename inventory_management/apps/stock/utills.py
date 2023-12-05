from abc import ABC, abstractmethod


class Converter(ABC):

    @abstractmethod
    def convert(self, bulk):
        """Converts an ect"""


class GToKg(Converter):

    def convert(self, bulk):
        return bulk / 1000


class GToMg(Converter):

    def convert(self, bulk):
        return bulk * 1000


class MgToKg(Converter):

    def convert(self, bulk):
        return bulk / 1000000


class MgToG(Converter):

    def convert(self, bulk):
        return bulk / 1000


class KgToG(Converter):

    def convert(self, bulk):
        return bulk * 1000


class KgToMg(Converter):

    def convert(self, bulk):
        return bulk * 1000000


class MlToL(Converter):

    def convert(self, bulk):
        return bulk / 1000


class LToML(Converter):

    def convert(self, bulk):
        return bulk * 1000


CONVERTOR = {2: GToKg, 3: MgToKg, 5: MlToL}

# CONVERTOR_FOR_UNIT = {(1, 2): KgToG, (2, 1): GToKg, (2, 3): GToMg, (3, 2): MgToG, (3, 1): MgToKg, (1, 3): KgToMg,
                      # (4, 5): LToML, (5, 4): MlToL}
