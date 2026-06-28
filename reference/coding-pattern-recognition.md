# CODING PATTERN RECOGNITION

Use this reference for coding interview coaching, grading the Approach dimension, and designing
re-drills. The goal is to help the candidate infer a pattern from the problem's information needs,
not memorize algorithm names.

During a live mock, do not reveal this guide before the user's first attempt. If the candidate stalls,
use one interviewer-style nudge from the questions below. At Grade, use the guide fully to explain the
approach gap and re-drill on a novel variant.

## Core question

Start from:

```text
What information must I remember while scanning or building the answer?
```

Do not start from:

```text
Which algorithm do I know?
```

The pattern usually appears after the candidate identifies the state they must track.

## Solving scaffold

1. Restate the task in plain language.
2. Ask what must be remembered at each step.
3. Build the brute-force human method first.
4. Notice whether the brute-force method moves forward, revisits work, tracks counts, stores unresolved
   values, or explores choices.
5. Name the pattern only after the need is clear.
6. Code the smallest correct version.
7. Trace one normal case and one edge case.

## Detection questions

Use these questions before naming a pattern:

```text
1. What am I searching for?
2. Does order matter?
3. Do I need adjacency, or can I skip elements?
4. Do I need frequency counts?
5. Do I need previous values?
6. Do I need a range or window?
7. Do I need to try all possibilities?
8. Can I solve it by scanning once?
```

## Pattern signals

| Signal | Ask | Likely pattern |
|---|---|---|
| "in order", "relative order", "subsequence", "merge" | Do I walk through one or two inputs left to right? | Two pointers / subsequence scan |
| "pair", "sum", "two numbers" | For current value x, what previous value do I need? | HashMap; two pointers if sorted |
| "longest/shortest subarray/string", "at most k", "exactly k" | Can I expand and shrink a range? | Sliding window |
| "next greater", "previous smaller", "unresolved previous values" | What previous values are still waiting for an answer? | Stack / monotonic stack |
| "top k", "smallest k", "largest k" | Do I repeatedly need the best remaining item? | Heap / priority queue |
| "all combinations", "all paths", "choose or skip" | Do I need to try a choice and undo it? | Backtracking |
| "minimum ways", "maximum ways", "count ways", "can reach" | Does the answer depend on smaller subproblems? | Dynamic programming |

## Example: LeetCode 392 - Is Subsequence

Problem:

```text
Given s and t, check whether s is a subsequence of t.
```

Important clues:

```text
subsequence
delete characters
relative positions
```

These clues mean:

```text
Order matters.
Skipping is allowed.
Going backward is not allowed.
```

Plain restatement:

```text
Can I find all characters of s inside t, in order?
```

For:

```text
s = "abc"
t = "ahbgdc"
```

The candidate is not checking whether `"abc"` appears contiguously inside `t`. The candidate is asking:

```text
Can I find 'a', then later 'b', then later 'c'?
```

That suggests scanning.

## Minimum state for Is Subsequence

While scanning `t`, the candidate only needs to remember:

```text
Which character of s am I currently trying to match?
```

That is one pointer:

```java
int i = 0;
```

Meaning:

```text
I am currently looking for s.charAt(i).
```

Then scan `t` left to right. Move `i` only when the current `t` character matches the needed `s`
character.

## Human brute force to algorithm

Human method:

```text
Find a.
Then after that, find b.
Then after that, find c.
```

The search never moves backward in `t`, so the computer version is:

```text
move forward through t once
move forward through s only when matched
```

This is the two pointers / subsequence matching pattern.

## Is Subsequence algorithm

```text
i = current needed character in s
j = current scanned character in t

while scanning t:
    if t[j] equals s[i]:
        move i

return i reached the end of s
```

Complexity:

```text
time: O(length of t)
space: O(1)
```

## Interviewer nudges

Use one of these only if the candidate stalls:

- "What does relative order let you skip, and what does it forbid?"
- "What is the minimum state you need while scanning the larger string?"
- "If you found the first character, where is the earliest place the second character can be?"
- "Can you solve this without ever moving backward?"

## Grade signals

Strong Approach answer:

- Restates the problem as order-preserving search.
- Names that adjacency is not required.
- Explains that one pointer tracks the next needed character in `s`.
- Scans `t` once and advances the `s` pointer only on a match.
- Handles empty `s`, empty `t`, and `s` longer than `t`.

Weak Approach answer:

- Looks for a contiguous substring.
- Sorts characters, which destroys order.
- Counts frequency only, which misses order.
- Uses nested scans without explaining why it can be reduced to one pass.
- Names "two pointers" without explaining what each pointer tracks.

## Re-drill variants

Use a novel variant that tests the same dimension:

- Given two strings, verify whether one can be formed by deleting characters from the other.
- Merge two sorted arrays and explain what each pointer tracks.
- Check whether a typed string could be a long-pressed version of a name.
- Given a stream of characters, determine whether a target pattern has appeared as a subsequence so far.
