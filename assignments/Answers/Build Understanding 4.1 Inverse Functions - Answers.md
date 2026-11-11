# Answer Sheet: Build Understanding 4.1 Inverse Functions

**Course:** MAT1340003 College Algebra: MA1 (Steven Yamiolkoski) FA26  
**Assignment:** Build Understanding 4.1 Inverse Functions  

---

### **Question 1**
* **Problem:** Determine whether or not the function is one-to-one: $f(x) = x^3 - 8$.
* **Answer:** **`One-to-one`**
* **Graph Equation:** `f(x) = x^3 - 8`
* **The Rule:** A function $f$ is one-to-one if $f(a) = f(b) \implies a = b$. Odd power functions $x^3 + c$ are strictly increasing and therefore one-to-one.
* **Work:**
  * Set $a^3 - 8 = b^3 - 8 \implies a^3 = b^3 \implies a = b$. Thus, the function is **One-to-one**.

---

### **Question 2**
* **Problem:** Determine whether or not the function is one-to-one: $f(x) = x^2 + 12$.
* **Answer:** **`Not one-to-one`**
* **Graph Equation:** `f(x) = x^2 + 12`
* **The Rule:** Quadratic functions with unrestricted domains fail the horizontal line test because $f(-x) = f(x)$.
* **Work:**
  * Notice that $f(1) = 1^2 + 12 = 13$ and $f(-1) = (-1)^2 + 12 = 13$. Two different inputs give the same output, so it is **Not one-to-one**.

---

### **Question 3**
* **Problem:** Determine whether or not the function is one-to-one: $f(x) = -(x + 4)^2$.
* **Answer:** **`Not one-to-one`**
* **Graph Equation:** `f(x) = -(x + 4)^2`
* **The Rule:** Any parabola opening up or down fails the horizontal line test on $(-\infty, \infty)$.
* **Work:**
  * Pick two inputs symmetric around the vertex $x = -4$: $f(-3) = -(-3 + 4)^2 = -1$ and $f(-5) = -(-5 + 4)^2 = -1$. Since $f(-3) = f(-5)$, it is **Not one-to-one**.

---

### **Question 4**
* **Problem:** Determine whether or not the function is one-to-one: $h(x) = \frac{1}{9}x - \frac{8}{9}$.
* **Answer:** **`One-to-one`**
* **Graph Equation:** `h(x) = (1/9)x - 8/9`
* **The Rule:** Any linear function $h(x) = mx + b$ with a non-zero slope ($m \neq 0$) is strictly monotonic and one-to-one.
* **Work:**
  * The slope is $m = \frac{1}{9} \neq 0$. Setting $\frac{1}{9}a - \frac{8}{9} = \frac{1}{9}b - \frac{8}{9}$ yields $a = b$. Thus, it is **One-to-one**.

---

### **Question 5**
* **Problem:** Decide whether the function is one-to-one: $y = \frac{-1}{x + 8}$.
* **Answer:** **`Yes`**
* **Graph Equation:** `y = -1 / (x + 8)`
* **The Rule:** Reciprocal functions of the form $y = \frac{a}{x - h} + k$ ($a \neq 0$) pass the horizontal line test and are one-to-one.
* **Work:**
  * Assume $\frac{-1}{a + 8} = \frac{-1}{b + 8}$. Cross-multiplying gives $-(b + 8) = -(a + 8) \implies a = b$. Thus, **Yes**, it is one-to-one.

---

### **Question 6**
* **Problem:** Determine whether the function is one-to-one: $y = 4|x + 4|$.
* **Answer:** **`The function is not one-to-one. At least one horizontal line intersects the graph of the function more than once.`** (Choice 3)
* **Graph Equation:** `y = 4 * abs(x + 4)`
* **The Rule:** Absolute value graphs are V-shaped, so any horizontal line above the vertex intersects the graph twice.
* **Work:**
  * For example, at $y = 4$, $4|x + 4| = 4 \implies x = -3$ or $x = -5$. Because a horizontal line intersects the graph more than once, the function is not one-to-one.

---

### **Question 7**
* **Problem:** Determine whether or not the function is one-to-one: $f(x) = 4$.
* **Answer:** **`Not one-to-one`**
* **Graph Equation:** `f(x) = 4`
* **The Rule:** A constant function $f(x) = c$ is a horizontal line; every $x$-value produces the exact same $y$-value.
* **Work:**
  * Since $f(0) = 4$ and $f(1) = 4$, infinitely many inputs share the output $4$. Thus, it is **Not one-to-one**.

