# Sorting Algorithm Recommendation Guide

## Quick Reference Decision Tree

```
                    Start Here
                        │
                        ▼
              Is n > 10,000?
              /           \
           Yes             No
            │               │
            ▼               ▼
      Use Merge Sort    Is n > 1,000?
                        /         \
                     Yes           No
                      │             │
                      ▼             ▼
               Is data mostly    Is n > 50?
               sorted?           /       \
               /     \        Yes         No
            Yes       No       │           │
             │         │       ▼           ▼
             ▼         ▼   Is data     Use Insertion
       Use Insertion  Use  mostly     Sort for
       Sort          Merge sorted?    simplicity
                     Sort  /    \
                        Yes     No
                         │       │
                         ▼       ▼
                   Insertion   Merge
                   Sort        Sort
```

## At-a-Glance Recommendations

### By Data Size

| Dataset Size | Primary Choice | When to Use Alternative |
|-------------|----------------|------------------------|
| **n ≤ 50** | Insertion Sort | Merge Sort if stability is critical |
| **50 < n ≤ 1,000** | Merge Sort | Insertion Sort if data is mostly sorted |
| **1,000 < n ≤ 10,000** | Merge Sort | Only Merge Sort is practical |
| **n > 10,000** | Merge Sort | No practical alternative |

### By Data Characteristics

| Data Pattern | Best Algorithm | Why |
|-------------|----------------|-----|
| **Random/Unknown** | Merge Sort | Consistent O(n log n) performance |
| **Already Sorted** | Insertion Sort | O(n) best case |
| **Reverse Sorted** | Merge Sort | O(n²) algorithms are worst case |
| **Partially Sorted** | Insertion Sort | Exploits existing order |
| **Streaming Data** | Insertion Sort | Online algorithm, maintains order |

### By Constraints

| Constraint | Best Algorithm | Why |
|-----------|----------------|-----|
| **Limited Memory** | Insertion Sort | O(1) space complexity |
| **Write-Expensive Storage** | Selection Sort | Minimizes swaps (≤ n-1) |
| **Need Stability** | Merge Sort | Guaranteed stable |
| **Predictable Performance** | Merge Sort | Always O(n log n) |
| **Simplicity** | Insertion Sort | Easiest to implement correctly |

## Performance Reference Table

### Execution Times (seconds) from Our Benchmarks

#### Random Data
| n | Bubble | Selection | Insertion | Merge |
|---|--------|-----------|-----------|-------|
| 1,000 | 0.027 | 0.012 | 0.010 | **0.001** |
| 5,000 | 0.774 | 0.356 | 0.325 | **0.007** |
| 10,000 | 3.125 | 1.354 | 1.232 | **0.023** |
| 50,000 | - | - | - | **0.086** |

#### Sorted Data (Best Case)
| n | Bubble | Selection | Insertion | Merge |
|---|--------|-----------|-----------|-------|
| 1,000 | **0.000** | 0.013 | **0.000** | 0.001 |
| 5,000 | **0.000** | 0.333 | **0.000** | 0.005 |
| 10,000 | **0.001** | 1.624 | **0.001** | 0.012 |

#### Reverse Sorted Data (Worst Case for Some)
| n | Bubble | Selection | Insertion | Merge |
|---|--------|-----------|-----------|-------|
| 1,000 | 0.035 | 0.014 | 0.024 | **0.001** |
| 5,000 | 0.928 | 0.363 | 0.598 | **0.006** |
| 10,000 | 4.454 | 1.592 | 2.207 | **0.010** |

## Algorithm Complexity Summary

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |

## Red Flags: When NOT to Use

### Never Use Bubble Sort When:
- n > 100 elements
- Performance matters
- This is production code

### Never Use Selection Sort When:
- Data might already be sorted
- Stability is required
- n > 5,000 elements

### Never Use Insertion Sort When:
- n > 10,000 elements
- Data is reverse sorted
- Worst-case performance matters

### Be Cautious with Merge Sort When:
- Memory is severely constrained
- n < 50 (simpler algorithms have less overhead)
- Working with linked lists (consider iterative merge sort)

## Common Patterns in Practice

### Pattern 1: Small, Frequently Updated Lists (UI dropdowns, autocomplete)
```
Recommendation: Insertion Sort
Reason: Low overhead, excellent for maintaining sorted order
as new items are added
```

### Pattern 2: Large Dataset, One-Time Sort (database query results)
```
Recommendation: Merge Sort (or Timsort)
Reason: Predictable O(n log n), handles any input well
```

### Pattern 3: Embedded System with Limited RAM
```
Recommendation: Insertion Sort for small data, Heapsort for larger
Reason: Both are O(1) space; Insertion is simpler for small n
```

### Pattern 4: External Sorting (data larger than memory)
```
Recommendation: External Merge Sort
Reason: Natural fit for disk-based sorting with sequential access
```

### Pattern 5: Nearly Sorted Log Files
```
Recommendation: Insertion Sort or Timsort
Reason: Both exploit existing order for O(n) performance
```

## Final Checklist

Before choosing an algorithm, ask:

1. **What's my data size?** → If n > 1000, probably Merge Sort
2. **What's my data distribution?** → If sorted/nearly sorted, consider Insertion Sort
3. **Do I need stability?** → Eliminates Selection Sort
4. **What's my memory budget?** → If tight, use in-place algorithms
5. **What's my performance requirement?** → If worst-case matters, use Merge Sort
6. **Am I sorting repeatedly with small changes?** → Insertion Sort maintains order well

---

*Generated from Sorting Algorithm Comparison Tool*
*See ANALYSIS.md for detailed explanations and benchmark methodology*
