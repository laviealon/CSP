class CSP:
    """

    Attributes:
        - variable_dict: A dictionary mapping variable names to their domains.
        - constraints: EITHER a dictionary mapping tuples of variables to a constraint function.
            Each function takes two values and returns True if they satisfy the constraint and False otherwise.
    """
    def __init__(self, variable_dict, constraints):
        self.variable_dict = variable_dict
        self.constraints = constraints

    def consistent(self, assignment):
        """Checks if an assignment is consistent with the constraints of the CSP."""
        for variable in assignment:
            for var_pair in self.constraints.keys():
                if variable in var_pair:
                    l = list(var_pair)
                    if l[0] not in assignment or l[1] not in assignment:
                        continue
                    if not self.constraints[var_pair](assignment[l[0]], assignment[l[1]]):
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


def order_domain_values(var, csp):
    return csp.variable_dict[var]


def backtrack(csp: CSP, assignment):
    """Backtracking search.

    :param csp: A constraint satisfaction problem
    :param assignment: A partial assignment to the variables of csp allowing for recursive backtracking

    :return: A complete assignment to the variables of csp or None if no assignment is found
    """
    if csp.check_assignment_complete(assignment):
        return assignment
    var = csp.select_unassigned_variable(assignment)
    for value in order_domain_values(var, csp):
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


def _revise(csp, x, y):
    revised = False
    for v in csp.variable_dict[x]:
        if all([not csp.constraints[frozenset([x, y])](v, w) for w in csp.variable_dict[y]]):
            csp.variable_dict[x].remove(v)
            revised = True
    return revised


def ac3(csp: CSP):
    # add all arcs to queue
    queue = [(x, y) for x in csp.variable_dict.keys() for y in csp.variable_dict.keys() if x != y]
    while len(queue) > 0:
        queue_item = queue.pop(0)
        if _revise(csp, queue_item[0], queue_item[1]):
            if len(csp.variable_dict[queue_item[0]]) == 0:
                return False
            for neighbor in csp.variable_dict.keys():
                if neighbor == queue_item[0] or neighbor == queue_item[1]:
                    continue
                queue.append((neighbor, queue_item[0]))
    return True


if __name__ == '__main__':
    four_queens_csp = CSP(
        variable_dict={'q1': [1, 2, 3, 4], 'q2': [1, 2, 3, 4], 'q3': [1, 2, 3, 4], 'q4': [1, 2, 3, 4]},
        constraints={
            frozenset(['q1', 'q2']): lambda x, y: x != y and abs(x - y) != 1,
            frozenset(['q1', 'q3']): lambda x, y: x != y and abs(x - y) != 2,
            frozenset(['q1', 'q4']): lambda x, y: x != y and abs(x - y) != 3,
            frozenset(['q2', 'q3']): lambda x, y: x != y and abs(x - y) != 1,
            frozenset(['q2', 'q4']): lambda x, y: x != y and abs(x - y) != 2,
            frozenset(['q3', 'q4']): lambda x, y: x != y and abs(x - y) != 1,
        })
    print(backtracking_search(four_queens_csp))
    print(ac3(four_queens_csp))