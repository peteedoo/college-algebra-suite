# **Build Understanding 9.5: Nonlinear System of Equations - Answer Sheet**

**Course:** MAT1340003 College Algebra: MA1 (Steven Yamiolkoski) FA26  
**Assignment:** Build Understanding 9.5 Nonlinear System of Equations

---

### **Question 1**
* **Problem:** A nonlinear system is given below, and the graphs of both equations in the system are shown to the right. Verify that the points of intersection specified on the graph are solutions of the system by substituting directly into both equations.
  $$\begin{aligned} x^2 &= y - 1 \\ y &= 2x + 4 \end{aligned}$$
  * Verify for the point $(3, 10)$.
  * Verify for the point $(-1, 2)$.
* **Answer:**
  * **Point $(3, 10)$:**
    * $x^2 = y - 1 \rightarrow ($**`3`**$)^2 \stackrel{?}{=}$ **`10`** $- 1$
    * $y = 2x + 4 \rightarrow$ **`10`** $\stackrel{?}{=} 2($**`3`**$) + 4$
    * Does the solution check? **`Yes`**
  * **Point $(-1, 2)$:**
    * $x^2 = y - 1 \rightarrow ($**`-1`**$)^2 \stackrel{?}{=}$ **`2`** $- 1$
    * $y = 2x + 4 \rightarrow$ **`2`** $\stackrel{?}{=} 2($**`-1`**$) + 4$
    * Does the solution check? **`Yes`**
* **Graph Equation:** `x^2 = y - 1; y = 2x + 4`
* **The Rule:** A point $(x, y)$ is a solution of a system if substituting its coordinates into each equation produces a true statement.
* **Work:**
  1. For $(3, 10)$:
     * $(3)^2 = 10 - 1 \implies 9 = 9$ (True)
     * $10 = 2(3) + 4 \implies 10 = 10$ (True)
  2. For $(-1, 2)$:
     * $(-1)^2 = 2 - 1 \implies 1 = 1$ (True)
     * $2 = 2(-1) + 4 \implies 2 = 2$ (True)

---

### **Question 2**
* **Problem:** A nonlinear system is given, along with the graphs of both equations in the system. Verify that the points of intersection specified on the graph, $(-1, -2)$ and $\left(\frac{2}{5}, \frac{11}{5}\right)$, are solutions of the system by substituting directly into both equations:
  $$\begin{aligned} x^2 + y^2 &= 5 \\ 21x - 7y &= -7 \end{aligned}$$
* **Answer:**
  * For $(-1, -2)$ in first equation: $x^2 + y^2 =$ **`5`**
  * For $(-1, -2)$ in second equation: $21x - 7y =$ **`-7`**
  * For $\left(\frac{2}{5}, \frac{11}{5}\right)$ in first equation: $x^2 + y^2 =$ **`5`**
  * For $\left(\frac{2}{5}, \frac{11}{5}\right)$ in second equation: $21x - 7y =$ **`-7`**
  * Are the points of intersection specified on the graph the solutions of the system? **`Yes`**
* **Graph Equation:** `x^2 + y^2 = 5; 21x - 7y = -7`
* **The Rule:** Substitute each ordered pair $(x, y)$ into the left-hand side of both equations and simplify.
* **Work:**
  1. Substitute $(-1, -2)$:
     * $x^2 + y^2 = (-1)^2 + (-2)^2 = 1 + 4 = 5$
     * $21x - 7y = 21(-1) - 7(-2) = -21 + 14 = -7$
  2. Substitute $\left(\frac{2}{5}, \frac{11}{5}\right)$:
     * $x^2 + y^2 = \left(\frac{2}{5}\right)^2 + \left(\frac{11}{5}\right)^2 = \frac{4}{25} + \frac{121}{25} = \frac{125}{25} = 5$
     * $21x - 7y = 21\left(\frac{2}{5}\right) - 7\left(\frac{11}{5}\right) = \frac{42 - 77}{5} = \frac{-35}{5} = -7$

---

