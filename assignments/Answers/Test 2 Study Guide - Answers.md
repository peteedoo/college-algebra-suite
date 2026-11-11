# Test 2 Study Guide — Complete Step-by-Step Solutions
**Course:** MAT 1340 College Algebra  
**Covers:** Chapter 1.8, Chapter 3 (3.1, 3.2, 3.3, 3.4, 3.5, 3.6)

---

### Question 1 (1.8): Absolute Value Equation |2x - 4| = 8
* **Problem:** Solve the absolute value equation $|2x - 4| = 8$, write the solution in set notation, and graph.
* **Answers:**
  * Solution Set: **`{-2, 6}`**
* **The Rule:** An absolute value equation $|u| = k$ (where $k > 0$) splits into two linear equations: $u = k$ or $u = -k$.
* **Step-by-Step Work:**
  1. Set up cases: $2x - 4 = 8$ or $2x - 4 = -8$.
  2. Case 1: $2x = 12 \implies x = 6$.
  3. Case 2: $2x = -4 \implies x = -2$.
  4. Number Line Graph: Solid closed dots at $x = -2$ and $x = 6$.
* **Tip:** Always check both answers in the original equation: $|2(6) - 4| = |8| = 8$ and $|2(-2) - 4| = |-8| = 8$.

---

### Question 2 (1.8): Absolute Value Inequality |4x - 6| > 9
* **Problem:** Solve $|4x - 6| > 9$, write in interval notation, and graph.
* **Answers:**
  * Interval: **`(-∞, -3/4) U (15/4, ∞)`**
* **The Rule:** The "great-OR" inequality $|u| > k$ splits into a disjoint union: $u < -k$ or $u > k$.
* **Step-by-Step Work:**
  1. $4x - 6 < -9$ or $4x - 6 > 9$.
  2. $4x < -3 \implies x < -3/4$.
  3. $4x > 15 \implies x > 15/4$.
  4. Number Line Graph: Shade left of $-3/4$ with open parenthesis and shade right of $15/4$ with open parenthesis.
* **Tip:** Because the inequality is strictly $>$, use parentheses `( )`, not square brackets `[ ]`.

---

### Question 3 (1.8): Absolute Value Inequality |1 - 2x| < 5
* **Problem:** Solve $|1 - 2x| < 5$, write in interval notation, and graph.
* **Answers:**
  * Interval: **`(-2, 3)`**
* **The Rule:** The "less-AND" inequality $|u| < k$ becomes a three-part compound inequality: $-k < u < k$.
* **Step-by-Step Work:**
  1. $-5 < 1 - 2x < 5$.
  2. Subtract 1: $-6 < -2x < 4$.
  3. Divide by $-2$ (flip signs!): $3 > x > -2$, which is $-2 < x < 3$.
  4. Number Line Graph: Open parentheses at $-2$ and $3$, shaded in between.
* **Tip:** Whenever you multiply or divide an inequality by a negative number, remember to reverse the inequality signs!

---

### Question 4 (1.8): Absolute Value Equation |x - 6| = |2x - 6|
* **Problem:** Solve $|x - 6| = |2x - 6|$, write in set notation, and graph.
* **Answers:**
  * Solution Set: **`{0, 4}`**
* **The Rule:** An equation with two absolute values $|u| = |v|$ splits into $u = v$ or $u = -v$.
* **Step-by-Step Work:**
  1. Case 1: $x - 6 = 2x - 6 \implies -6 = x - 6 \implies x = 0$.
  2. Case 2: $x - 6 = -(2x - 6) \implies x - 6 = -2x + 6 \implies 3x = 12 \implies x = 4$.
  3. Graph: Closed points at $x = 0$ and $x = 4$.
* **Tip:** Check: $|0 - 6| = |-6| = 6$ and $|2(0) - 6| = |-6| = 6$ (true). $|4 - 6| = |-2| = 2$ and $|2(4) - 6| = |2| = 2$ (true).

---

