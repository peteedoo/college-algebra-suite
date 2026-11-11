# **Build Understanding 3.5: Rational Functions — Answers**

---

### **Question 1**
* **Problem:** Select the correct choices that complete the sentence below. If the graph of a function $f$ increases or decreases without bound as $x$ approaches $a$, then the line $x = a$ is (1) ________ of the graph of $f$. The equation of such a line for the graph of $f(x) = \frac{7}{x + 4}$ is (2) ________.
* **Answer:** **(1) `a vertical asymptote`, (2) `x = -4.`**
* **Graph Equation:** `f(x) = 7/(x + 4)`
* **The Rule:** A vertical line $x = a$ where $f(x) \to \pm\infty$ as $x \to a$ is a vertical asymptote, found by setting the simplified denominator equal to $0$.
* **Work:**
  1. By definition, the line $x = a$ is **a vertical asymptote**.
  2. Set the denominator of $f(x) = \frac{7}{x + 4}$ equal to $0$:
     $$x + 4 = 0 \implies x = -4$$

---

### **Question 2**
* **Problem:** Select the correct choices that complete the sentence below. If the graph of a function $f$ approaches $b$ as $x$ increases or decreases without bound, then the line $y = b$ is (1) ________ of the graph of $f$. The equation of such a line for the graph of $y = \frac{x - 10}{3x^2 + x + 1}$ is (2) ________. The equation of such a line for the graph of $y = \frac{x^2 - 10}{3x^2 + x + 1}$ is (3) ________.
* **Answer:** **(1) `a horizontal asymptote`, (2) `y = 0.`, (3) `y = 1/3.`**
* **Graph Equation:** `f(x) = (x^2 - 10)/(3x^2 + x + 1)`
* **The Rule:** A horizontal line $y = b$ approached as $x \to \pm\infty$ is a horizontal asymptote. If $\deg(\text{num}) < \deg(\text{den})$, it is $y = 0$; if $\deg(\text{num}) = \deg(\text{den})$, it is $y = \frac{\text{leading coeff of num}}{\text{leading coeff of den}}$.
* **Work:**
  1. By definition, $y = b$ is **a horizontal asymptote**.
  2. For $y = \frac{x - 10}{3x^2 + x + 1}$, $\deg(\text{num}) = 1 < \deg(\text{den}) = 2$, so the horizontal asymptote is **$y = 0$**.
  3. For $y = \frac{x^2 - 10}{3x^2 + x + 1}$, $\deg(\text{num}) = 2 = \deg(\text{den}) = 2$, so the horizontal asymptote is **$y = \frac{1}{3}$**.

---

### **Question 3**
* **Problem:** Decide whether the following statement is true or false. "If the degree of the numerator of a rational function equals the degree of the denominator, then the ratio of the leading coefficients gives rise to the horizontal asymptote."
* **Answer:** **`True`**
* **The Rule:** When a rational function $f(x) = \frac{a_n x^n + \dots}{b_n x^n + \dots}$ has equal degrees in the numerator and denominator, its horizontal asymptote is $y = \frac{a_n}{b_n}$.
* **Work:**
  1. As $x \to \pm\infty$, the highest-degree terms dominate: $\frac{a_n x^n}{b_n x^n} = \frac{a_n}{b_n}$.
  2. Thus, the ratio of the leading coefficients gives the horizontal asymptote $y = \frac{a_n}{b_n}$. The statement is **True**.

---

### **Question 4**
* **Problem:** Fill in the blank so that the resulting statement is true. The graph of a rational function has a slant asymptote if the degree of the numerator is (1) ________ the degree of the denominator.
* **Answer:** **(1) `one more than`**
* **The Rule:** A rational function (in lowest terms) has a slant (oblique) asymptote if and only if the degree of the numerator is exactly **one more than** the degree of the denominator.
* **Work:**
  1. When $\deg(p(x)) = \deg(q(x)) + 1$, polynomial division yields a linear quotient $mx + b$ plus a remainder whose fraction approaches $0$ as $x \to \pm\infty$.
  2. Therefore, the degree of the numerator must be **one more than** the degree of the denominator.

---

### **Question 5**
* **Problem:** Match each description from Column I with the correct rational function in Column II:
  * (1) The $x$-intercept is $(-8, 0)$.
  * (2) The $y$-intercept is $(0, 3)$.
  * (3) The horizontal asymptote is $y = 3$.
  * (4) The vertical asymptote is $x = -3$.
  * (5) There is a hole in the graph at $(-9, -18)$.
  * (6) The graph has an oblique asymptote.
  * (7) The $x$-axis is its horizontal asymptote and the $y$-axis is not its vertical asymptote.
  * (8) The $x$-axis is its horizontal asymptote and the $y$-axis is its vertical asymptote.
* **Answer:**
  * **(1):** `f(x) = (x + 8)/(x - 16)`
  * **(2):** `f(x) = (x + 12)/(x + 4)`
  * **(3):** `f(x) = (3x + 7)/(x - 10)`
  * **(4):** `f(x) = (x + 6)/(x + 3)`
  * **(5):** `f(x) = (x^2 - 81)/(x + 9)`
  * **(6):** `f(x) = (x^2 + 6x + 7)/(x - 8)`
  * **(7):** `f(x) = 1/(x + 6)`
  * **(8):** `f(x) = -5/(x^2)`