### **Question 3**
* **Problem:** How can we tell, before doing any work, that the below system cannot have more than two solutions?
  $$\begin{aligned} x^2 - y &= 4 \\ x + y &= -2 \end{aligned}$$
* **Answer:** **Choice A: Consider the graphs; a line and a parabola cannot intersect in more than two points.**
* **Graph Equation:** `x^2 - y = 4; x + y = -2`
* **The Rule:** The first equation represents a parabola and the second represents a line; geometrically, a line can intersect a parabola in at most two points.
* **Work:**
  1. $x^2 - y = 4 \implies y = x^2 - 4$ is a parabola.
  2. $x + y = -2 \implies y = -x - 2$ is a line.
  3. A line and a parabola can intersect in at most two points (**Choice A**).

---

### **Question 4**
* **Problem:** Fill in the blank. When solving
  $$\begin{cases} x^2 - 3y = 3 \\ x + y = -1 \end{cases}$$
  by the substitution method, we obtain $x = -3$ or $x = 0$, so the solution set is `{____}`.
* **Answer:** **`(-3, 2), (0, -1)`**
* **Graph Equation:** `x^2 - 3y = 3; x + y = -1`
* **The Rule:** Substitute each found $x$-value back into the linear equation $x + y = -1$ to find its corresponding $y$-value, and write each solution as an ordered pair $(x, y)$.
* **Work:**
  1. From $x + y = -1$, we have $y = -1 - x$.
  2. For $x = -3$: $y = -1 - (-3) = 2 \implies (-3, 2)$.
  3. For $x = 0$: $y = -1 - 0 = -1 \implies (0, -1)$.
  4. Solution set: $\{(-3, 2), (0, -1)\}$.

---

### **Question 5**
* **Problem:** Fill in the blanks so that the resulting statement is true. When solving
  $$\begin{cases} 4x^2 + 3y^2 = 36 \\ 6x^2 + 4y^2 = 49 \end{cases}$$
  by the addition method, we can eliminate $x^2$ by multiplying the first equation by **(1)** `____` and the second equation by **(2)** `____` and then adding the equations.
  * Choices for (1): `-6`, `3`, `4`
  * Choices for (2): `4,`, `36,`, `3,`
* **Answer:** **(1) `-6`**, **(2) `4,`**
* **Graph Equation:** `4x^2 + 3y^2 = 36; 6x^2 + 4y^2 = 49`
* **The Rule:** Multiply the two equations by constants so the coefficients of $x^2$ become opposites (such as $-24$ and $+24$).
* **Work:**
  1. Multiplying the first equation by **$-6$** gives $-24x^2 - 18y^2 = -216$.
  2. Multiplying the second equation by **$4$** gives $24x^2 + 16y^2 = 196$.
  3. Adding them eliminates $x^2$.

---

### **Question 6**
* **Problem:** Give all solutions of the nonlinear system of equations, including those with nonreal complex components.
  $$\begin{aligned} x^2 - y &= 0 \\ 2x + y &= 8 \end{aligned}$$
* **Answer:** **Choice A: The solution set is `{(-4, 16), (2, 4)}`.**
* **Graph Equation:** `x^2 - y = 0; 2x + y = 8`
* **The Rule:** Solve the first equation for $y$ ($y = x^2$) and substitute into the second equation.
* **Work:**
  1. From the first equation: $y = x^2$.
  2. Substitute into the second equation:
     $$2x + x^2 = 8 \implies x^2 + 2x - 8 = 0 \implies (x + 4)(x - 2) = 0$$
  3. Thus $x = -4$ or $x = 2$.
  4. Find $y = x^2$:
     * For $x = -4$: $y = (-4)^2 = 16 \implies (-4, 16)$
     * For $x = 2$: $y = (2)^2 = 4 \implies (2, 4)$

---

### **Question 7**
* **Problem:** Give all solutions of the nonlinear system of equations, including those with nonreal complex components.
  $$\begin{aligned} y &= x^2 + 5x \\ 2x - y &= -10 \end{aligned}$$