---

### **Question 8**
* **Problem:** Decide whether the function is one-to-one: $y = 9x - 3$.
* **Answer:** **`Yes`**
* **Graph Equation:** `y = 9x - 3`
* **The Rule:** A linear function with non-zero slope ($m = 9 \neq 0$) is one-to-one.
* **Work:**
  * $9a - 3 = 9b - 3 \implies 9a = 9b \implies a = b$. Thus, **Yes**.

---

### **Question 9**
* **Problem:** Decide whether the function is one-to-one: $y = 2(x + 3)^2 - 6$.
* **Answer:** **`No`**
* **Graph Equation:** `y = 2(x + 3)^2 - 6`
* **The Rule:** A quadratic function (parabola) is not one-to-one on $(-\infty, \infty)$.
* **Work:**
  * At $x = -2$ and $x = -4$, $y = 2(1) - 6 = -4$. Two distinct $x$-values give the same $y$-value, so **No**.

---

### **Question 11**
* **Problem:** Is the function one-to-one? Use the horizontal line test on the given downward-sloping line graph.
* **Answer:** **`Yes`**
* **Graph Equation:** `y = -6x + 8`
* **The Rule:** Horizontal Line Test: If every horizontal line intersects the graph at most once, the function is one-to-one.
* **Work:**
  * The graph is a non-horizontal straight line. Every horizontal line crosses it exactly once, so **Yes**.

---

### **Question 12**
* **Problem:** Is the function one-to-one? Use the horizontal line test on the given exponential curve graph.
* **Answer:** **`Yes`**
* **Graph Equation:** `y = 3^x`
* **The Rule:** Strictly increasing exponential curves pass the horizontal line test.
* **Work:**
  * Every horizontal line intersects the curve at most once, so **Yes**.

---

### **Question 13**
* **Problem:** Is the function one-to-one? Use the horizontal line test on the given symmetric cusp/root graph ($y = |x|^{1/2}$ or $x^{2/3}$).
* **Answer:** **`No`**
* **Graph Equation:** `y = abs(x)^(1/2)`
* **The Rule:** If any horizontal line intersects the graph in more than one point, the function is not one-to-one.
* **Work:**
  * Any horizontal line above the $x$-axis ($y > 0$) intersects both the left branch and the right branch of the graph (two points). Thus, **No**.

---

### **Question 14**
* **Problem:** Decide whether the function graphed (a steep line passing through $(0, -6)$ and $(2, 4)$) is one-to-one.
* **Answer:** **`Yes`**
* **Graph Equation:** `y = 5x - 6`
* **The Rule:** Non-horizontal lines pass the horizontal line test.
* **Work:**
  * No horizontal line intersects the line more than once, so **Yes**.

---

### **Question 15**
* **Problem:** Determine whether the function graphed (a downward-opening parabola with vertex at $(-1, 6)$) is one-to-one.
* **Answer:** **`Choice C: No, there is a horizontal line that intersects the graph at more than one point.`**
* **Graph Equation:** `y = -2(x + 1)^2 + 6`
* **The Rule:** A parabola fails the horizontal line test because horizontal lines below the vertex intersect the graph twice.
* **Work:**
  * For example, the horizontal line $y = 4$ intersects the parabola at $(0, 4)$ and $(-2, 4)$. Therefore, **Choice C** is correct.

---

### **Question 16**
* **Problem:** The graph of a function $f$ is given (a cubic curve decreasing through $(-2, 2), (0, -2), (1, -3)$). Use the horizontal-line test to determine whether $f$ is one-to-one.
* **Answer:** **`Yes`**
* **Graph Equation:** `f(x) = -0.5x^3 - 2`
* **The Rule:** A strictly decreasing function passes the horizontal line test everywhere.
* **Work:**
  * Every horizontal line intersects the curve at exactly one point, so **Yes**.

---