* **Graph Equation:** `f(x) = (x + 8)/(x - 16)`
* **The Rule:** Match intercepts, asymptotes, and removable discontinuities by examining numerator roots, $f(0)$, leading degrees/coefficients, and denominator roots.
* **Work:**
  1. **$x$-intercept $(-8, 0)$:** Numerator $= 0$ at $x = -8 \implies f(x) = \frac{x + 8}{x - 16}$.
  2. **$y$-intercept $(0, 3)$:** Evaluate $f(0) = \frac{0 + 12}{0 + 4} = 3 \implies f(x) = \frac{x + 12}{x + 4}$.
  3. **Horizontal asymptote $y = 3$:** Ratio of leading coefficients is $\frac{3}{1} = 3 \implies f(x) = \frac{3x + 7}{x - 10}$.
  4. **Vertical asymptote $x = -3$:** Denominator $= 0$ at $x = -3 \implies f(x) = \frac{x + 6}{x + 3}$.
  5. **Hole at $(-9, -18)$:** $\frac{x^2 - 81}{x + 9} = \frac{(x - 9)(x + 9)}{x + 9} = x - 9$ for $x \neq -9$; at $x = -9$, $y = -9 - 9 = -18 \implies f(x) = \frac{x^2 - 81}{x + 9}$.
  6. **Oblique asymptote:** Degree of numerator ($2$) is $1$ more than degree of denominator ($1$) with no common factor $\implies f(x) = \frac{x^2 + 6x + 7}{x - 8}$.
  7. **HA is $x$-axis ($y = 0$) and VA is not $y$-axis ($x \neq 0$):** $\deg(\text{num}) < \deg(\text{den})$ and VA at $x = -6 \implies f(x) = \frac{1}{x + 6}$.
  8. **HA is $x$-axis ($y = 0$) and VA is $y$-axis ($x = 0$):** $\deg(\text{num}) < \deg(\text{den})$ and VA at $x = 0 \implies f(x) = \frac{-5}{x^2}$.

---

### **Question 6**
* **Graph Equation:** None
* **Problem:** *(Interactive GeoGebra Applet)* Explore the behavior of rational functions by adjusting sliders for numerator and denominator factors to observe vertical asymptotes, horizontal asymptotes, and holes.
* **Answer:** Use the interactive sliders to set the poles (vertical asymptotes) and roots (intercepts). Common factors in numerator and denominator produce holes rather than vertical asymptotes.
* **The Rule:** A factor $(x - c)$ in the denominator produces a vertical asymptote at $x = c$ if it does not cancel with the numerator, and a hole (removable discontinuity) at $x = c$ if it cancels.
* **Work:** Adjusting the sliders updates the curve and asymptotic dashed lines in real time matching the rational formula.

---

### **Question 7**
* **Problem:** Find the vertical asymptotes, if any, and the values of $x$ corresponding to holes, if any, of the graph of the rational function: $f(x) = \frac{x}{x - 1}$
* **Answer:** **Choice C: The vertical asymptote(s) is(are) `x = 1`. There are no holes.**
* **Graph Equation:** `f(x) = x/(x - 1)`
* **The Rule:** A root of the denominator that does not cancel with the numerator produces a vertical asymptote; a common factor that cancels produces a hole.
* **Work:**
  1. The numerator $x$ and denominator $x - 1$ share no common factors, so there are **no holes**.
  2. Set the denominator equal to zero: $x - 1 = 0 \implies x = 1$ (vertical asymptote).

---

### **Question 8**
* **Problem:** Find the vertical asymptotes, if any, and the values of $x$ corresponding to holes, if any, of the graph of the rational function: $h(x) = \frac{x + 3}{x(x - 7)}$
* **Answer:** **Choice B: The vertical asymptote(s) is(are) `x = 0, x = 7`. There are no holes.**
* **Graph Equation:** `h(x) = (x + 3)/(x*(x - 7))`
* **The Rule:** Set each non-canceling factor in the denominator equal to zero to find the vertical asymptotes.
* **Work:**
  1. No factors cancel between $x + 3$ and $x(x - 7)$, so there are **no holes**.
  2. Set the denominator equal to zero: $x(x - 7) = 0 \implies x = 0$ and $x = 7$.

---

### **Question 9**
* **Problem:** Find the vertical asymptotes, if any, and the values of $x$ corresponding to holes, if any, of the graph of the rational function: $h(x) = \frac{x}{x(x - 5)}$
* **Answer:** **Choice B: The vertical asymptote(s) is(are) `x = 5` and hole(s) corresponding to `x = 0`.**
* **Graph Equation:** `h(x) = x/(x*(x - 5))`
* **The Rule:** Cancel common factors to locate holes ($x = c$), then set the remaining denominator equal to zero to find vertical asymptotes.
* **Work:**
  1. Cancel the common factor $x$:
     $$h(x) = \frac{x}{x(x - 5)} = \frac{1}{x - 5}, \quad x \neq 0$$
  2. The canceled factor $x = 0$ gives a **hole** at $x = 0$.
  3. The remaining denominator factor $x - 5 = 0$ gives a **vertical asymptote** at $x = 5$.

---

