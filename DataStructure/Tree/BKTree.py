class BKTree:
    def __init__(self):
        self.root = None

    class Node:
        def __init__(self, term):
            self.term = term
            self.children = {}

    def add(self, term):
        if self.root is None:
            self.root = self.Node(term)
        else:
            node = self.root # Create a temp root to compare with term
            while True:
                distance = self.levenshtein_distance(term, node.term) # Calculate distance from term to node.term
                if distance in node.children: # If distance exist in root distance
                    node = node.children[distance] # assign node to next node
                else:
                    node.children[distance] = self.Node(term) 
                    break

    def search(self, term, max_distance):
        candidates = [self.root] # Stack for DFS Algorithsm
        results = []

        while candidates:
            node = candidates.pop()
            distance = self.levenshtein_distance(term, node.term)
            if distance <= max_distance:
                results.append(node.term)
            low, high = distance - max_distance, distance + max_distance
            candidates.extend(
                child for dist, child in node.children.items()
                if low <= dist <= high
            )

        return results

    def levenshtein_distance(self, a, b):
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

        return dp[m][n]

# # Usage
# data = ["apple", "apply", "banana", "bandana", "orange"]
# bk_tree = BKTree(levenshtein_distance)
# for item in data:
#     bk_tree.add(item)

# query = "aple"
# max_distance = 2
# results = bk_tree.search(query, max_distance)
# print(results)  # Output should include ["apple", "apply"]
