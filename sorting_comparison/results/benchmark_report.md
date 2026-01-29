# Sorting Algorithm Performance Comparison

*Generated: 2026-01-29 18:37:23*

## Performance Results

### Random

| Algorithm | Size | Mean Time | Std Dev |
|-----------|------|-----------|---------|
| Merge Sort | 1000 | 0.001164s | 0.000033s |
| Insertion Sort | 1000 | 0.009960s | 0.000437s |
| Selection Sort | 1000 | 0.012285s | 0.000040s |
| Bubble Sort | 1000 | 0.027078s | 0.000271s |
| Merge Sort | 5000 | 0.007129s | 0.000596s |
| Insertion Sort | 5000 | 0.324962s | 0.019558s |
| Selection Sort | 5000 | 0.356148s | 0.024875s |
| Bubble Sort | 5000 | 0.773754s | 0.052870s |
| Merge Sort | 10000 | 0.022614s | 0.005697s |
| Insertion Sort | 10000 | 1.231970s | 0.102684s |
| Selection Sort | 10000 | 1.353833s | 0.072713s |
| Bubble Sort | 10000 | 3.124556s | 0.185165s |
| Merge Sort | 50000 | 0.085455s | 0.002217s |

### Sorted

| Algorithm | Size | Mean Time | Std Dev |
|-----------|------|-----------|---------|
| Bubble Sort | 1000 | 0.000041s | 0.000001s |
| Insertion Sort | 1000 | 0.000065s | 0.000002s |
| Merge Sort | 1000 | 0.000850s | 0.000007s |
| Selection Sort | 1000 | 0.013390s | 0.001257s |
| Bubble Sort | 5000 | 0.000186s | 0.000004s |
| Insertion Sort | 5000 | 0.000282s | 0.000007s |
| Merge Sort | 5000 | 0.004514s | 0.000098s |
| Selection Sort | 5000 | 0.332711s | 0.009847s |
| Bubble Sort | 10000 | 0.000580s | 0.000050s |
| Insertion Sort | 10000 | 0.000609s | 0.000016s |
| Merge Sort | 10000 | 0.011993s | 0.001264s |
| Selection Sort | 10000 | 1.624083s | 0.110543s |
| Merge Sort | 50000 | 0.056940s | 0.004506s |

### Reverse Sorted

| Algorithm | Size | Mean Time | Std Dev |
|-----------|------|-----------|---------|
| Merge Sort | 1000 | 0.000836s | 0.000059s |
| Selection Sort | 1000 | 0.013913s | 0.001492s |
| Insertion Sort | 1000 | 0.023583s | 0.001779s |
| Bubble Sort | 1000 | 0.034634s | 0.001270s |
| Merge Sort | 5000 | 0.005742s | 0.000313s |
| Selection Sort | 5000 | 0.363406s | 0.010605s |
| Insertion Sort | 5000 | 0.597628s | 0.022501s |
| Bubble Sort | 5000 | 0.928413s | 0.057997s |
| Merge Sort | 10000 | 0.010015s | 0.000094s |
| Selection Sort | 10000 | 1.592358s | 0.060775s |
| Insertion Sort | 10000 | 2.207137s | 0.091948s |
| Bubble Sort | 10000 | 4.453627s | 0.092783s |
| Merge Sort | 50000 | 0.055267s | 0.000625s |

### Partially Sorted

| Algorithm | Size | Mean Time | Std Dev |
|-----------|------|-----------|---------|
| Merge Sort | 1000 | 0.001198s | 0.000144s |
| Insertion Sort | 1000 | 0.001621s | 0.000063s |
| Selection Sort | 1000 | 0.013839s | 0.001586s |
| Bubble Sort | 1000 | 0.020640s | 0.000275s |
| Merge Sort | 5000 | 0.005831s | 0.000053s |
| Insertion Sort | 5000 | 0.033468s | 0.000723s |
| Selection Sort | 5000 | 0.332526s | 0.012798s |
| Bubble Sort | 5000 | 0.581263s | 0.025206s |
| Merge Sort | 10000 | 0.013079s | 0.000373s |
| Insertion Sort | 10000 | 0.144209s | 0.003924s |
| Selection Sort | 10000 | 1.303824s | 0.011841s |
| Bubble Sort | 10000 | 1.878770s | 0.116170s |
| Merge Sort | 50000 | 0.076209s | 0.000392s |

## Best Algorithm per Scenario

| Size | random | sorted | reverse_sorted | partially_sorted |
|------|---|---|---|---|
| 1000 | Merge Sort | Bubble Sort | Merge Sort | Merge Sort |
| 5000 | Merge Sort | Bubble Sort | Merge Sort | Merge Sort |
| 10000 | Merge Sort | Bubble Sort | Merge Sort | Merge Sort |
| 50000 | Merge Sort | Merge Sort | Merge Sort | Merge Sort |