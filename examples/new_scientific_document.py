#!/usr/bin/env python3
"""
Generate a beautiful new scientific document using the WAFT simple template.

This creates a comprehensive technical report on computational complexity
and algorithmic efficiency.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.simple_scientific import generate_simple_scientific_document

# Document content - comprehensive technical report
CONTENT = """
<h2>1. Introduction</h2>

<p>
Computational complexity theory provides the mathematical foundation for understanding
the efficiency and limitations of algorithms. As computational problems grow in scale
and complexity, the ability to analyze and optimize algorithmic performance becomes
increasingly critical for modern software systems.
</p>

<p>
This report examines fundamental concepts in computational complexity, including
time and space complexity analysis, Big O notation, and the classification of
problems into complexity classes. We explore practical applications of complexity
theory in algorithm design and optimization.
</p>

<h2>2. Theoretical Foundations</h2>

<h3>2.1 Time Complexity</h3>

<p>
Time complexity describes how the execution time of an algorithm grows as a function
of input size. The most common notation is Big O, which provides an upper bound on
growth rate. Common complexity classes include:
</p>

<ul>
    <li><strong>O(1)</strong> - Constant time: Accessing an array element</li>
    <li><strong>O(log n)</strong> - Logarithmic: Binary search</li>
    <li><strong>O(n)</strong> - Linear: Iterating through an array</li>
    <li><strong>O(n log n)</strong> - Linearithmic: Efficient sorting algorithms</li>
    <li><strong>O(n²)</strong> - Quadratic: Nested loops, bubble sort</li>
    <li><strong>O(2ⁿ)</strong> - Exponential: Recursive Fibonacci</li>
</ul>

<h3>2.2 Space Complexity</h3>

<p>
Space complexity measures the amount of memory an algorithm requires relative to
input size. This includes both auxiliary space (temporary variables) and input space.
Understanding space complexity is crucial for memory-constrained environments.
</p>

<h3>2.3 Complexity Classes</h3>

<p>
The P vs NP problem represents one of the most important open questions in computer
science. Problems in P can be solved in polynomial time, while NP problems have
solutions that can be verified in polynomial time. Whether P = NP remains unresolved.
</p>

<h2>3. Algorithmic Analysis</h2>

<h3>3.1 Sorting Algorithms</h3>

<p>
Sorting provides an excellent case study for complexity analysis. Different
algorithms exhibit vastly different performance characteristics:
</p>

<table>
    <caption>Table 1: Sorting Algorithm Complexity Comparison</caption>
    <tr>
        <th>Algorithm</th>
        <th>Best Case</th>
        <th>Average Case</th>
        <th>Worst Case</th>
        <th>Space</th>
    </tr>
    <tr>
        <td>Bubble Sort</td>
        <td>O(n)</td>
        <td>O(n²)</td>
        <td>O(n²)</td>
        <td>O(1)</td>
    </tr>
    <tr>
        <td>Quick Sort</td>
        <td>O(n log n)</td>
        <td>O(n log n)</td>
        <td>O(n²)</td>
        <td>O(log n)</td>
    </tr>
    <tr>
        <td>Merge Sort</td>
        <td>O(n log n)</td>
        <td>O(n log n)</td>
        <td>O(n log n)</td>
        <td>O(n)</td>
    </tr>
    <tr>
        <td>Heap Sort</td>
        <td>O(n log n)</td>
        <td>O(n log n)</td>
        <td>O(n log n)</td>
        <td>O(1)</td>
    </tr>
</table>

<h3>3.2 Search Algorithms</h3>

<p>
Search algorithms demonstrate the power of algorithmic optimization. Linear search
requires O(n) time in the worst case, while binary search achieves O(log n) by
exploiting sorted data structures.
</p>

<h2>4. Practical Implementation</h2>

<h3>4.1 Example: Binary Search</h3>

<p>
The following implementation demonstrates an efficient binary search algorithm:
</p>

<pre><code>def binary_search(arr, target):
    # Perform binary search on a sorted array
    # Time Complexity: O(log n)
    # Space Complexity: O(1)
    # Args: arr (sorted list), target (element to find)
    # Returns: Index of target if found, -1 otherwise

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1</code></pre>

<h3>4.2 Example: Merge Sort</h3>

<p>
Merge sort provides guaranteed O(n log n) performance through divide-and-conquer:
</p>

<pre><code>def merge_sort(arr):
    # Sort array using merge sort algorithm
    # Time Complexity: O(n log n) - guaranteed
    # Space Complexity: O(n) - auxiliary array
    # Args: arr (list to sort)
    # Returns: Sorted list

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    # Merge two sorted lists
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result</code></pre>

<h2>5. Optimization Strategies</h2>

<h3>5.1 Memoization</h3>

<p>
Memoization trades space for time by caching computed results. This technique
dramatically improves performance for recursive algorithms with overlapping
subproblems, such as dynamic programming solutions.
</p>

<h3>5.2 Data Structure Selection</h3>

<p>
Choosing appropriate data structures significantly impacts algorithm efficiency.
Hash tables provide O(1) average-case lookups, while balanced trees offer
O(log n) worst-case guarantees. The choice depends on access patterns and
constraints.
</p>

<h3>5.3 Algorithmic Paradigms</h3>

