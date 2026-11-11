# **Pre-work 9.5: Systems of Non-Linear Equations - Answer Sheet**

**Course:** MAT1340003 College Algebra: MA1 (Steven Yamiolkoski) FA26  
**Assignment:** Pre-work 9.5 Systems of Non-Linear Equations

---

### **Question 1**
* **Problem:** If a list of equations of circles, parabolas, ellipses, and hyperbolas is given, explain how to distinguish the different conic sections from their equations.
* **Answer:** **Choice A: If there are both $x^2$- and $y^2$-terms on one side of equation with the same signs and coefficients, then this is an equation of a circle. If the coefficients are different, then this is an equation of an ellipse. If the signs are different, then this is an equation of a hyperbola. If there is only an $x^2$-term or an $y^2$-term, then this is an equation of a parabola.**
* **The Rule:** For $Ax^2 + Cy^2 + Dx + Ey + F = 0$:
  * Circle: $A = C$ (same sign and same coefficient)
  * Ellipse: $A \neq C$ with the same sign ($AC > 0$)
  * Hyperbola: $A$ and $C$ have opposite signs ($AC < 0$)
  * Parabola: Either $A = 0$ or $C = 0$ (only one squared term)
* **Work:**
  1. Comparing the classification rules to the options, **Choice A** accurately states all four conditions.

---

### **Question 2**
* **Problem:** Identify the type of conic section represented by each of the equations. Drag each of the equations given into the appropriate area below, depending on whether it represents a parabola, circle, ellipse, or hyperbola:
  $$\frac{x^2}{64} + \frac{y^2}{64} = 1, \quad \frac{x^2}{11} + \frac{y^2}{25} = 1, \quad \frac{x^2}{16} + \frac{y^2}{16} = 1, \quad \frac{y^2}{36} - \frac{x^2}{41} = 1, \quad \frac{x^2}{49} - \frac{y^2}{19} = 1, \quad \frac{x^2}{144} + \frac{y^2}{123} = 1, \quad \frac{x^2}{16} - \frac{y^2}{67} = 1, \quad \frac{x^2}{36} + \frac{y^2}{16} = 1$$
* **Answer:**
  * **Parabola:** *(None of the given equations)*
  * **Circle:** **`x^2/64 + y^2/64 = 1`**, **`x^2/16 + y^2/16 = 1`**
  * **Ellipse:** **`x^2/11 + y^2/25 = 1`**, **`x^2/144 + y^2/123 = 1`**, **`x^2/36 + y^2/16 = 1`**
  * **Hyperbola:** **`y^2/36 - x^2/41 = 1`**, **`x^2/49 - y^2/19 = 1`**, **`x^2/16 - y^2/67 = 1`**
* **Graph Equation:** `x^2/36 + y^2/16 = 1`
* **The Rule:** Sum of squares with equal denominators is a circle; sum of squares with unequal denominators is an ellipse; difference of squares is a hyperbola.
* **Work:**
  1. **Circles** (both positive, equal denominators): $\frac{x^2}{64} + \frac{y^2}{64} = 1$ and $\frac{x^2}{16} + \frac{y^2}{16} = 1$.
  2. **Ellipses** (both positive, different denominators): $\frac{x^2}{11} + \frac{y^2}{25} = 1$, $\frac{x^2}{144} + \frac{y^2}{123} = 1$, and $\frac{x^2}{36} + \frac{y^2}{16} = 1$.
  3. **Hyperbolas** (opposite signs / subtraction): $\frac{y^2}{36} - \frac{x^2}{41} = 1$, $\frac{x^2}{49} - \frac{y^2}{19} = 1$, and $\frac{x^2}{16} - \frac{y^2}{67} = 1$.

---

### **Question 3**
* **Problem:** What is the maximum number of times that a line can intersect an ellipse?
* **Answer:** **Choice A: `2`**
* **The Rule:** A linear equation (degree 1) and a conic section (degree 2) can intersect at most $1 \times 2 = 2$ times.
* **Work:**
  1. Substituting a linear equation into a quadratic equation in two variables yields a quadratic equation in one variable, which has at most **2** real solutions.

---

### **Question 4**
* **Problem:** What is the maximum number of times that a parabola can intersect an ellipse?
* **Answer:** **`4 times`** (Fourth radio button choice)
* **The Rule:** Two distinct conic sections (each of degree 2) can intersect at most $2 \times 2 = 4$ times.
* **Work:**
  1. A parabola and an ellipse can cross each other in at most **4** points.

---

### **Question 5**
* **Problem:** Fill in the blank to correctly complete the sentence. The following nonlinear system has two solutions, one of which is $(1, \text{____})$.
  $$\begin{aligned} x + y &= 4 \\ x^2 + y^2 &= 10 \end{aligned}$$