### **Question 10**
* **Problem:** Find the vertical asymptotes, if any, and the value of $x$ corresponding to holes, if any, of the graph of the following rational function: $f(x) = \frac{x^2 - 4}{x - 2}$
* **Answer:** **Choice C: There are no vertical asymptotes but there is (are) hole(s) corresponding to $x =$ `2`.**
* **Graph Equation:** `f(x) = (x^2 - 4)/(x - 2)`
* **The Rule:** If all factors of the denominator cancel with factors in the numerator, there are no vertical asymptotes and only holes.
* **Work:**
  1. Factor the numerator and simplify:
     $$f(x) = \frac{(x - 2)(x + 2)}{x - 2} = x + 2, \quad x \neq 2$$
  2. Because $x - 2$ cancels completely, there is a **hole** at $x = 2$ and **no vertical asymptotes**.

---

### **Question 11**
* **Problem:** Find the vertical asymptotes, if any, and the value of $x$ corresponding to holes, if any, of the graph of the following rational function: $f(x) = \frac{x - 7}{x^2 - 49}$
* **Answer:** **Choice C: Vertical asymptote(s) at $x =$ `-7` and hole(s) corresponding to $x =$ `7`.**
* **Graph Equation:** `f(x) = (x - 7)/(x^2 - 49)`
* **The Rule:** Factor the denominator as a difference of squares, cancel common factors to identify holes, and use remaining denominator factors for vertical asymptotes.
* **Work:**
  1. Factor the denominator:
     $$f(x) = \frac{x - 7}{(x - 7)(x + 7)} = \frac{1}{x + 7}, \quad x \neq 7$$
  2. The canceled factor $x - 7 = 0$ gives a **hole** at $x = 7$.
  3. The remaining factor $x + 7 = 0$ gives a **vertical asymptote** at $x = -7$.

---

### **Question 12**
* **Problem:** Find the vertical asymptotes, if any, and the values of $x$ corresponding to holes, if any, of the graph of the rational function: $f(x) = \frac{x - 1}{x^2 - 3x + 2}$
* **Answer:** **Choice C: Vertical asymptote(s) at $x =$ `2` and hole(s) at $x =$ `1`**
* **Graph Equation:** `f(x) = (x - 1)/(x^2 - 3x + 2)`
* **The Rule:** Factor the quadratic denominator, cancel common factors for holes, and set the remaining denominator factor to zero for vertical asymptotes.
* **Work:**
  1. Factor the denominator:
     $$f(x) = \frac{x - 1}{(x - 1)(x - 2)} = \frac{1}{x - 2}, \quad x \neq 1$$
  2. The canceled factor $x - 1 = 0$ gives a **hole** at $x = 1$.
  3. The remaining factor $x - 2 = 0$ gives a **vertical asymptote** at $x = 2$.

---

### **Question 13**
* **Problem:** Find the horizontal asymptote, if any, of the graph of the rational function: $f(x) = \frac{18x}{3x^2 + 7}$
* **Answer:** **Choice A: The horizontal asymptote is `y = 0`.**
* **Graph Equation:** `f(x) = (18x)/(3x^2 + 7)`
* **The Rule:** If the degree of the numerator is less than the degree of the denominator, the horizontal asymptote is $y = 0$.
* **Work:**
  1. Degree of numerator ($18x$) is $1$; degree of denominator ($3x^2 + 7$) is $2$.
  2. Since $1 < 2$, the horizontal asymptote is **$y = 0$**.

---

### **Question 14**
* **Problem:** Find the horizontal asymptote, if any, of the graph of the rational function: $g(x) = \frac{27x^2}{9x^2 + 2}$
* **Answer:** **Choice A: The horizontal asymptote is `y = 3`.**
* **Graph Equation:** `g(x) = (27x^2)/(9x^2 + 2)`
* **The Rule:** If the degree of the numerator equals the degree of the denominator, the horizontal asymptote is $y = \frac{a_n}{b_n}$.
* **Work:**
  1. Both numerator and denominator have degree $2$.
  2. Divide the leading coefficients:
     $$y = \frac{27}{9} = 3$$

---

### **Question 15**
* **Problem:** Find the horizontal asymptote, if any, of the graph of the rational function: $h(x) = \frac{10x^3}{2x^2 + 5}$
  - Select the correct choice below and, if necessary, fill in the answer box to complete your choice.
    - **A.** The horizontal asymptote is ______. *(Type an equation.)*
    - **B.** There is no horizontal asymptote.
* **Answer:** **Choice B: There is no horizontal asymptote.**
  * **Horizontal Asymptote:** **`None`** *(Select Choice B)*
  * **Oblique (Slant) Asymptote:** **`y = 5x`** *(Found via polynomial division $\frac{10x^3}{2x^2 + 5} = 5x - \frac{25x}{2x^2 + 5}$)*
  * **Vertical Asymptote(s):** **`None`** *(Denominator $2x^2 + 5 = 0 \implies x^2 = -5/2$ has no real solutions)*
  * **Domain:** **`(-\infty, \infty)`**