### **Question 17**
* **Problem:** Determine whether the function defined is one-to-one: $f(x) = \sqrt{32 - x^2}$.
* **Answer:** **`Choice A: No, because the two x-values 2 and -2 correspond to same f(x) value` `2\sqrt{7}`**
* **Graph Equation:** `f(x) = sqrt(32 - x^2)`
* **The Rule:** If $f(2) = f(-2)$, the function is not one-to-one. Simplify radicals completely.
* **Work:**
  * Evaluate at $x = 2$ and $x = -2$:
  * $f(2) = \sqrt{32 - 2^2} = \sqrt{32 - 4} = \sqrt{28} = \sqrt{4 \cdot 7} = 2\sqrt{7}$.
  * $f(-2) = \sqrt{32 - (-2)^2} = \sqrt{28} = 2\sqrt{7}$.
  * Thus, select **Choice A** and enter **`2\sqrt{7}`**.

---

### **Question 18**
* **Problem:** Determine whether the function is one-to-one: $f(x) = 3x^3 - 6$.
* **Answer:** **`Choice B: Yes, because each x-value corresponds to only one f(x) value, and each f(x) value corresponds to only one x-value.`**
* **Graph Equation:** `f(x) = 3x^3 - 6`
* **The Rule:** A cubic function of the form $f(x) = ax^3 + d$ ($a \neq 0$) is strictly monotonic and one-to-one.
* **Work:**
  * $3a^3 - 6 = 3b^3 - 6 \implies a^3 = b^3 \implies a = b$. Every $x$-value corresponds to a unique $f(x)$ value, and vice versa (**Choice B**).

---

### **Question 19**
* **Problem:** If the function defined by the following is one-to-one, find its inverse: $\{(-2, 6), (3, 2), (5, 9)\}$.
* **Answer:** **`Choice A: The inverse function is {` `(6, -2), (2, 3), (9, 5)` `}.`**
* **The Rule:** A set of ordered pairs is one-to-one if no two pairs share the same $y$-coordinate. Its inverse is found by swapping $(x, y) \to (y, x)$ in each pair.
* **Work:**
  * The $y$-values are $6, 2, 9$ (all distinct), so it is one-to-one.
  * Swapping coordinates gives $(6, -2), (2, 3), (9, 5)$.

---

### **Question 20**
* **Problem:** If the function defined by the following is one-to-one, find its inverse: $\{(4, 3), (1, 7), (5, 2), (3, 3)\}$.
* **Answer:** **`Choice B: The function is not one-to-one.`**
* **The Rule:** If two different inputs have the same output ($y$-value), the function is not one-to-one.
* **Work:**
  * Both $(4, 3)$ and $(3, 3)$ have the output $y = 3$. Therefore, the function is **not one-to-one** (**Choice B**).

---

### **Question 21**
* **Problem:** The graph of a function $f$ is shown. Use the graph to find $f^{-1}(-7)$.
* **Answer:** **`-8`**
* **Graph Equation:** `f(x) = x + 1`
* **The Rule:** $f^{-1}(y) = x \iff f(x) = y$. Find the point on the graph with $y$-coordinate $-7$ and read its $x$-coordinate.
* **Work:**
  * Looking at the red dots on the graph: the lowest point is at $(-8, -7)$, the middle points are $(-3, -3)$ and $(2, 0)$, and the top point is $(8, 7)$.
  * Since $(-8, -7)$ is on the graph of $f$, $f(-8) = -7$, which means $f^{-1}(-7) = -8$.

---

### **Question 22**
* **Problem:** The graph of a function $f$ is shown. Use the graph to find $f^{-1}(-3)$.
* **Answer:** **`-2`**
* **Graph Equation:** `f(x) = 0.5x - 2`
* **The Rule:** $f^{-1}(-3)$ is the $x$-coordinate of the point on the graph where $y = -3$.
* **Work:**
  * Looking at the plotted red points on the graph: $(-8, -5)$, $(-2, -3)$, $(5, 0)$, and $(8, 5)$.
  * At $y = -3$, the plotted point is $(-2, -3)$. Thus, $f(-2) = -3 \implies f^{-1}(-3) = -2$.

---

### **Question 23**
* **Problem:** The graph of a function $f$ is shown. Use the graph to find $f^{-1}(0)$.
* **Answer:** **`3`**
* **Graph Equation:** `f(x) = x - 3`
* **The Rule:** $f^{-1}(0)$ is the $x$-intercept of the graph of $f$ (where $y = 0$).
* **Work:**
  * Looking at the plotted red points on the graph: $(-8, -4)$, $(-2, -2)$, $(3, 0)$, and $(8, 6)$.
  * The graph crosses $y = 0$ at the plotted point $(3, 0)$. Thus, $f(3) = 0 \implies f^{-1}(0) = 3$.

---