### Question 5 (1.8): Special Cases (No Solution vs Infinite Solutions)
* **Problem:** Explain why each has either no solution or infinite solutions:
  i. $|x - 2| = -3$
  ii. $|2x| < -1$
  iii. $|x + 3| > -1$
* **Answers:**
  * i. **No Solution (∅)** — Distance is always non-negative ($|x - 2| \ge 0$); it can never equal $-3$.
  * ii. **No Solution (∅)** — $|2x| \ge 0$ for all real $x$, so it can never be strictly less than $-1$.
  * iii. **Infinite Solutions (-∞, ∞)** — Absolute value is always $\ge 0 > -1$ for every real number.

---

### Question 6 (3.1): Quadratic Function Graphing f(x) = 2x^2 - 8x - 12
* **Problem:** Graph $f(x) = 2x^2 - 8x - 12$:
  (i) Find the vertex
  (ii) Find the x- and y-intercepts
  (iii) Determine which way the graph opens and state why
* **Answers:**
  * (i) Vertex: **`(2, -20)`**
  * (ii) y-intercept: **`(0, -12)`** | x-intercepts: **`(2 + √10, 0) ≈ (5.16, 0)`** and **`(2 - √10, 0) ≈ (-1.16, 0)`**
  * (iii) Direction of Opening: **Opens upward** because $a = 2 > 0$ (minimum at vertex).
* **Step-by-Step Work:**
  1. $V_x = -\frac{b}{2a} = -\frac{-8}{2(2)} = 2$.
  2. $V_y = f(2) = 2(2)^2 - 8(2) - 12 = 8 - 16 - 12 = -20$.
  3. y-intercept: $f(0) = -12$.
  4. x-intercepts: $2(x^2 - 4x - 6) = 0 \implies x = \frac{4 \pm \sqrt{16 - 4(1)(-6)}}{2} = \frac{4 \pm \sqrt{40}}{2} = 2 \pm \sqrt{10}$.
  5. Axis of symmetry: $x = 2$.

---

### Question 7 (3.1): Vertex by Completing the Square
* **Problem:** Find the vertex of each parabola by completing the square:
  a. $f(x) = x^2 - 6x + 4$
  b. $f(x) = x^2 - 8x + 4$
* **Answers:**
  * a. Vertex: **`(3, -5)`** | Vertex form: **`f(x) = (x - 3)^2 - 5`**
  * b. Vertex: **`(4, -12)`** | Vertex form: **`f(x) = (x - 4)^2 - 12`**
* **Step-by-Step Work:**
  * Part a: $(b/2)^2 = (-6/2)^2 = 9$. Add/subtract 9: $y = (x^2 - 6x + 9) + 4 - 9 = (x - 3)^2 - 5 \implies V(3, -5)$.
  * Part b: $(b/2)^2 = (-8/2)^2 = 16$. Add/subtract 16: $y = (x^2 - 8x + 16) + 4 - 16 = (x - 4)^2 - 12 \implies V(4, -12)$.

---

### Question 8 (3.1): Projectile Motion Application
* **Problem:** An object is launched upward at 96 ft/sec: $S(t) = -16t^2 + 96t$. Find:
  i. Maximum height
  ii. Time to reach maximum height
  iii. Time when height is 128 feet
  iv. Time to hit the ground
* **Answers:**
  * i. Maximum Height: **`144 feet`**
  * ii. Time to Max Height: **`3 seconds`**
  * iii. Times at 128 ft: **`t = 2 seconds`** (upward) and **`t = 4 seconds`** (downward)
  * iv. Time to Hit Ground: **`6 seconds`**
* **Step-by-Step Work:**
  * Time at vertex: $t = -\frac{b}{2a} = -\frac{96}{2(-16)} = 3$ sec.
  * Max height: $S(3) = -16(9) + 96(3) = 144$ ft.
  * For $S(t) = 128$: $-16t^2 + 96t - 128 = 0 \implies -16(t - 2)(t - 4) = 0 \implies t = 2, 4$ sec.
  * For $S(t) = 0$: $-16t(t - 6) = 0 \implies t = 0$ (launch) or $t = 6$ sec (landing).

---

