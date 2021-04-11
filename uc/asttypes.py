from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional, Tuple, Union
from ply.yacc import YaccProduction


def set_terminal_lineinfo(p: YaccProduction, sym: int = 1) -> Tuple[int, int]:
    line, index = p.lineno(sym), p.lexpos(sym)
    p.set_lineno(0, line)
    p.set_lexpos(0, index)
    return line, index


# # # # # # # #
# EXPRESSIONS #

class Expression:
    ...


@dataclass(frozen=True)
class AssignExpr(Expression):
    item: Expression
    value: Expression


@dataclass(frozen=True)
class CallExpr(Expression):
    item: Expression
    args: List[Expression]


@dataclass(frozen=True)
class AccessExpr(Expression):
    item: Expression
    at: Expression


@dataclass(frozen=True)
class UnOp(Expression):
    op: Operator
    item: Expression


@dataclass(frozen=True)
class BinOp(Expression):
    op: Operator
    left: Expression
    right: Expression


# # # # # # # # # # #
# TERMINAL  SYMBOLS #

class TerminalSymbol(Expression):
    @classmethod
    def from_token(cls, p: YaccProduction) -> TerminalSymbol:
        info = set_terminal_lineinfo(p)
        return cls(cls.parse(p[1]), info)

    @classmethod
    @property
    def symbol(cls) -> str:
        return cls.__name__

    @classmethod
    def parse(cls, text):
        return text

    def __str__(self) -> str:
        return str(self.value)

    def __value__(self):
        return self.value

    def __repr__(self) -> str:
        value = self.__value__()
        return f"{self.symbol}::{value}"


@unique
class TypeSpec(TerminalSymbol, Enum):
    VOID = "void"
    CHAR = "char"
    INT = "int"

    @classmethod
    def from_token(cls, p: YaccProduction) -> TypeSpec:
        set_terminal_lineinfo(p)
        return cls(p[1])


@dataclass(frozen=True, repr=False)
class Int(TerminalSymbol):
    value: int
    position: Tuple[int, int]

    @classmethod
    def __parse__(cls, text: str) -> int:
        return int(text)


@dataclass(frozen=True, repr=False)
class Char(TerminalSymbol):
    value: str
    position: Tuple[int, int]

    @classmethod
    def __parse__(cls, text: str) -> str:
        return text.strip("'")

    def __value__(self) -> str:
        return f"'{self.value}'"


@dataclass(frozen=True, repr=False)
class Ident(TerminalSymbol):
    value: str
    position: Tuple[int, int]


@dataclass(frozen=True, repr=False)
class String(TerminalSymbol):
    value: str
    position: Tuple[int, int]

    def __value__(self) -> str:
        return repr(self.value)


@dataclass(frozen=True, repr=False)
class Operator(TerminalSymbol):
    value: str

    @classmethod
    def from_token(cls, p: YaccProduction, *, set_info=True) -> TypeSpec:
        if set_info:
            set_terminal_lineinfo(p)
        return cls(p[1])
