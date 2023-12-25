from typing import Callable
from .dtos.registration import RegistrationDTO, RegistrationKey, Interface, Implementation
from .utils.validate_signature import validate_signature
from inspect import signature
from functools import wraps

class DIContainer:    
    __deps: dict[RegistrationKey, RegistrationDTO] = {}
    
    @validate_signature
    def register(
        self,
        name: str, 
        interface: Interface,
        implementation: Implementation,
    ) -> None:
        self.__deps[name]: dict[str, RegistrationDTO] = RegistrationDTO(
            interface=interface,
            implementation=implementation,
        ) 
        
    def resolve(self, name: str) -> Implementation:        
        dep_implementation = self._get_dependency_implementation(name)
        dep_interface = self._get_dependency_interface(name)
        subdeps_interface: dict[str, Protocol] = self._get_subdependencies_interface(dep_implementation)          
        subdeps_implementation: dict[str, Implementation] = {}
        if subdeps_interface is not None:     
            for name, interface in subdeps_interface.items():                   
                subdep_implementation = self.resolve(name)                
                subdeps_implementation[name] = subdep_implementation
        return dep_implementation(**subdeps_implementation)
    
    def _get_dependency_implementation(self, name: str) -> Implementation:
        return self.__deps.get(name).implementation
    
    def _get_dependency_interface(self, name: str) -> Interface:
        return self.__deps.get(name).interface    
    
    def _get_subdependencies_interface(self, implementation: Implementation):
        return signature(implementation).parameters
    
    @property
    def dependencies(self):
        return list(self.__deps.keys())    
    
    
def inject(container: DIContainer):  
    def inner(func: Callable):    
        annotations = func.__annotations__        
        parameters = signature(func).parameters
        dependencies_name = container.dependencies
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, param in parameters.items():
                if (name in annotations) and (name not in kwargs) and (name in dependencies_name) :                      
                    kwargs[name] = container.resolve(name)        
            return func(*args, **kwargs)
        return wrapper
    return inner


    