### Question 9 (3.1): Parabola Equation from Point and Vertex
* **Problem:** Find the stretch factor $a$ and equation of the parabola with vertex $(1, -1)$ containing $(2, 3)$.
* **Answers:**
  * Stretch factor: **`a = 4`**
  * Equation: **`y = 4(x - 1)^2 - 1`**
* **Step-by-Step Work:**
  1. Vertex form: $y = a(x - h)^2 + k = a(x - 1)^2 - 1$.
  2. Substitute $(2, 3)$: $3 = a(2 - 1)^2 - 1 \implies 3 = a(1) - 1 \implies a = 4$.

---

### Question 10 (3.3): Rational Zero Theorem
* **Problem:** Determine all possible rational zeros for $f(x) = 3x^4 - 7x^3 - 6x^2 + 12x + 8$.
* **Answers:**
  * Possible Rational Zeros: **`±1, ±2, ±4, ±8, ±1/3, ±2/3, ±4/3, ±8/3`**
* **The Rule:** By the Rational Zero Theorem, all possible rational zeros are $\pm \frac{p}{q}$ where $p$ divides the constant term 8, and $q$ divides the leading coefficient 3.

---

### Question 11 (3.3): Finding All Zeros (Real and Complex)
* **Problem:** Find all zeros for $f(x) = 2x^3 - 5x^2 - x + 6$.
* **Answers:**
  * All Zeros: **`x = -1, 3/2, 2`**
  * Factored Form: **`f(x) = (x + 1)(2x - 3)(x - 2)`**
* **Step-by-Step Work:**
  1. Test $x = -1$: $f(-1) = 2(-1) - 5(1) - (-1) + 6 = -2 - 5 + 1 + 6 = 0$.
  2. Synthetic division with $c = -1$: $[2, -5, -1, 6] \to [2, -7, 6 | 0]$.
  3. Depressed quadratic: $2x^2 - 7x + 6 = (2x - 3)(x - 2) = 0 \implies x = 3/2, 2$.

---

### Question 12 (3.3): Polynomial from Given Zeros and Point
* **Problem:** Find lowest-degree polynomial with real coefficients having zeros $-1, 1, i$ and $f(0) = 3$.
* **Answers:**
  * Polynomial: **`f(x) = -3x^4 + 3`** (or `-3(x^4 - 1)`)
* **Step-by-Step Work:**
  1. Conjugate Zeros Theorem: Because coefficients are real, $-i$ must also be a zero. Zeros are $-1, 1, i, -i$.
  2. Factored form: $f(x) = a(x + 1)(x - 1)(x - i)(x + i) = a(x^2 - 1)(x^2 + 1) = a(x^4 - 1)$.
  3. Use $f(0) = 3$: $a(0 - 1) = -a = 3 \implies a = -3$.
  4. Expand: $f(x) = -3(x^4 - 1) = -3x^4 + 3$.

---

### Question 13 (3.4): Graphing Polynomial Functions
* **Problem:** Graph $f(x) = 3x^4 - 7x^3 - 6x^2 + 12x + 8$:
  (1) y-intercept, (2) zeros and multiplicities, (3) prototype / end behavior.
* **Answers:**
  * y-intercept: **`(0, 8)`**
  * Zeros: **`x = -1` (mult. 1, crosses)**, **`x = -2/3` (mult. 1, crosses)**, **`x = 2` (mult. 2, touches/bounces)**
  * Factored form: **`f(x) = (x + 1)(3x + 2)(x - 2)^2`**
  * End Behavior: Leading term $3x^4$ (even degree, positive) $\implies$ rises left and rises right (↖ ↗).

---

### Question 14 (3.5): Rational Function with a Hole
* **Problem:** Analyze and graph $f(x) = \frac{x - 2}{x^2 - x - 2}$.
* **Answers:**
  * Simplified: **`f(x) = \frac{1}{x + 1}`** (for $x \ne 2$)
  * Hole: **`(2, 1/3)`**
  * Vertical Asymptote: **`x = -1`**
  * Horizontal Asymptote: **`y = 0`**
  * x-intercept: **None** (numerator has no zeros)
  * y-intercept: **`(0, 1)`**
