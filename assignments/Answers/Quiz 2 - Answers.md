# Quiz 2 — Complete Step-by-Step Solutions
**Course:** MAT 1340 College Algebra  
**Topic:** Polynomial Functions, Graphing, Zeros, and Inequalities

---

### Question 1: Polynomial Function Analysis & Graphing: f(x) = x^3 + x^2 - 36x - 36
* **Problem:** For the polynomial $f(x) = x^3 + x^2 - 36x - 36$:
  1. Determine the parent function.
  2. Find all possible zeros (Rational Zero Test) and all zeros using synthetic division.
  3. Express the polynomial in factored form and decide whether the graph crosses or touches at each zero.
  4. Find the y-intercept.
  5. Graph the function, labeling all zeros and the y-intercept in $(x,y)$ coordinates.
* **Answers:**
  * Parent Function: **`y = x^3`** (Cubic prototype, falls left and rises right: $\swarrow \nearrow$)
  * Possible Rational Zeros: **`±1, ±2, ±3, ±4, ±6, ±9, ±12, ±18, ±36`**
  * All Zeros: **`x = -1, -6, 6`**
  * Factored Form: **`f(x) = (x + 1)(x + 6)(x - 6)`**
  * Multiplicity & Behavior:
    * At $x = -1$ (multiplicity 1, odd): **Crosses** the x-axis
    * At $x = -6$ (multiplicity 1, odd): **Crosses** the x-axis
    * At $x = 6$ (multiplicity 1, odd): **Crosses** the x-axis
  * y-intercept: **`(0, -36)`**
* **The Rule:**
  * Factoring by grouping: $x^2(x + 1) - 36(x + 1) = (x^2 - 36)(x + 1) = (x - 6)(x + 6)(x + 1)$.
  * Multiplicity rule: Odd multiplicity $\implies$ graph crosses the x-axis; Even multiplicity $\implies$ graph touches the x-axis and turns around.
* **Step-by-Step Work:**
  1. Parent function is highest degree term: $y = x^3$. Since degree is 3 (odd) and $a = 1 > 0$, end behavior is falls left, rises right.
  2. By grouping: $x^3 + x^2 - 36x - 36 = x^2(x + 1) - 36(x + 1) = (x^2 - 36)(x + 1) = (x - 6)(x + 6)(x + 1) = 0$.
  3. Zeros: $x = -1, -6, 6$. All have multiplicity 1, so the curve crosses at all three x-intercepts: $(-6,0)$, $(-1,0)$, and $(6,0)$.
  4. y-intercept: $f(0) = 0 + 0 - 0 - 36 = -36 \implies (0, -36)$.
  5. Local extrema: Relative maximum between $x = -6$ and $x = -1$; relative minimum between $x = -1$ and $x = 6$.

---

### Question 2: Polynomial Inequality x^3 - 3x - 2 < 0
* **Problem:** Find the interval(s) where $x^3 - 3x - 2 < 0$.
* **Answers:**
  * Interval: **`(-∞, -1) U (-1, 2)`** (or $(-\infty, 2)$ excluding $x = -1$)
* **The Rule:** Factor the polynomial to find boundary zeros, test signs in each interval, and select regions with negative signs ($< 0$).
* **Step-by-Step Work:**
  1. Test $x = -1$: $(-1)^3 - 3(-1) - 2 = -1 + 3 - 2 = 0$. So $(x + 1)$ is a factor.
  2. Synthetic division with $c = -1$: $[1, 0, -3, -2] \to [1, -1, -2 | 0]$.
  3. Depressed quadratic: $x^2 - x - 2 = (x - 2)(x + 1)$.
  4. Factored form: $(x + 1)^2(x - 2) < 0$.
  5. Boundary zeros: $x = -1$ (multiplicity 2) and $x = 2$ (multiplicity 1).
  6. Test intervals:
     * $(-\infty, -1)$: test $x = -2 \implies (-1)^2(-4) = -4 < 0$ (YES)
     * $(-1, 2)$: test $x = 0 \implies (1)^2(-2) = -2 < 0$ (YES)
     * $(2, \infty)$: test $x = 3 \implies (4)^2(1) = +16 > 0$ (NO)
  7. Note: At $x = -1$, the expression equals $0$, which is not strictly $< 0$.
  8. Solution interval: **`(-∞, -1) U (-1, 2)`**.

---

### Question 3: Rational Inequality (x - 2)/(x + 3) > 1
* **Problem:** Find the interval(s) where $\frac{x - 2}{x + 3} > 1$.
* **Answers:**
  * Interval: **`(-∞, -3)`**
* **The Rule:** Never multiply both sides by $(x + 3)$ because its sign depends on $x$! Subtract 1 to get $0$ on the right, find a common denominator, and test intervals.
* **Step-by-Step Work:**
  1. $\frac{x - 2}{x + 3} - 1 > 0$.
  2. Combine: $\frac{(x - 2) - (x + 3)}{x + 3} = \frac{-5}{x + 3} > 0$.
  3. Boundary points: Numerator $-5$ has no zeros; Denominator $x + 3 = 0 \implies x = -3$.
  4. Test intervals:
     * $(-\infty, -3)$: test $x = -4 \implies \frac{-5}{-4 + 3} = \frac{-5}{-1} = +5 > 0$ (YES)
     * $(-3, \infty)$: test $x = 0 \implies \frac{-5}{0 + 3} = -\frac{5}{3} < 0$ (NO)
  5. Solution interval: **`(-∞, -3)`**.
