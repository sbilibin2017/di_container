from dataclasses import dataclass
from typing import NewType, Protocol

Interface = NewType("Interface", Protocol)
Implementation = NewType("Implementation", type)
RegistrationKey= NewType("RegistrationKey", str) 

@dataclass(frozen=True)
class RegistrationDTO:
    interface: Interface
    implementation: Implementation