* **Graph Equation:** `h(x) = (10x^3)/(2x^2 + 5)`
* **The Rule:**
  - If $\deg(\text{numerator}) < \deg(\text{denominator})$, the horizontal asymptote is $y = 0$.
  - If $\deg(\text{numerator}) = \deg(\text{denominator})$, the horizontal asymptote is $y = \frac{a_n}{b_n}$.
  - If $\deg(\text{numerator}) > \deg(\text{denominator})$, there is **no horizontal asymptote**. If $\deg(\text{numerator}) = \deg(\text{denominator}) + 1$, there is an **oblique (slant) asymptote** found by dividing the numerator by the denominator.
* **Work:**
  1. Degree of numerator ($10x^3$) is $3$; degree of denominator ($2x^2 + 5$) is $2$.
  2. Since $3 > 2$, there is **no horizontal asymptote** (**Choice B**).
  3. Divide numerator by denominator:
     $$\frac{10x^3}{2x^2 + 5} = 5x - \frac{25x}{2x^2 + 5}$$
     As $x \to \pm\infty$, the remainder term $\frac{25x}{2x^2 + 5} \to 0$, giving the oblique asymptote line $y = 5x$.

---

### **Question 16**
* **Problem:** Give the equations of any vertical, horizontal, or oblique asymptotes for the graph of the rational function: $f(x) = \frac{6}{x - 4}$
  - Identify any vertical asymptotes:
    - **A.** There is one vertical asymptote. Its equation is ______.
    - **B.** There are two vertical asymptotes...
    - **C.** There are no vertical asymptotes.
  - Identify the horizontal or oblique asymptote, if one exists:
    - **A.** The function has a horizontal asymptote whose equation is ______.
    - **B.** The function has an oblique asymptote whose equation is ______.
    - **C.** The function has neither a horizontal nor an oblique asymptote.
* **Answer:**
  * **Vertical Asymptote:** **Choice A: There is one vertical asymptote. Its equation is `x = 4`.**
  * **Horizontal Asymptote:** **Choice A: The function has a horizontal asymptote whose equation is `y = 0`.**
  * **Oblique Asymptote:** **Choice C: The function has neither a horizontal nor an oblique asymptote (or no oblique asymptote).**
  * **Domain:** **`(-\infty, 4) \cup (4, \infty)`**
  * **Intercepts:** No $x$-intercepts ($6 \neq 0$); $y$-intercept is $(0, -1.5)$ or $(0, -\frac{3}{2})$.
* **Graph Equation:** `f(x) = 6/(x - 4)`
* **The Rule:**
  - Vertical asymptotes: Set the denominator $Q(x) = 0$ after simplifying common factors.
  - Horizontal asymptotes: Compare degrees: $\deg(6) = 0 < \deg(x - 4) = 1 \implies y = 0$.
* **Work:**
  1. **Vertical asymptote:** $x - 4 = 0 \implies x = 4$. There is one vertical asymptote: $x = 4$ (**Choice A**).
  2. **Horizontal asymptote:** $\deg(\text{num}) = 0 < \deg(\text{den}) = 1 \implies y = 0$. The horizontal asymptote is $y = 0$ (**Choice A**).
  3. Since the function has a horizontal asymptote, it cannot have an oblique asymptote.

---

### **Question 17**
* **Problem:** Give the equations of any vertical, horizontal, or oblique asymptotes for the graph of the rational function: $f(x) = \frac{2 - 4x}{2x + 4}$
* **Answer:**
  * **Vertical Asymptote:** **Choice A: The equation of the vertical asymptote is $x =$ `-2`.**
  * **Horizontal Asymptote:** **Choice A: The equation of the horizontal asymptote is $y =$ `-2`.**
  * **Oblique Asymptote:** **Choice B: There is no oblique asymptote.**
* **Graph Equation:** `f(x) = (2 - 4x)/(2x + 4)`
* **The Rule:** Rewrite the numerator in descending powers of $x$ ($-4x + 2$) to avoid sign errors when taking the ratio of leading coefficients.
* **Work:**
  1. **Vertical asymptote:** Set $2x + 4 = 0 \implies 2x = -4 \implies x = -2$. No common factor cancels at $x = -2$.
  2. **Horizontal asymptote:** Write $f(x) = \frac{-4x + 2}{2x + 4}$. Since both degrees are $1$, $y = \frac{-4}{2} = -2$.
  3. **Oblique asymptote:** Because the function has a horizontal asymptote, there is **no oblique asymptote**.

---

### **Question 18**
* **Problem:** Give the equations of any vertical, horizontal, or oblique asymptotes for the graph of the rational function: $f(x) = \frac{x^2 - 3x - 4}{2x^2 - x - 10}$
* **Answer:**
  * **Vertical Asymptotes:** **Choice A: The vertical asymptotes are $x =$ `-2, 5/2`.**
  * **Horizontal Asymptote:** **Choice A: The horizontal asymptote is $y =$ `1/2`.**
  * **Oblique Asymptote:** **Choice B: There is no oblique asymptote.**
* **Graph Equation:** `f(x) = (x^2 - 3x - 4)/(2x^2 - x - 10)`
* **The Rule:** Factor numerator and denominator to verify no common factors cancel, find vertical asymptotes from denominator roots, and use the leading coefficient ratio for the horizontal asymptote.
* **Work:**
  1. Factor numerator and denominator:
     $$f(x) = \frac{(x - 4)(x + 1)}{(2x - 5)(x + 2)}$$
  2. **Vertical asymptotes:** No factors cancel, so set $(2x - 5)(x + 2) = 0 \implies x = -2, \frac{5}{2}$.
  3. **Horizontal asymptote:** Degrees are both $2$, so $y = \frac{1}{2}$.
  4. **Oblique asymptote:** None (**Choice B**).

