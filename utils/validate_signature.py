from utils.di_container.dtos.member import MemberDTO
from utils.di_container.dtos.registration import Interface, Implementation
from inspect import getmembers       
        
def _get_members(obj: Interface | Implementation) -> list[MemberDTO]:
    interface_members = getmembers(obj)    
    members: list[MemberDTO] = []
    for m in interface_members:
        m1 = m[0].startswith("__")
        m2 = m[0].endswith("__")   
        m3 = "protocol" not in m[0]     
        m4 = "_abc_impl" not in m[0]        
        if ~m1 & ~m2 & m3 & m4:            
            name = m[0]
            subfunc = m[1]            
            members.append(
                MemberDTO(
                    name=name, 
                    signature=signature(subfunc)
                )  
            )  
    return members


class InterfaceImplementationNotMatch(Exception):
    def __init__(self, interface_members: list[MemberDTO], implementation_members: list[MemberDTO]): 
        message:str = f"Interface does not match Implementation signature:\n\t"
        for interface, implementation in zip(interface_members, implementation_members):
            if interface!=implementation:
                message += f"{interface} <-> {implementation}\n\t"
        super().__init__(message)

                    
def validate_signature(func):
    def inner(*args, **kwargs):        
        interface = kwargs.get("interface")
        implementation = kwargs.get("implementation")    
        interface_members = _get_members(interface)
        implementation_members = _get_members(implementation)
        if not (interface_members==implementation_members):
            raise InterfaceImplementationNotMatch(interface_members, implementation_members)
        return func(*args, **kwargs)
    return inner