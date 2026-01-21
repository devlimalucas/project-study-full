import factory
from faker import Faker
from schemas import ProdutoCreate, UsuarioCreate

faker = Faker("pt_BR")  # gera dados mais realistas em português

class ProdutoFactory(factory.Factory):
    class Meta:
        model = ProdutoCreate

    nome = factory.LazyAttribute(lambda _: faker.pystr(min_chars=3, max_chars=15))
    preco = factory.LazyAttribute(lambda _: round(faker.pyfloat(left_digits=3, right_digits=2, positive=True), 2))
    estoque = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=100))
    descricao = factory.LazyAttribute(lambda _: faker.sentence(nb_words=6))

class UsuarioFactory(factory.Factory):
    class Meta:
        model = UsuarioCreate

    nome = factory.LazyAttribute(lambda _: faker.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())  # garante e-mails únicos
    senha = "123456"
    role = factory.Iterator(["cliente", "vendedor"])
