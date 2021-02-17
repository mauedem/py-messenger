from inject import Binder

from adapters.psql_database.repos import PsqlMessengerRepository
from core.repos import IMessengerRepository
from core.services import Service


def container(binder: Binder):
    # Сначала мы подаем интерфейс, а затем его реализацию
    binder.bind(IMessengerRepository, PsqlMessengerRepository())
    binder.bind(Service, Service())