---

### **Question 19**
* **Problem:** Give the equations of any vertical, horizontal, or oblique asymptotes for the graph of the rational function: $f(x) = \frac{7x^2 + 4}{x^2 + 3}$
* **Answer:**
  * **Vertical Asymptotes:** **Choice B: There is no vertical asymptote.**
  * **Horizontal Asymptotes:** **Choice A: $y =$ `7`**
  * **Oblique Asymptotes:** **Choice B: There is no oblique asymptote.**
* **Graph Equation:** `f(x) = (7x^2 + 4)/(x^2 + 3)`
* **The Rule:** A sum of squares $x^2 + c$ ($c > 0$) is never zero for real $x$, meaning there are no vertical asymptotes.
* **Work:**
  1. **Vertical asymptotes:** $x^2 + 3 \ge 3 > 0$ for all real $x$, so there is **no vertical asymptote**.
  2. **Horizontal asymptote:** Both degrees are $2$, so $y = \frac{7}{1} = 7$.
  3. **Oblique asymptote:** None (**Choice B**).

---

### **Question 20**
* **Problem:** Which of the following functions have a graph that does not have a vertical asymptote? Select all that apply.
  * A. $f(x) = \frac{2}{x^2}$
  * B. $f(x) = \frac{1}{x^2 - 5}$
  * C. $f(x) = \frac{1}{x^2 + 5}$
  * D. $f(x) = \frac{3x + 1}{x - 8}$
* **Answer:** **Choice C (`f(x) = 1/(x^2 + 5)`)**
* **Graph Equation:** `f(x) = 1/(x^2 + 5)`
* **The Rule:** A rational function has no vertical asymptotes when its simplified denominator has no real zeros.
* **Work:**
  1. In A, $x^2 = 0 \implies x = 0$ (VA).
  2. In B, $x^2 - 5 = 0 \implies x = \pm\sqrt{5}$ (VAs).
  3. In **C**, $x^2 + 5 = 0 \implies x^2 = -5$, which has no real solutions. Thus **C** has no vertical asymptote.
  4. In D, $x - 8 = 0 \implies x = 8$ (VA).

---

### **Question 21**
* **Problem:** Identify any vertical, horizontal, or oblique asymptotes in the graph of $y = f(x)$. State the domain of $f$.
* **Answer:**
  * **Vertical Asymptote:** **Choice A: There is one vertical asymptote. Its equation is `x = 1`.**
  * **Horizontal Asymptote:** **Choice A: The equation of the horizontal asymptote is `y = 1`.**
  * **Domain:** `(-\infty, 1) \cup (1, \infty)`
* **Graph Equation:** `f(x) = 1/(x - 1) + 1`
* **The Rule:** Read dashed vertical lines as vertical asymptotes $x = a$, dashed horizontal lines as horizontal asymptotes $y = b$, and exclude vertical asymptotes from the domain.
* **Work:**
  1. The dashed vertical line passes through $x = 1$, giving the vertical asymptote **`x = 1`**.
  2. The dashed horizontal line passes through $y = 1$, giving the horizontal asymptote **`y = 1`**.
  3. Excluding $x = 1$ gives the domain **`(-\infty, 1) \cup (1, \infty)`**.

---

### **Question 22**
* **Problem:** Identify any vertical, horizontal, or oblique asymptotes in the graph of $y = f(x)$. State the domain of $f$.
* **Answer:**
  * **Vertical Asymptotes:** **Choice B: There are two vertical asymptotes. The equation of the leftmost one is `x = -2`, and the equation of the rightmost one is `x = 2`.**
  * **Horizontal/Oblique Asymptote:** **Choice A: The function has a horizontal asymptote whose equation is `y = -2`.**
  * **Domain:** `(-\infty, -2) \cup (-2, 2) \cup (2, \infty)`
* **Graph Equation:** `f(x) = (-2x^2 - 8)/(x^2 - 4)`
* **The Rule:** Note the grid scale (each grid line represents $2$ units) to read the dashed asymptote lines accurately.
* **Work:**
  1. Each grid square equals $2$ units. The two vertical dashed lines are $1$ grid unit left and right of the $y$-axis, so they are **`x = -2`** and **`x = 2`**.
  2. The horizontal dashed line is $1$ grid unit below the $x$-axis, so its equation is **`y = -2`**.
  3. The domain excludes $x = -2$ and $x = 2$: **`(-\infty, -2) \cup (-2, 2) \cup (2, \infty)`**.

---

### **Question 23**
* **Problem:** Identify any vertical, horizontal, or oblique asymptotes in the graph of $y = f(x)$. State the domain of $f$.
* **Answer:**
  * **Vertical Asymptotes:** **Choice B: There is no vertical asymptote.**
  * **Horizontal Asymptotes:** **Choice A: $y =$ `-6`**
  * **Oblique Asymptotes:** **Choice B: There is no oblique asymptote.**
  * **Domain:** `(-\infty, \infty)`
