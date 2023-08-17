class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def consistent(self, assignment):
        for constraint in self.constraints:
            for variable in assignment:
                for neighbor in self.variables:
                    if variable == neighbor or neighbor not in assignment :
                        continue
                    if not constraint(assignment[variable], assignment[neighbor], variable, neighbor):
                        return False
            return True

    def check_assignment_complete(self, assignment):
        return len(self.variables) == len(assignment)

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable
        return None

    def backtrack(self, assignment):
        return backtrack(self, assignment)

def backtracking_search(csp):
    return csp.backtrack({})

def order_domain_values(var, assignment, csp):
    return csp.domains[var]


def backtrack(csp, assignment):
    if csp.check_assignment_complete(assignment):
        return assignment
    var = csp.select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment, csp):
        assignment[var] = value
        if csp.consistent(assignment):
            result = backtrack(csp, assignment)
            if result is not None:
                return result
        assignment.pop(var)
    return None


if __name__ == '__main__':
    four_queens_csp = CSP(
        variables=['q1', 'q2', 'q3', 'q4'],
        domains={q: [1, 2, 3, 4] for q in ['q1', 'q2', 'q3', 'q4']},
        constraints=[lambda q1, q2, q1_name, q2_name: q1 != q2 and abs(q1 - q2) != abs(int(q1_name[1]) - int(q2_name[1]))],
    )
    print(backtracking_search(four_queens_csp))