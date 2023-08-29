class CSP:
    def __init__(self, variable_dict, constraints):
        self.variable_dict = variable_dict
        self.constraints = constraints

    def consistent(self, assignment):
        for constraint in self.constraints:
            for variable in assignment:
                for neighbor in self.variable_dict.keys():
                    if variable == neighbor or neighbor not in assignment:
                        continue
                    if not constraint(assignment[variable], assignment[neighbor], variable, neighbor):
                        return False
            return True

    def check_assignment_complete(self, assignment):
        return len(self.variable_dict.keys()) == len(assignment)

    def select_unassigned_variable(self, assignment):
        for variable in self.variable_dict.keys():
            if variable not in assignment:
                return variable
        return None

    def backtrack(self, assignment):
        return backtrack(self, assignment)

    def inference(self, assignment):
        new_domains = dict()
        for var in self.variable_dict.keys():
            inference_domain = []
            if var in assignment:
                continue
            for value in self.variable_dict[var]:
                assignment[var] = value
                if self.consistent(assignment):
                    inference_domain.append(value)
                assignment.pop(var)
            if len(inference_domain) == 0:
                return None
            new_domains[var] = inference_domain
        return new_domains

    def update(self, inferences):
        old_domains = self.variable_dict.copy()
        for var in inferences:
            self.variable_dict[var] = inferences[var]
        return old_domains

    def restore(self, old_domains):
        self.variable_dict = old_domains


def backtracking_search(csp):
    return csp.backtrack({})


def order_domain_values(var, assignment, csp):
    return csp.variable_dict[var]


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
        variable_dict={'q1': [1, 2, 3, 4], 'q2': [1, 2, 3, 4], 'q3': [1, 2, 3, 4], 'q4': [1, 2, 3, 4]},
        constraints=[lambda q1, q2, q1_name, q2_name: q1 != q2 and abs(q1 - q2) != abs(int(q1_name[1]) - int(q2_name[1]))],
    )
    print(backtracking_search(four_queens_csp))