### **Question 24**
* **Problem:** Use the definition of inverses to determine whether $f$ and $g$ are inverses: $f(x) = -2x + 10$, $g(x) = -\frac{1}{2}x - 10$.
* **Answer:** **`No`**
* **Graph Equation:** `f(x) = -2x + 10`
* **The Rule:** $f$ and $g$ are inverses if and only if $(f \circ g)(x) = x$ and $(g \circ f)(x) = x$.
* **Work:**
  * $(f \circ g)(x) = -2\left(-\frac{1}{2}x - 10\right) + 10 = x + 20 + 10 = x + 30 \neq x$.
  * Since $(f \circ g)(x) \neq x$, they are **No** (not inverses).

---

### **Question 25**
* **Problem:** Are the functions $f$ and $g$ inverses of each other? $f(x) = 7x - 8$, $g(x) = \frac{x + 7}{8}$.
* **Answer:** **`No`**
* **Graph Equation:** `f(x) = 7x - 8`
* **The Rule:** Check whether $f(g(x)) = x$.
* **Work:**
  * $f(g(x)) = 7\left(\frac{x + 7}{8}\right) - 8 = \frac{7x + 49 - 64}{8} = \frac{7x - 15}{8} \neq x$.
  * Thus, **No** (the true inverse of $7x - 8$ is $\frac{x + 8}{7}$).

---

### **Question 26**
* **Problem:** Use the definition of inverses to determine whether $f$ and $g$ are inverses: $f(x) = \frac{5x + 8}{x + 3}$, $g(x) = \frac{3x - 8}{5 - x}$.
* **Answer:** **`Yes`**
* **Graph Equation:** `f(x) = (5x + 8) / (x + 3)`
* **The Rule:** Verify $(f \circ g)(x) = x$ and $(g \circ f)(x) = x$.
* **Work:**
  * $(f \circ g)(x) = \frac{5\left(\frac{3x - 8}{5 - x}\right) + 8}{\left(\frac{3x - 8}{5 - x}\right) + 3} = \frac{5(3x - 8) + 8(5 - x)}{(3x - 8) + 3(5 - x)} = \frac{15x - 40 + 40 - 8x}{3x - 8 + 15 - 3x} = \frac{7x}{7} = x$.
  * $(g \circ f)(x) = \frac{3\left(\frac{5x + 8}{x + 3}\right) - 8}{5 - \left(\frac{5x + 8}{x + 3}\right)} = \frac{15x + 24 - 8x - 24}{5x + 15 - 5x - 8} = \frac{7x}{7} = x$.
  * Therefore, **Yes**, they are inverses.

---

### **Question 27**
* **Problem:** The graph of a one-to-one function is given with points $(-4, -2), (-2, 1), (0, 2), (1, 4)$. Draw the graph of the inverse function $f^{-1}$.
* **Answer:** **`Choice D`**
* **The Rule:** To graph $f^{-1}$, swap the coordinates of every point $(x, y) \to (y, x)$ on $f$ (reflect across $y = x$).
* **Work:**
  * Original points on $f$: $(-4, -2), (-2, 1), (0, 2), (1, 4)$.
  * Inverse points on $f^{-1}$: $(-2, -4), (1, -2), (2, 0), (4, 1)$.
  * **Choice D** is the only graph displaying these exact four points: $(-2, -4), (1, -2), (2, 0), (4, 1)$.

---

### **Question 28**
* **Problem:** Graph the inverse of the given one-to-one function (a curve passing through $(-2, -2), (2, 0), (10, 10)$ lying below $y = x$ for $x \in (-2, 10)$).
* **Answer:** **`Choice C`**
* **Graph Equation:** `f(x) = (x - 2)^2 / 8`
* **The Rule:** The graph of $f^{-1}$ is the reflection of the given curve across the dashed line $y = x$.
* **Work:**
  * The given curve passes through $(-2, -2)$, $(0, -1)$, $(2, 0)$, and $(10, 10)$, staying below the line $y = x$ between $(-2, -2)$ and $(10, 10)$.
  * Reflecting across $y = x$ maps $(2, 0) \to (0, 2)$ and $(0, -1) \to (-1, 0)$, producing a curve that arches *above* the line $y = x$ between $(-2, -2)$ and $(10, 10)$.
  * **Choice C** shows this exact reflection arching above $y = x$ through $(-2, -2), (0, 2), (10, 10)$.

---

