from collections import defaultdict

# cost of modules

def cost_of_modules(lines):
    graph = defaultdict(list)
    all_nodes = []

    for line in lines:
        nodes = line.split(',')
        all_nodes.append(nodes[0])
        for node in nodes[1:]:
            graph[node].append(nodes[0])

    res = []
    for node in all_nodes:
        visited = defaultdict(bool)
        stack = []
        cost_of_modules_utils(node, visited, stack, graph)
        res.append((node, len(stack)))
    return res


def _cost_of_modules_utils(node, visited, stack, graph):
    visited[node] = True
    for n in graph[node]:
        if not visited[n]:
            cost_of_modules_utils(n, visited, stack, graph)
    stack.append(node)


if __name__ == '__main__':
    # a depends on s, e, n
    # s depends on h , n 
    #e depends on n
    # h does not depend on any module
    # n does not depend on any module
    ip = [
        'a,s,e,n',
        's,h,n',
        'e,n',
        'h',
        'n'

    ]
    print(cost_of_modules(ip))
