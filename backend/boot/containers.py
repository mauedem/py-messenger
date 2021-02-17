from inject import Binder

from adapters.local_database.repos import LocalMessengerRepository
from core.repos import IMessengerRepository
from core.services import Service


def container(binder: Binder):
    binder.bind(IMessengerRepository, LocalMessengerRepository())
    binder.bind(Service, Service())