### **Question 29**
* **Problem:** Decide whether the given functions are inverses from the tables:
  * $f$: $(2, 3), (-1, -5), (-5, 9), (3, 1)$
  * $g$: $(3, 2), (-5, -1), (-9, -5), (1, 3)$
* **Answer:** **`No`**
* **The Rule:** For $f$ and $g$ to be inverses, every pair $(a, b)$ in $f$ must appear as $(b, a)$ in $g$.
* **Work:**
  * In $f$, we have $(-5, 9)$, so $g$ would need to contain $(9, -5)$. Instead, $g$ has $(-9, -5)$. Thus, **No**.

---

### **Question 31**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = 2x - 8$.
* **Answer:** **`Choice C:` $f^{-1}(x) = \frac{x + 8}{2}$**
* **Graph Equation:** `f(x) = 2x - 8`
* **The Rule:** Swap $x$ and $y$, then solve for $y$.
* **Work:**
  * $y = 2x - 8 \implies x = 2y - 8 \implies x + 8 = 2y \implies y = \frac{x + 8}{2}$ (**Choice C**).

---

### **Question 32**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = 2x$.
* **Answer:** **`Choice A:` $f^{-1}(x) = \frac{x}{2}$**
* **Graph Equation:** `f(x) = 2x`
* **The Rule:** Swap $x$ and $y$, then solve for $y$.
* **Work:**
  * $y = 2x \implies x = 2y \implies y = \frac{x}{2}$ (**Choice A**).

---

### **Question 33**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = \frac{8}{x}$.
* **Answer:** **`Choice B:` $f^{-1}(x) = \frac{8}{x}$**
* **Graph Equation:** `f(x) = 8 / x`
* **The Rule:** Swap $x$ and $y$, then solve for $y$. Reciprocal functions $f(x) = \frac{k}{x}$ are their own inverses.
* **Work:**
  * $y = \frac{8}{x} \implies x = \frac{8}{y} \implies xy = 8 \implies y = \frac{8}{x}$ (**Choice B**).

---

### **Question 34**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = x^3 - 3$.
* **Answer:** **`Choice C:` $f^{-1}(x) = \sqrt[3]{x + 3}$**
* **Graph Equation:** `f(x) = x^3 - 3`
* **The Rule:** Swap $x$ and $y$, add $3$, and take the cube root of the entire expression $x + 3$.
* **Work:**
  * $y = x^3 - 3 \implies x = y^3 - 3 \implies y^3 = x + 3 \implies y = \sqrt[3]{x + 3}$ (**Choice C**, where the radical bar covers all of $x + 3$).

---

### **Question 35**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = \frac{7x + 2}{5}$.
* **Answer:** **`Choice D:` $f^{-1}(x) = \frac{5x - 2}{7}$**
* **Graph Equation:** `f(x) = (7x + 2) / 5`
* **The Rule:** Swap $x$ and $y$, multiply by $5$, subtract $2$, and divide by $7$.
* **Work:**
  * $y = \frac{7x + 2}{5} \implies x = \frac{7y + 2}{5} \implies 5x = 7y + 2 \implies 7y = 5x - 2 \implies y = \frac{5x - 2}{7}$ (**Choice D**).

---

### **Question 36**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = (x + 6)^3$.
* **Answer:** **`Choice C:` $f^{-1}(x) = \sqrt[3]{x} - 6$**
* **Graph Equation:** `f(x) = (x + 6)^3`
* **The Rule:** Swap $x$ and $y$, take the cube root first, then subtract $6$ outside the radical.
* **Work:**
  * $y = (x + 6)^3 \implies x = (y + 6)^3 \implies \sqrt[3]{x} = y + 6 \implies y = \sqrt[3]{x} - 6$ (**Choice C**).

---

### **Question 37**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = (x + 2)^3 - 8$.
* **Answer:** **`Choice C:` $f^{-1}(x) = \sqrt[3]{x + 8} - 2$**
* **Graph Equation:** `f(x) = (x + 2)^3 - 8`
* **The Rule:** Swap $x$ and $y$, isolate the cubed term, take the cube root, and isolate $y$.
* **Work:**
  * $y = (x + 2)^3 - 8 \implies x = (y + 2)^3 - 8 \implies x + 8 = (y + 2)^3 \implies \sqrt[3]{x + 8} = y + 2 \implies y = \sqrt[3]{x + 8} - 2$ (**Choice C**).