<p>
Common algorithmic paradigms include:
</p>

<ul>
    <li><strong>Divide and Conquer:</strong> Break problem into subproblems (e.g., merge sort)</li>
    <li><strong>Dynamic Programming:</strong> Solve overlapping subproblems efficiently</li>
    <li><strong>Greedy Algorithms:</strong> Make locally optimal choices</li>
    <li><strong>Backtracking:</strong> Explore solution space systematically</li>
</ul>

<h2>6. Real-World Applications</h2>

<h3>6.1 Database Query Optimization</h3>

<p>
Database systems rely heavily on complexity analysis to optimize query execution.
Index selection, join algorithms, and query planning all depend on understanding
computational complexity.
</p>

<h3>6.2 Network Routing</h3>

<p>
Routing algorithms in computer networks must balance efficiency with correctness.
Shortest path algorithms like Dijkstra's algorithm (O(V²) or O(E + V log V) with
priority queue) enable efficient packet routing.
</p>

<h3>6.3 Machine Learning</h3>

<p>
Training machine learning models involves optimizing complex objective functions.
Understanding the computational complexity of optimization algorithms helps
design scalable learning systems.
</p>

<h2>7. Challenges and Limitations</h2>

<h3>7.1 Worst-Case vs Average-Case</h3>

<p>
Algorithm analysis often focuses on worst-case complexity, but average-case
performance may be more relevant for practical applications. Understanding
both perspectives provides a complete picture.
</p>

<h3>7.2 Hidden Constants</h3>

<p>
Big O notation ignores constant factors, which can be significant in practice.
An O(n) algorithm with large constants may perform worse than an O(n log n)
algorithm for small inputs.
</p>

<h3>7.3 Modern Hardware Considerations</h3>

<p>
Cache locality, parallelization, and modern CPU features can significantly
affect real-world performance. Theoretical complexity analysis provides
guidance but must be validated through empirical testing.
</p>

<h2>8. Conclusion</h2>

<p>
Computational complexity theory provides essential tools for understanding
algorithmic efficiency. By analyzing time and space complexity, we can make
informed decisions about algorithm selection and optimization strategies.
</p>

<p>
As computational problems continue to grow in scale, the principles of complexity
theory remain fundamental to building efficient, scalable software systems.
Continued research in complexity theory will drive advances in algorithm design
and computational capabilities.
</p>

<h2>9. Future Directions</h2>

<p>
Emerging areas of research include quantum complexity theory, approximation
algorithms for NP-hard problems, and complexity analysis of parallel and
distributed algorithms. These directions will shape the future of computational
efficiency.
</p>
"""


def main():
    """Generate the scientific document."""
    output_dir = Path("_work_efforts/showcase_documents")
    output_path = output_dir / "Computational_Complexity_Analysis.pdf"

    # Generate document
    pdf_path = generate_simple_scientific_document(
        title="Computational Complexity and Algorithmic Efficiency: A Comprehensive Analysis",
        content=CONTENT,
        output_path=output_path,
        authors=["Dr. Sarah Chen", "Prof. Michael Rodriguez", "Dr. Emily Watson"],
        date=datetime.now().strftime("%B %Y"),
        abstract=(
            "This report provides a comprehensive analysis of computational complexity "
            "theory and its applications in algorithm design. We examine fundamental "
            "concepts including time and space complexity, Big O notation, and complexity "
            "class classifications. Through detailed analysis of sorting and search algorithms, "
            "we demonstrate practical applications of complexity theory. The report explores "
            "optimization strategies, real-world applications in databases and networking, "
            "and addresses challenges in complexity analysis. Our findings highlight the "
            "critical importance of computational complexity theory for building efficient, "
            "scalable software systems."
        ),
        references=[
            "[1] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms (4th ed.). MIT Press.",
            "[2] Sipser, M. (2012). Introduction to the Theory of Computation (3rd ed.). Cengage Learning.",
            "[3] Knuth, D. E. (1997). The Art of Computer Programming, Volume 1: Fundamental Algorithms (3rd ed.). Addison-Wesley.",
            "[4] Kleinberg, J., & Tardos, É. (2005). Algorithm Design. Pearson.",
            "[5] Papadimitriou, C. H. (1994). Computational Complexity. Addison-Wesley.",
            "[6] Arora, S., & Barak, B. (2009). Computational Complexity: A Modern Approach. Cambridge University Press.",
            "[7] Dasgupta, S., Papadimitriou, C., & Vazirani, U. (2006). Algorithms. McGraw-Hill.",
            "[8] Skiena, S. S. (2008). The Algorithm Design Manual (2nd ed.). Springer.",
        ],
        short_title="Computational Complexity Analysis",
    )

    print(f"✅ Generated: {pdf_path}")
    print(f"   Size: {pdf_path.stat().st_size:,} bytes")
    print(f"   Location: {pdf_path.absolute()}")

    return pdf_path


if __name__ == "__main__":
    pdf_path = main()

    # Open the PDF
    import platform
    import subprocess

    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", str(pdf_path)])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", str(pdf_path)])
    elif platform.system() == "Windows":
        subprocess.run(["start", str(pdf_path)], shell=True)

    print("\n📄 Document opened in your default PDF viewer!")