* **Graph Equation:** `f(x) = -2/(x^2 + 1) - 6`
* **The Rule:** A continuous curve extending across the entire coordinate plane has no vertical asymptotes and domain $(-\infty, \infty)$.
* **Work:**
  1. The graph has no breaks or vertical asymptotes (**Choice B**).
  2. As $x \to \pm\infty$, the curve flattens along the line $y = -6$, so the horizontal asymptote is $y =$ **`-6`**.
  3. There is no oblique asymptote (**Choice B**), and the domain is **`(-\infty, \infty)`**.

---

### **Question 24**
* **Problem:** Graph the rational function: $f(x) = \frac{x - 7}{x + 2}$
* **Answer:** **Choice D**
* **Graph Equation:** `f(x) = (x - 7)/(x + 2)`
* **The Rule:** Find the vertical asymptote ($x = -2$), horizontal asymptote ($y = 1$), and intercepts ($(7, 0)$ and $(0, -3.5)$) to identify the correct graph.
* **Work:**
  1. **Vertical asymptote:** $x + 2 = 0 \implies x = -2$.
  2. **Horizontal asymptote:** $y = \frac{1}{1} = 1$.
  3. **Intercepts:** $x$-intercept at $(7, 0)$ and $y$-intercept at $(0, -\frac{7}{2}) = (0, -3.5)$.
  4. **Choice D** is the only graph with VA $x = -2$, HA $y = 1$, and the lower-right branch passing through $(0, -3.5)$ and $(7, 0)$.

---

### **Question 25**
* **Problem:** Graph the rational function: $f(x) = \frac{x + 2}{x + 1}$
* **Answer:** **Choice C**
* **Graph Equation:** `f(x) = (x + 2)/(x + 1)`
* **The Rule:** Locate the vertical asymptote ($x = -1$), horizontal asymptote ($y = 1$), $x$-intercept ($(-2, 0)$), and $y$-intercept ($(0, 2)$).
* **Work:**
  1. **Vertical asymptote:** $x = -1$.
  2. **Horizontal asymptote:** $y = 1$.
  3. **Intercepts:** $f(-2) = 0 \implies (-2, 0)$; $f(0) = 2 \implies (0, 2)$.
  4. **Choice C** shows the vertical asymptote at $x = -1$, horizontal asymptote at $y = 1$, left branch below $y = 1$ through $(-2, 0)$, and right branch above $y = 1$ through $(0, 2)$.

---

### **Question 26**
* **Problem:** Graph the rational function: $f(x) = \frac{-4x}{x^2 - 64}$
* **Answer:** **Choice A**
* **Graph Equation:** `f(x) = (-4x)/(x^2 - 64)`
* **The Rule:** Find vertical asymptotes ($x = \pm 8$), horizontal asymptote ($y = 0$), origin intercept $(0, 0)$, and test signs in each interval.
* **Work:**
  1. **Vertical asymptotes:** $x^2 - 64 = 0 \implies x = -8, 8$.
  2. **Horizontal asymptote:** $\deg(\text{num}) = 1 < \deg(\text{den}) = 2 \implies y = 0$.
  3. **Test point:** At $x = 4$, $f(4) = \frac{-16}{16 - 64} = \frac{1}{3} > 0$, so the middle branch rises from $-\infty$ (at $x = -8^+$) through $(0, 0)$ to $+\infty$ (at $x = 8^-$). For $x > 8$, $f(x) < 0$.
  4. This matches **Choice A**.

---

### **Question 27**
* **Problem:** Sketch the graph of the rational function: $f(x) = \frac{(x + 9)(x - 1)}{(x + 1)(x - 4)}$
* **Answer:** **Choice A**
* **Graph Equation:** `f(x) = ((x + 9)(x - 1))/((x + 1)(x - 4))`
* **The Rule:** Identify the vertical asymptotes ($x = -1, 4$), horizontal asymptote ($y = 1$), $x$-intercepts ($x = -9, 1$), and $y$-intercept ($y = \frac{9}{4}$).
* **Work:**
  1. **Vertical asymptotes:** $x = -1$ and $x = 4$ (eliminates B and D).
  2. **$y$-intercept:** $f(0) = \frac{(9)(-1)}{(1)(-4)} = \frac{9}{4} = 2.25 > 0$.
  3. Between $x = -1$ and $x = 4$, the curve comes down from $+\infty$ at $x = -1^+$, passes through $(0, 2.25)$ and $(1, 0)$, and goes to $-\infty$ at $x = 4^-$. This matches **Choice A**.

---

### **Question 28**
* **Problem:** Sketch the graph of the rational function: $f(x) = \frac{4x^2 - 1}{x^2 - 16}$
* **Answer:** **Choice A**
* **Graph Equation:** `f(x) = (4x^2 - 1)/(x^2 - 16)`
* **The Rule:** Use even symmetry ($f(-x) = f(x)$), vertical asymptotes ($x = \pm 4$), horizontal asymptote ($y = 4$), and test values in $(-4, 4)$ and $(4, \infty)$.
* **Work:**
  1. **Vertical asymptotes:** $x = -4, 4$. **Horizontal asymptote:** $y = 4$.
  2. **$y$-intercept:** $f(0) = \frac{-1}{-16} = \frac{1}{16} > 0$, and at $x = 2$, $f(2) = \frac{15}{-12} = -1.25 < 0$, so the middle branch opens downward toward $-\infty$.
  3. For $|x| > 4$ (e.g., $x = 5$), $f(5) = \frac{99}{9} = 11 > 4$, so the outer branches lie above $y = 4$. This matches **Choice A**.