---

### **Question 38**
* **Problem:** The function $f$ is one-to-one. Find its inverse: $f(x) = \sqrt{x + 4}$.
* **Answer:** **`Choice D:` $f^{-1}(x) = x^2 - 4, x \ge 0$**
* **Graph Equation:** `f(x) = sqrt(x + 4)`
* **The Rule:** The range of $f(x) = \sqrt{x + 4}$ is $[0, \infty)$, which restricts the domain of $f^{-1}$ to $x \ge 0$.
* **Work:**
  * $y = \sqrt{x + 4}$ with $y \ge 0$.
  * Swap $x$ and $y$: $x = \sqrt{y + 4}$ for $x \ge 0$.
  * Square both sides: $x^2 = y + 4 \implies y = x^2 - 4, x \ge 0$ (**Choice D**).

---

### **Question 39**
* **Problem:** For the function $f(x) = 2x - 7$, determine whether $f(x)$ is one-to-one. If so, (a) write an equation for the inverse function, (b) graph $f$ and $f^{-1}$ on the same axes, and (c) give the domain and range of $f$ and $f^{-1}$.
* **Answer:**
  * **(a) `Choice A`: $f^{-1}(x) =$ `(x + 7)/2`** (or `\frac{x+7}{2}`)
  * **(b) `Choice B`**
  * **(c) Domain and Range of $f$: `Choice A`, Domain = `(-\infty, \infty)`, Range = `(-\infty, \infty)`**
  * **(c) Domain and Range of $f^{-1}$: `Choice A`, Domain = `(-\infty, \infty)`, Range = `(-\infty, \infty)`**
* **Graph Equation:** `f(x) = 2x - 7`
* **The Rule:** Linear functions with non-zero slope have domain and range $(-\infty, \infty)$, and their inverses are reflections across $y = x$.
* **Work:**
  * (a) $x = 2y - 7 \implies 2y = x + 7 \implies f^{-1}(x) = \frac{x + 7}{2}$.
  * (b) $f(x) = 2x - 7$ has $y$-intercept $(0, -7)$ and slope $2$ (solid blue line). $f^{-1}(x) = \frac{1}{2}x + 3.5$ has $y$-intercept $(0, 3.5)$ and $x$-intercept $(-7, 0)$ (dashed red line). This matches **Choice B**.
  * (c) Both linear functions have domain $(-\infty, \infty)$ and range $(-\infty, \infty)$.

---

### **Question 40**
* **Problem:** The function $f(x) = 6x + 3$ is one-to-one. (a) Find the inverse of $f$. (b) State the domain and range of $f$. (c) State the domain and range of $f^{-1}$. (d) Graph $f, f^{-1}$, and $y = x$ on the same set of axes.
* **Answer:**
  * **(a) $f^{-1}(x) =$ `(x - 3)/6`** (or `\frac{1}{6}x - \frac{1}{2}`)
  * **(b) `Choice D: The domain and range of f are all real numbers.`**
  * **(c) `Choice D: The domain and range of f^(-1) are all real numbers.`**
  * **(d) `Choice A`**
* **Graph Equation:** `f(x) = 6x + 3`
* **The Rule:** Swap $x$ and $y$ to solve for $f^{-1}(x)$, and match intercepts on the graph.
* **Work:**
  * (a) $x = 6y + 3 \implies 6y = x - 3 \implies f^{-1}(x) = \frac{x - 3}{6}$.
  * (b) & (c) Non-constant linear functions have domain and range equal to all real numbers (**Choice D**).
  * (d) $f(x) = 6x + 3$ is steep with $y$-intercept $(0, 3)$, and $f^{-1}(x) = \frac{x - 3}{6}$ is shallow with $x$-intercept $(3, 0)$ and $y$-intercept $(0, -0.5)$. Both intersect on $y = x$ in Quadrant III at $(-0.6, -0.6)$. This matches **Choice A**.

---

### **Question 41**
* **Problem:** Determine whether $f(x) = x^3 - 4$ is one-to-one. If so, (a) write an equation for $f^{-1}(x)$, (b) graph $f$ and $f^{-1}$, and (c) give the domain and range of $f$ and $f^{-1}$.
* **Answer:**
  * **(a) `Choice A`: $f^{-1}(x) =$ `\sqrt[3]{x + 4}`**
  * **(b) `Choice B`**
  * **(c) Domain and Range of $f$: `Choice A`, Domain = `(-\infty, \infty)`, Range = `(-\infty, \infty)`**
  * **(c) Domain and Range of $f^{-1}$: `Choice A`, Domain = `(-\infty, \infty)`, Range = `(-\infty, \infty)`**
