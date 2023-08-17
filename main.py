from __future__ import annotations
from typing import List, Dict, Union, Optional


class Variable:
    name: str
    value: Optional[int]
    domain: List[Union[int, str]]

    def __init__(self, name: str, domain: List[Union[int, str]]) -> None:
        self.name = name
        self.domain = domain
        self.value = None

    def is_assigned(self) -> bool:
        return self.value is not None


class CSP:
    variables: List[Variable]
    initial_domain: List[Union[int, str]]
    _constraints: List[callable]

    def check_assignment_complete(self) -> bool:
        return all([var.is_assigned() for var in self.variables])

    def backtracking_search(self):
        return self.backtrack({})

    def select_unassigned_variable(self) -> Variable:
        return next(var for var in self.variables if not var.is_assigned())

    def consistent(self, assignment: Dict[str, Union[int, str]]) -> bool:
        return all(constraint(assignment) for constraint in self._constraints)

    def backtrack(self, assignment: Dict[str, Union[int, str]]):
        if self.check_assignment_complete():
            return assignment
        var = self.select_unassigned_variable()
        for value in var.domain:
            assignment[var.name] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var.name)
        return None

if __name__ == '__main__':
