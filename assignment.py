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

    def inference(self, assignment):
        new_domains = dict()
        for var in self.variables:
            inference_domain = []
            if var in assignment:
                continue
            for value in self.domains[var]:
                assignment[var] = value
                if self.consistent(assignment):
                    inference_domain.append(value)
                assignment.pop(var)
            if len(inference_domain) == 0:
                return None
            new_domains[var] = inference_domain
        return new_domains

    def update(self, inferences):
        old_domains = self.domains.copy()
        for var in inferences:
            self.domains[var] = inferences[var]
        return old_domains

    def restore(self, old_domains):
        self.domains = old_domains


def backtracking_search(csp):
    return csp.backtrack({})

def order_domain_values(var, assignment, csp):
    return csp.domains[var]


def backtrack(csp: CSP, assignment):
    if csp.check_assignment_complete(assignment):
        return assignment
    var = csp.select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment, csp):
        assignment[var] = value
        inferences = csp.inference(assignment)
        if inferences is not None:
            old_domains = csp.update(inferences)
        if csp.consistent(assignment):
            result = backtrack(csp, assignment)
            if result is not None:
                return result
        assignment.pop(var)
        if inferences is not None:
            csp.restore(old_domains)
    return None


if __name__ == '__main__':
    four_queens_csp = CSP(
        variables=['q1', 'q2', 'q3', 'q4'],
        domains={q: [1, 2, 3, 4] for q in ['q1', 'q2', 'q3', 'q4']},
        constraints=[lambda q1, q2, q1_name, q2_name: q1 != q2 and abs(q1 - q2) != abs(int(q1_name[1]) - int(q2_name[1]))],
    )
    print(backtracking_search(four_queens_csp))