* **Graph Equation:** `f(x) = x^3 - 4`
* **The Rule:** Cubic functions are one-to-one on $(-\infty, \infty)$ with cube-root inverses.
* **Work:**
  * (a) $x = y^3 - 4 \implies y^3 = x + 4 \implies f^{-1}(x) = \sqrt[3]{x + 4}$.
  * (b) $f(x) = x^3 - 4$ (solid blue) has $y$-intercept $(0, -4)$, and $f^{-1}(x) = \sqrt[3]{x + 4}$ (dashed red) has $x$-intercept $(-4, 0)$. This matches **Choice B**.
  * (c) Both cubic and cube-root functions have domain $(-\infty, \infty)$ and range $(-\infty, \infty)$.

---

### **Question 42**
* **Problem:** Determine whether $f(x) = x^2 + 13$ is one-to-one. If so, (a) write an equation for $f^{-1}(x)$, (b) graph $f$ and $f^{-1}$, and (c) give the domain and range of $f$ and $f^{-1}$.
* **Answer:**
  * **(a) `Choice B: The function is not one-to-one.`**
  * **(b) `Choice D: The function is not one-to-one. Thus, the inverse does not exist.`**
  * **(c) Domain and Range of $f$: `Choice A`, Domain = `(-\infty, \infty)`, Range = `[13, \infty)`**
  * **(c) Domain and Range of $f^{-1}$: `Choice B: The function is not one-to-one.`**
* **Graph Equation:** `f(x) = x^2 + 13`
* **The Rule:** An unrestricted quadratic function $f(x) = x^2 + k$ is not one-to-one; its domain is $(-\infty, \infty)$ and its range is $[k, \infty)$.
* **Work:**
  * (a) & (b) Because $f(-1) = f(1) = 14$, $f$ is not one-to-one, so $f^{-1}$ does not exist (**Choice B** for a, **Choice D** for b).
  * (c) Even though $f$ is not one-to-one, $f(x) = x^2 + 13$ itself has domain $(-\infty, \infty)$ and since $x^2 \ge 0$, $x^2 + 13 \ge 13$, giving range $[13, \infty)$. For $f^{-1}$, select **Choice B: The function is not one-to-one.**

---

### **Question 43**
* **Problem:** Determine whether $f(x) = \frac{11}{x}$ is one-to-one. If so, (a) write an equation for $f^{-1}(x)$, (b) graph $f$ and $f^{-1}$, and (c) give the domain and range of $f$ and $f^{-1}$.
* **Answer:**
  * **(a) `Choice A`: $f^{-1}(x) =$ `11/x`** (or `\frac{11}{x}`)
  * **(b) `Choice B`**
  * **(c) Domain and Range of $f$: `Choice A`, Domain = `(-\infty, 0) \cup (0, \infty)`, Range = `(-\infty, 0) \cup (0, \infty)`**
  * **(c) Domain and Range of $f^{-1}$: `Choice A`, Domain = `(-\infty, 0) \cup (0, \infty)`, Range = `(-\infty, 0) \cup (0, \infty)`**
* **Graph Equation:** `f(x) = 11 / x`
* **The Rule:** $f(x) = \frac{k}{x}$ ($k > 0$) is symmetric across $y = x$, so $f^{-1}(x) = f(x) = \frac{k}{x}$ with hyperbola branches in Quadrants I and III.
* **Work:**
  * (a) $x = \frac{11}{y} \implies y = \frac{11}{x}$.
  * (b) Since $f$ and $f^{-1}$ are identical and $11 > 0$, both curves lie on top of each other in Quadrants I and III (**Choice B**).
  * (c) Neither $x$ nor $y$ can be $0$, so all domains and ranges are $(-\infty, 0) \cup (0, \infty)$.

---

