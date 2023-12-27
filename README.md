```
from typing import Protocol
from functools import cache

class IRepository(Protocol):
    def say_hello(self) -> str:
        ...
        
class Repository1:
    def say_hello(self) -> str:
        return "hello from repository1"
    
class Repository2:
    def say_hello(self) -> str:
        return "hello from repository2"
    
class IService(Protocol):
    @property
    def repository1(self) -> IRepository:
        ...
        
    @repository1.setter
    def repository1(self) -> IRepository:
        ...
        
    @property
    def repository2(self) -> IRepository:
        ...
        
    @repository2.setter
    def repository2(self) -> IRepository:
        ...
        
    def say_hello(self):
        ...
        
        
class Service:
    def __init__(self, repository1: IRepository, repository2: IRepository):
        self.repository1=repository1
        self.repository2=repository2
    
    def say_hello(self):
        h1 = self.repository1.say_hello()
        h2 = self.repository2.say_hello()
        return f"{h1}, {h2}"

# конфигурирование контейнера со всеми зависимостями
di_container = DIContainer()
di_container.register("repository1", IRepository, Repository1)
di_container.register("repository2", IRepository, Repository2)
di_container.register("service", IService, Service)

# инициализация приложения
app = FastAPI()

# прикрепление di-контейнера к инстансу приложения
app.state.di_container = di_container

# зависимость FastAPI(кешируем зависимость для реализации синглтона)
@cache
def get_service(app: FastAPI()) -> IService:
    return app.state.di_container.resolve("service")

# роутер
@router("/")
async def get_data(
    service: IService = Depends(get_service)
) -> ResponseSchema:
    data = await service.get_data()
    return ResponseSchema(data=data, status: HTTPStatus.OK)
```