* **Answer:** **Choice A: The solution set is `{(-5, 0), (2, 14)}`.**
* **Graph Equation:** `y = x^2 + 5x; 2x - y = -10`
* **The Rule:** Substitute $y = x^2 + 5x$ into the linear equation and solve the resulting quadratic equation.
* **Work:**
  1. Substitute $y = x^2 + 5x$ into $2x - y = -10$:
     $$2x - (x^2 + 5x) = -10 \implies -x^2 - 3x = -10 \implies x^2 + 3x - 10 = 0$$
  2. Factor:
     $$(x + 5)(x - 2) = 0 \implies x = -5 \text{ or } x = 2$$
  3. Find $y = 2x + 10$:
     * For $x = -5$: $y = 2(-5) + 10 = 0 \implies (-5, 0)$
     * For $x = 2$: $y = 2(2) + 10 = 14 \implies (2, 14)$

---

### **Question 8**
* **Problem:** Give all solutions of the nonlinear system of equations, including those with nonreal complex components.
  $$\begin{aligned} 3x^2 + 2y^2 &= 2 \\ x - y &= -1 \end{aligned}$$
* **Answer:** **Choice A: The solution set is `{(0, 1), (-4/5, 1/5)}`.**
* **Graph Equation:** `3x^2 + 2y^2 = 2; x - y = -1`
* **The Rule:** Solve the linear equation for $y$ ($y = x + 1$) and substitute into the quadratic equation.
* **Work:**
  1. From the second equation: $y = x + 1$.
  2. Substitute into the first equation:
     $$3x^2 + 2(x + 1)^2 = 2 \implies 3x^2 + 2(x^2 + 2x + 1) = 2 \implies 5x^2 + 4x + 2 = 2$$
  3. Simplify and factor:
     $$5x^2 + 4x = 0 \implies x(5x + 4) = 0 \implies x = 0 \text{ or } x = -\frac{4}{5}$$
  4. Find $y = x + 1$:
     * For $x = 0$: $y = 0 + 1 = 1 \implies (0, 1)$
     * For $x = -\frac{4}{5}$: $y = -\frac{4}{5} + 1 = \frac{1}{5} \implies \left(-\frac{4}{5}, \frac{1}{5}\right)$

---

### **Question 9**
* **Problem:** Give all solutions of the nonlinear system of equations, including those with nonreal complex components.
  $$\begin{aligned} 6x^2 + y^2 &= 42 \\ 36x^2 - y^2 &= 0 \end{aligned}$$
* **Answer:** **Choice A: The solution set is `{(1, 6), (1, -6), (-1, 6), (-1, -6)}`.**
* **Graph Equation:** `6x^2 + y^2 = 42; 36x^2 - y^2 = 0`
* **The Rule:** Add the two equations to eliminate $y^2$, solve for $x$, and then find all corresponding values of $y$.
* **Work:**
  1. Add the two equations:
     $$42x^2 = 42 \implies x^2 = 1 \implies x = \pm 1$$
  2. Substitute $x^2 = 1$ into $36x^2 - y^2 = 0$:
     $$36(1) - y^2 = 0 \implies y^2 = 36 \implies y = \pm 6$$
  3. Combining all signs gives four solutions: $(1, 6), (1, -6), (-1, 6), (-1, -6)$.

---

### **Question 10**
* **Problem:** Give all solutions of the nonlinear system of equations, including those with nonreal complex components.
  $$\begin{aligned} 2x^2 + 5y^2 &= 22 \\ 5x^2 - 4y^2 &= -11 \end{aligned}$$