### **Question 44**
* **Problem:** Determine whether $f(x) = \frac{1}{x - 7}, x \neq 7$ is one-to-one. If so, (a) write an equation for $f^{-1}(x)$, (b) graph $f$ and $f^{-1}$, and (c) give the domain and range of $f$ and $f^{-1}$.
* **Answer:**
  * **(a) `Choice A`: $f^{-1}(x) =$ `\frac{1}{x} + 7`** (or `\frac{7x + 1}{x}`)
  * **(b) `Choice B`**
  * **(c) Domain and Range of $f$: `Choice A`, Domain = `(-\infty, 7) \cup (7, \infty)`, Range = `(-\infty, 0) \cup (0, \infty)`**
  * **(c) Domain and Range of $f^{-1}$: `Choice A`, Domain = `(-\infty, 0) \cup (0, \infty)`, Range = `(-\infty, 7) \cup (7, \infty)`**
* **Graph Equation:** `f(x) = 1 / (x - 7)`
* **The Rule:** Swap $x$ and $y$ to find $f^{-1}$. The vertical asymptote $x = 7$ of $f$ becomes the horizontal asymptote $y = 7$ of $f^{-1}$.
* **Work:**
  * (a) $x = \frac{1}{y - 7} \implies y - 7 = \frac{1}{x} \implies f^{-1}(x) = \frac{1}{x} + 7$ (or $\frac{1 + 7x}{x}$).
  * (b) $f(x)$ has vertical asymptote $x = 7$ and horizontal asymptote $y = 0$; $f^{-1}(x)$ has vertical asymptote $x = 0$ and horizontal asymptote $y = 7$ (in the upper half of the grid). Looking at Choices A and B: in **Choice B**, the hyperbola $f^{-1}(x)$ is centered at $(0, 7)$ with upper-right branch in Quadrant I above $y = 7$, and $f(x)$ is centered at $(7, 0)$ with right branch in Quadrant I to the right of $x = 7$. (In Choice A, the branches are inverted as if numerator were $-1$). Thus, **Choice B** is correct.
  * (c) Domain of $f$ excludes $7$: $(-\infty, 7) \cup (7, \infty)$. Range of $f$ excludes $0$: $(-\infty, 0) \cup (0, \infty)$. Swap these for $f^{-1}$.

---

### **Question 45**
* **Problem:** Determine if the function $f(x) = \frac{x + 4}{x - 5}, x \neq 5$, is one-to-one. If so, find the inverse, graph $f$ and $f^{-1}$, and give the domain and range of $f$ and $f^{-1}$.
* **Answer:**
  * **Inverse Equation: `Choice A`: $f^{-1}(x) =$ `\frac{5x + 4}{x - 1}`**
  * **Graph: `Choice C`**
  * **Domain of $f$: `Choice A`, `(-\infty, 5) \cup (5, \infty)`**
  * **Domain of $f^{-1}$: `Choice A`, `(-\infty, 1) \cup (1, \infty)`**
  * **Range of $f$: `Choice A`, `(-\infty, 1) \cup (1, \infty)`**
  * **Range of $f^{-1}$: `Choice A`, `(-\infty, 5) \cup (5, \infty)`**
* **Graph Equation:** `f(x) = (x + 4) / (x - 5)`
* **The Rule:** For $f(x) = \frac{ax + b}{cx + d}$, swap $x$ and $y$ and solve for $y$. Domain of $f$ excludes where the denominator of $f$ is zero; Range of $f$ (and Domain of $f^{-1}$) excludes the horizontal asymptote $y = \frac{a}{c}$.
* **Work:**
  * 1. Find inverse: $x = \frac{y + 4}{y - 5} \implies x(y - 5) = y + 4 \implies xy - 5x = y + 4 \implies xy - y = 5x + 4 \implies y(x - 1) = 5x + 4 \implies f^{-1}(x) = \frac{5x + 4}{x - 1}$.
  * 2. Match graph: $f(x)$ (solid blue) has vertical asymptote $x = 5$ and horizontal asymptote $y = 1$. $f^{-1}(x)$ (dashed red) has vertical asymptote $x = 1$ and horizontal asymptote $y = 5$. At $x = 6$, $f(6) = 10$ and at $x = 2$, $f^{-1}(2) = 14$. This matches **Choice C**.
  * 3. Domains and Ranges:
    * Domain of $f$ ($x \neq 5$): $(-\infty, 5) \cup (5, \infty)$
    * Domain of $f^{-1}$ ($x \neq 1$): $(-\infty, 1) \cup (1, \infty)$
    * Range of $f$ ($y \neq 1$): $(-\infty, 1) \cup (1, \infty)$
    * Range of $f^{-1}$ ($y \neq 5$): $(-\infty, 5) \cup (5, \infty)$