* **Answer:** **`3`** (One of the solutions of the system is `(1, 3)`)
* **Graph Equation:** `x + y = 4; x^2 + y^2 = 10`
* **The Rule:** Substitute the given $x$-value into the linear equation and verify in the nonlinear equation.
* **Work:**
  1. Substitute $x = 1$ into $x + y = 4$:
     $$1 + y = 4 \implies y = 3$$
  2. Check in $x^2 + y^2 = 10$:
     $$1^2 + 3^2 = 1 + 9 = 10 \quad \checkmark$$

---

### **Question 6**
* **Problem:** Fill in the blank to correctly complete the sentence. The following nonlinear system has two solutions with real components, one of which is $(2, \text{____})$.
  $$\begin{aligned} y &= x^2 + 2 \\ x^2 - y^2 &= -32 \end{aligned}$$
* **Answer:** **`6`** (One of the solutions of the system is `(2, 6)`)
* **Graph Equation:** `y = x^2 + 2; x^2 - y^2 = -32`
* **The Rule:** Substitute $x = 2$ into $y = x^2 + 2$ and verify that $(x, y)$ satisfies $x^2 - y^2 = -32$.
* **Work:**
  1. Substitute $x = 2$ into $y = x^2 + 2$:
     $$y = 2^2 + 2 = 4 + 2 = 6$$
  2. Check in $x^2 - y^2 = -32$:
     $$2^2 - 6^2 = 4 - 36 = -32 \quad \checkmark$$

---

### **Question 7**
* **Problem:** Fill in the blank to correctly complete the sentence. The following nonlinear system has two solutions, one of which is $(\text{____}, 9)$.
  $$\begin{aligned} 2x + y &= 3 \\ x^2 + y^2 &= 90 \end{aligned}$$
* **Answer:** **`-3`** (One of the solutions of the system is `(-3, 9)`)
* **Graph Equation:** `2x + y = 3; x^2 + y^2 = 90`
* **The Rule:** Substitute $y = 9$ into the linear equation to solve for $x$.
* **Work:**
  1. Substitute $y = 9$ into $2x + y = 3$:
     $$2x + 9 = 3 \implies 2x = -6 \implies x = -3$$
  2. Check in $x^2 + y^2 = 90$:
     $$(-3)^2 + 9^2 = 9 + 81 = 90 \quad \checkmark$$

---

### **Question 8**
* **Problem:** The following nonlinear system has two solutions. One solution with real components has $x$-value $-1$. What is the $y$-value of this solution?
  $$\begin{aligned} y &= x^2 + 4 \\ x^2 - y^2 &= -24 \end{aligned}$$
* **Answer:** **`5`**
* **Graph Equation:** `y = x^2 + 4; x^2 - y^2 = -24`
* **The Rule:** Substitute $x = -1$ into $y = x^2 + 4$.
* **Work:**
  1. Substitute $x = -1$ into $y = x^2 + 4$:
     $$y = (-1)^2 + 4 = 1 + 4 = 5$$
  2. Check in $x^2 - y^2 = -24$:
     $$(-1)^2 - 5^2 = 1 - 25 = -24 \quad \checkmark$$

---

### **Question 9**
* **Problem:** To solve the following nonlinear system by substitution and to solve equation (2) for $y$, what will be the resulting equation when the substitution is made into equation (1)?
  $$\begin{aligned} x^2 + y &= 14 \quad &(1) \\ x - y &= 0 \quad &(2) \end{aligned}$$
* **Answer:** **`x^2 + x = 14`**
* **Graph Equation:** `x^2 + y = 14; x - y = 0`
* **The Rule:** Solve equation (2) for $y$ in terms of $x$, then replace $y$ in equation (1) with that expression.
* **Work:**
  1. Solve equation (2) for $y$:
     $$x - y = 0 \implies y = x$$
  2. Substitute $y = x$ into equation (1):
     $$x^2 + x = 14$$

---

### **Question 10**
* **Problem:** To solve the following nonlinear system by eliminating $y^2$-terms, what number should equation (2) be multiplied by?
  $$\begin{aligned} x^2 + 4y^2 &= 3 \quad &(1) \\ x^2 - y^2 &= 0 \quad &(2) \end{aligned}$$
* **Answer:** **`4`**
* **Graph Equation:** `x^2 + 4y^2 = 3; x^2 - y^2 = 0`
* **The Rule:** Multiply equation (2) by a constant so that the coefficient of $y^2$ becomes the opposite of $+4$.
* **Work:**
  1. Equation (1) has $+4y^2$ and equation (2) has $-1y^2$.
  2. Multiplying equation (2) by **$4$** gives $4x^2 - 4y^2 = 0$, which eliminates $y^2$ when added to equation (1).