* **Answer:** **Choice A: The solution set is `{(1, 2), (1, -2), (-1, 2), (-1, -2)}`.**
* **Graph Equation:** `2x^2 + 5y^2 = 22; 5x^2 - 4y^2 = -11`
* **The Rule:** Use the addition (elimination) method to eliminate $y^2$ or $x^2$.
* **Work:**
  1. Multiply the first equation by $4$ and the second by $5$:
     $$\begin{aligned} 8x^2 + 20y^2 &= 88 \\ 25x^2 - 20y^2 &= -55 \end{aligned}$$
  2. Add the equations:
     $$33x^2 = 33 \implies x^2 = 1 \implies x = \pm 1$$
  3. Substitute $x^2 = 1$ into $2x^2 + 5y^2 = 22$:
     $$2(1) + 5y^2 = 22 \implies 5y^2 = 20 \implies y^2 = 4 \implies y = \pm 2$$
  4. All four combinations give $(1, 2), (1, -2), (-1, 2), (-1, -2)$.

---

### **Question 11**
* **Problem:** Solve the system by the addition method.
  $$\begin{cases} x^2 - 5y^2 = -19 \\ 2x^2 + y^2 = 6 \end{cases}$$
* **Answer:** **`(1, 2), (1, -2), (-1, 2), (-1, -2)`**
* **Graph Equation:** `x^2 - 5y^2 = -19; 2x^2 + y^2 = 6`
* **The Rule:** Multiply the second equation by $5$ and add to the first equation to eliminate $y^2$.
* **Work:**
  1. Multiply the second equation by $5$:
     $$10x^2 + 5y^2 = 30$$
  2. Add to the first equation ($x^2 - 5y^2 = -19$):
     $$11x^2 = 11 \implies x^2 = 1 \implies x = \pm 1$$
  3. Substitute $x^2 = 1$ into $2x^2 + y^2 = 6$:
     $$2(1) + y^2 = 6 \implies y^2 = 4 \implies y = \pm 2$$
  4. Solution set: $\{(1, 2), (1, -2), (-1, 2), (-1, -2)\}$.

---

### **Question 12**
* **Problem:** Solve the problem using a system of equations in two variables. Find two positive numbers whose squares have a sum of $113$ and a difference of $15$.
* **Answer:** **`8, 7`** (or `7, 8`)
* **Graph Equation:** `x^2 + y^2 = 113; x^2 - y^2 = 15`
* **The Rule:** Let the two positive numbers be $x$ and $y$, set up the system $x^2 + y^2 = 113$ and $x^2 - y^2 = 15$, and solve by addition.
* **Work:**
  1. Add the two equations:
     $$(x^2 + y^2) + (x^2 - y^2) = 113 + 15 \implies 2x^2 = 128 \implies x^2 = 64$$
  2. Since $x > 0$, $x = 8$.
  3. Substitute $x^2 = 64$ into $x^2 + y^2 = 113$:
     $$64 + y^2 = 113 \implies y^2 = 49$$
  4. Since $y > 0$, $y = 7$.

---

### **Question 13**
* **Problem:** Does the straight line $3x - 2y = 18$ intersect the circle $x^2 + y^2 = 25$? *(Hint: To find out, solve the system formed by these two equations.)* Do the graphs of the two equations intersect?
* **Answer:** **`Yes`** (Second radio button choice — the line and circle intersect at $(4, -3)$ and $\left(\frac{56}{13}, -\frac{33}{13}\right)$)
* **Graph Equation:** `3x - 2y = 18; x^2 + y^2 = 25`
* **The Rule:** Two graphs intersect if and only if the system of their equations has at least one real solution (discriminant $\Delta \ge 0$).
* **Work:**
  1. Solve the linear equation for $y$: $y = \frac{3x - 18}{2}$.
  2. Substitute into the circle equation:
     $$x^2 + \left(\frac{3x - 18}{2}\right)^2 = 25 \implies 4x^2 + (9x^2 - 108x + 324) = 100 \implies 13x^2 - 108x + 224 = 0$$
  3. Compute the discriminant $\Delta = b^2 - 4ac$:
     $$\Delta = (-108)^2 - 4(13)(224) = 11,664 - 11,648 = 16 > 0$$
  4. Since $\Delta = 16 > 0$, the line intersects the circle at two real points: $(4, -3)$ and $\left(\frac{56}{13}, -\frac{33}{13}\right)$.