* **The Rule:** Factors that cancel from both numerator and denominator create removable discontinuities (HOLES), NOT vertical asymptotes.

---

### Question 15 (3.5): Rational Function with Two Vertical Asymptotes
* **Problem:** Analyze and graph $f(x) = \frac{x - 2}{x^2 - 1}$.
* **Answers:**
  * Vertical Asymptotes: **`x = -1`** and **`x = 1`**
  * Horizontal Asymptote: **`y = 0`** (degree 1 < degree 2)
  * Holes: **None**
  * x-intercept: **`(2, 0)`**
  * y-intercept: **`(0, 2)`**

---

### Question 16 (3.5): Rational Function with Nonzero Horizontal Asymptote
* **Problem:** Analyze and graph $f(x) = \frac{x - 2}{2x + 1}$.
* **Answers:**
  * Vertical Asymptote: **`x = -1/2`**
  * Horizontal Asymptote: **`y = 1/2`** (degrees equal: ratio of leading coefficients $1/2$)
  * Holes: **None**
  * x-intercept: **`(2, 0)`**
  * y-intercept: **`(0, -2)`**

---

### Question 17 (3.5): Rational Function with Oblique (Slant) Asymptote
* **Problem:** Analyze and graph $f(x) = \frac{x^2 - 9}{x + 1}$.
* **Answers:**
  * Oblique / Slant Asymptote: **`y = x - 1`**
  * Vertical Asymptote: **`x = -1`**
  * Horizontal Asymptote: **None**
  * Holes: **None**
  * x-intercepts: **`(-3, 0)`** and **`(3, 0)`**
  * y-intercept: **`(0, -9)`**
* **Step-by-Step Work:**
  * Degree of numerator (2) is exactly 1 higher than denominator (1) $\implies$ Slant Asymptote!
  * Divide: $(x^2 - 9) \div (x + 1) = (x - 1)$ with remainder $-8$.
  * As $x \to \pm\infty$, remainder $-\frac{8}{x + 1} \to 0$, so graph approaches the line $y = x - 1$.

---

### Question 18 (3.6): Polynomial Inequality x^2 - 6x > 27
* **Problem:** Solve $x^2 - 6x > 27$ in interval notation and graph.
* **Answers:**
  * Solution: **`(-∞, -3) U (9, ∞)`**
* **Step-by-Step Work:**
  1. Move 27 over: $x^2 - 6x - 27 > 0$.
  2. Factor: $(x - 9)(x + 3) > 0$.
  3. Boundary points: $x = -3, 9$.
  4. Test intervals:
     * $(-\infty, -3)$: test $x = -4 \implies (-13)(-1) = +13 > 0$ (YES)
     * $(-3, 9)$: test $x = 0 \implies (-9)(3) = -27 < 0$ (NO)
     * $(9, \infty)$: test $x = 10 \implies (1)(13) = +13 > 0$ (YES)
  5. Number Line Graph: Shade left of $-3$ and right of $9$ with open parentheses.

---

### Question 19 (3.6): Rational Inequality (3x - 1)/(3x + 3) < 6
* **Problem:** Solve $\frac{3x - 1}{3x + 3} < 6$ in interval notation.
* **Answers:**
  * Solution: **`(-∞, -19/15) U (-1, ∞)`**
* **Step-by-Step Work:**
  1. Subtract 6: $\frac{3x - 1}{3x + 3} - 6 < 0 \implies \frac{3x - 1 - 18x - 18}{3x + 3} < 0 \implies \frac{-15x - 19}{3x + 3} < 0$.
  2. Critical points: Numerator $= 0 \implies x = -19/15 \approx -1.27$; Denominator $= 0 \implies x = -1$.
  3. Test intervals:
     * $(-\infty, -19/15)$: Negative (YES)
     * $(-19/15, -1)$: Positive (NO)
     * $(-1, \infty)$: Negative (YES)
  4. Note: $x = -1$ must have an open parenthesis because the denominator cannot be 0.
