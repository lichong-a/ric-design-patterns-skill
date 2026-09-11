from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class _Settings:
    mode: str

# Module-scoped instance: conventional Python expression of shared configuration.
_SETTINGS = _Settings("production")

def settings() -> _Settings:
    return _SETTINGS


if __name__ == "__main__":
    assert settings() is settings()
    assert settings().mode == "production"
    print("OK singleton")
