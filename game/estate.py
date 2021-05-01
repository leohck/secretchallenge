class Estate:
    """
    Propriedade
    """

    def __init__(self, id_, price):
        """
        :param id_: ID da propriedade
        :param price: Valor da propriedade
        :attr sale_price: Preço de Venda
        :attr rent_price: Preço do aluguel
        :attr owner: Proprietário (Player)
        """
        self.__id_ = id_
        self.__owner = None
        self.price = price

    @property
    def id_(self):
        return self.__id_

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        assert value > 0, "The Price must be greater than zero"
        self._price = value
        self.__sale_price = self.price
        self.__rent_price = self.sale_price / 4

    @property
    def sale_price(self):
        return self.__sale_price

    @property
    def rent_price(self):
        return self.__rent_price

    @property
    def owner(self):
        return self.__owner

    def change_owner(self, new_owner):
        self.__owner = new_owner

    def __str__(self):
        return f'ID: {self.__id_} | SALE PRICE: R$ {self.sale_price} | RENT PRICE: R$ {self.rent_price} | OWNER ID: {self.owner.id_ if self.owner else "No Owner"}'

    def __repr__(self):
        return f'Estate ({self.__id_})'