---

### **Question 29**
* **Problem:** Graph the rational function: $f(x) = \frac{(x + 6)(x - 7)}{(x - 5)^2}$
* **Answer:** **Choice B**
* **Graph Equation:** `f(x) = ((x + 6)(x - 7))/((x - 5)^2)`
* **The Rule:** At a vertical asymptote of even multiplicity, the graph approaches the same infinity ($+\infty$ or $-\infty$) on both sides.
* **Work:**
  1. **Vertical asymptote:** $x = 5$ (eliminates A and D). **Horizontal asymptote:** $y = 1$.
  2. Near $x = 5$, the numerator approaches $(5 + 6)(5 - 7) = -22 < 0$, while the denominator $(x - 5)^2 > 0$ on both sides.
  3. Thus, $f(x) \to -\infty$ as $x \to 5^-$ and as $x \to 5^+$. This matches **Choice B**.

---

### **Question 30**
* **Problem:** Graph the rational function: $f(x) = \frac{-2x}{x^2 - 9}$
* **Answer:** **Choice B**
* **Graph Equation:** `f(x) = (-2x)/(x^2 - 9)`
* **The Rule:** Locate vertical asymptotes ($x = \pm 3$), horizontal asymptote ($y = 0$), and check sign behavior on $(-3, 3)$ and $(3, \infty)$.
* **Work:**
  1. **Vertical asymptotes:** $x = -3, 3$. **Horizontal asymptote:** $y = 0$.
  2. At $x = 1$, $f(1) = \frac{-2}{-8} = \frac{1}{4} > 0$, so the middle branch rises from $-\infty$ through $(0, 0)$ to $+\infty$.
  3. At $x = 4$, $f(4) = \frac{-8}{7} < 0$ (below $x$-axis for $x > 3$), and by odd symmetry $f(x) > 0$ for $x < -3$. This matches **Choice B**.

---

### **Question 31**
* **Problem:** Graph the rational function: $f(x) = \frac{3}{x^2 + 2}$
* **Answer:** **Choice A**
* **Graph Equation:** `f(x) = 3/(x^2 + 2)`
* **The Rule:** Since $x^2 + 2 \ge 2 > 0$ for all real $x$, the graph is a smooth, symmetric, positive bell-shaped curve with horizontal asymptote $y = 0$ and peak at $(0, 1.5)$.
* **Work:**
  1. No vertical asymptotes (eliminates B and D).
  2. $f(0) = \frac{3}{2} = 1.5 > 0$, and $f(x) > 0$ for all $x$, which matches **Choice A**.

---

### **Question 32**
* **Problem:** Sketch the graph of the rational function: $f(x) = \frac{4x^2 - 16}{x^2 - 5x + 6}$
* **Answer:** **Choice B**
* **Graph Equation:** `f(x) = (4x^2 - 16)/(x^2 - 5x + 6)`
* **The Rule:** Factor and cancel common terms to find the hole, then graph the simplified rational function with its vertical and horizontal asymptotes.
* **Work:**
  1. Factor numerator and denominator:
     $$f(x) = \frac{4(x - 2)(x + 2)}{(x - 2)(x - 3)} = \frac{4(x + 2)}{x - 3}, \quad x \neq 2$$
  2. **Vertical asymptote:** $x = 3$. **Horizontal asymptote:** $y = 4$.
  3. **Hole:** At $x = 2$, $y = \frac{4(2 + 2)}{2 - 3} = -16$, so there is an open circle at $(2, -16)$ just to the left of the vertical asymptote $x = 3$. This matches **Choice B**.

---

### **Question 33**
* **Problem:** Find an equation for the rational function graphed below.
* **Answer:** `f(x) = ((x + 1)(x - 2))/((x + 3)(x - 2))` (or expanded form `(x^2 - x - 2)/(x^2 + x - 6)`)
* **Graph Equation:** `f(x) = ((x + 1)(x - 2))/((x + 3)(x - 2))`
* **The Rule:** Build the rational function from its vertical asymptote ($x = -3$), horizontal asymptote ($y = 1$), $x$-intercept ($(-1, 0)$), and removable discontinuity (hole at $x = 2$).
* **Work:**
  1. **Vertical asymptote at $x = -3$:** Denominator has factor $(x + 3)$.
  2. **$x$-intercept at $(-1, 0)$:** Numerator has factor $(x + 1)$.
  3. **Horizontal asymptote at $y = 1$:** Leading coefficient ratio is $1$, giving the base function $g(x) = \frac{x + 1}{x + 3}$ (which also passes through $(-4, 3)$, $(-2, -1)$, and $(0, \frac{1}{3})$).
  4. **Hole at $x = 2$:** The open circle on the graph is at $x = 2$ ($y = \frac{2 + 1}{2 + 3} = \frac{3}{5}$), so multiply both numerator and denominator by $(x - 2)$:
     $$f(x) = \frac{(x + 1)(x - 2)}{(x + 3)(x - 2)} = \frac{x^2 - x - 2}{x^2 + x - 6}$$

