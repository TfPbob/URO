class DomainError(Exception):
    """Базовый класс для доменных ошибок"""
    pass


class StateError(DomainError):
    """Ошибка при переходе состояния ресурса"""
    pass


class ConfigError(DomainError):
    """Ошибка при выборе неправильного конфига"""
    pass

class ResourceNotFound(DomainError):
    """Ошибка при отсутствии необходимого ресурса на сервере"""
    pass