---

### **Question 34**
* **Problem:** Find an equation for the rational function graph.
* **Answer:** **`f(x) = (x - 1)/(x(x - 5))`** (3rd choice)
* **Graph Equation:** `f(x) = (x - 1)/(x*(x - 5))`
* **The Rule:** Match the vertical asymptotes ($x = 0$ and $x = 5$), $x$-intercept ($(1, 0)$), and horizontal asymptote ($y = 0$).
* **Work:**
  1. **Vertical asymptotes:** The graph has vertical asymptotes at $x = 0$ (the $y$-axis) and $x = 5$, so the denominator is $x(x - 5)$.
  2. **$x$-intercept:** The graph crosses the $x$-axis at $(1, 0)$, so the numerator is $x - 1$.
  3. **Horizontal asymptote:** $y = 0$, since $\deg(\text{num}) = 1 < \deg(\text{den}) = 2$.
  4. Combining these gives **$f(x) = \frac{x - 1}{x(x - 5)}$**.

---

### **Question 35**
* **Problem:** Find a possible equation for the function with a graph having the given features: $x$-intercepts $(-5, 0)$ and $(3, 0)$, $y$-intercept $(0, -15)$, vertical asymptote $x = 1$, horizontal asymptote $y = 1$.
* **Answer:** **`f(x) = ((x - 3)(x + 5))/(x - 1)^2`** (4th choice)
* **Graph Equation:** `f(x) = ((x - 3)(x + 5))/((x - 1)^2)`
* **The Rule:** Use the $x$-intercepts for numerator factors, the vertical asymptote for the denominator factor, and match the degrees and $y$-intercept.
* **Work:**
  1. **$x$-intercepts $(-5, 0)$ and $(3, 0)$:** Numerator has factors $(x - 3)(x + 5)$ (degree $2$).
  2. **Vertical asymptote $x = 1$ and Horizontal asymptote $y = 1$:** Denominator must also have degree $2$ with leading coefficient $1$, so the denominator is $(x - 1)^2$.
  3. **Verify $y$-intercept:** $f(0) = \frac{(-3)(5)}{(-1)^2} = -15$, which matches $(0, -15)$.

---

### **Question 36**
* **Problem:** Use the graph of the rational function to complete the following statement: As $x \to 3^-$, $f(x) \to$ ____.
* **Answer:** `\infty`
* **The Rule:** Follow the curve as $x$ approaches $3$ from the left side ($x < 3$) and observe whether $y$ goes to $\infty$ or $-\infty$.
* **Work:**
  1. Locate the vertical asymptote at $x = 3$.
  2. Just to the left of $x = 3$ ($x \to 3^-$), the graph rises upward without bound, so $f(x) \to \infty$.

---

### **Question 37**
* **Problem:** Use the graph of the rational function to complete the following statement: As $x \to -\infty$, $f(x) \to$ ____.
* **Answer:** `0`
* **The Rule:** As $x \to -\infty$, $f(x)$ approaches the horizontal asymptote on the far left of the graph.
* **Work:**
  1. Follow the graph to the far left ($x \to -\infty$).
  2. The curve flattens out along the $x$-axis ($y = 0$), so $f(x) \to 0$.

---

### **Question 38**
* **Problem:** Use the graph of the rational function to complete the following statement: As $x \to 2^-$, $f(x) \to$ ____.
* **Answer:** `-\infty`
* **The Rule:** Follow the graph as $x$ approaches the vertical asymptote $x = 2$ from the left side ($x < 2$).
* **Work:**
  1. Locate the vertical asymptote $x = 2$.
  2. On the left side of $x = 2$ ($x \to 2^-$), the middle branch plunges downward without bound, so $f(x) \to -\infty$.

---

### **Question 39**
* **Problem:** Use the graph of the rational function to complete the following statement: As $x \to -2^+$, $f(x) \to$ ____.
* **Answer:** `\infty`
* **The Rule:** Follow the graph as $x$ approaches the vertical asymptote $x = -2$ from the right side ($x > -2$).
* **Work:**
  1. Locate the vertical asymptote $x = -2$.
  2. Immediately to the right of $x = -2$ ($x \to -2^+$), the curve shoots upward without bound, so $f(x) \to \infty$.

---

### **Question 40**
* **Problem:** Use the graph of the rational function to complete the following statement: As $x \to \infty$, $f(x) \to$ ____.
* **Answer:** `3`
* **The Rule:** As $x \to \infty$, a rational function approaches its horizontal asymptote $y = b$.
* **Work:**
  1. The problem states and shows the horizontal asymptote is $y = 3$.
  2. As $x \to \infty$, the right branch approaches $y = 3$, so $f(x) \to 3$.

---

### **Question 41**
* **Problem:** Use the graph of the rational function to complete the following statement: As $x \to -2^-$, $f(x) \to$ ____.
* **Answer:** `\infty`
* **The Rule:** Follow the curve as $x$ approaches $x = -2$ from the left side ($x < -2$).
* **Work:**
  1. Locate the vertical asymptote at $x = -2$.
  2. As $x$ approaches $-2$ from the left ($x \to -2^-$), the left branch rises upward without bound, so $f(x) \to \infty$.
