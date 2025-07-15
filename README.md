# About magma-diffalg

(NOTE: This file can be edited with Typora or the github editor) 

There are two implementations of differential polynomials in the package. There is one that uses differential monomials (`RngDiffPol`) and one based on pronlongations sequences which are essentially collections of polynomial rings with inclusion and derivations between them (`RngMPolProlSeq`). 

Each of these two types has a corresponding element tupe with an `Elt` appended to the end. Currently, `RngDiffPol` is only implemented with a constant base but `RngMPolProlSeq` can have a base which is a differential ring. 

Also term order associated with block rankings are implemented in the prolongation sequences version. 

# Contents


1. [Example: Instantiating Basic Objects](###example-instantiating-basic-objects)
2. [Example: Linear Differential Equations and Weyl Algebra Element Sequences](###example-linear-differential-equations-and-weyl-algebra-element-sequences)
3. [Example: Weyl Algebras](example-weyl-algebras)
4. [Example: Weyl Algebra Division Algorithm Over A Field](example-weil-algebra-division-algorithm-over-a-field)
5. [Example: Truncating to Polynomial Rings of Finite Order](example-truncating-to-polynomial-rings-of-finite-order)
6. [Example: Leading Monomials, Leaders, Separants, Initials, TopCoeff](example-leading-monomials-leaders-separants-initials-topcoeff)
7. [Example: Eltseq and Coercion](example-eltseq-and-coercion)
8. [Example: Evaluation of Differential Polynomials](example-evaluation-of-differential-polynomials)
9. [Example: Specialization of Coefficients of Differential Polynomials](example-specialization-of-coefficients-of-differential-polynomials)
10. [Example: Polynomial Pseudodivision](example-polynomial-pseudodivision)
11. [Example: Ritt's Division Algorithm](example-ritts-division-algorithm)
12. [Example: Element Comparison and Sorting](example-element-comparison-and-sorting)
13. [Example: Characteristic Sets and Pseudodivision for Polynomial Rings](example-characteristic-sets-and-pseudodivision-for-polynomial-rings)
14. [Example: Characteristic Sets and Pseudodivision for RngMPolProlSeq](example-characteristic-sets-and-pseudodivision-for-rngmpolprolseq)
15. [Example: The Rosenfeld-Groebner Algorithm](example-the-rosenfeld-groebner-algorithm)
16. [Example: Ollivier's Division Algorithm](example-olliviers-division-algorithm)
17. [Example: Evaluation of Free Algebra Elements into Weyl Algebras](example-evaluation-of-free-algebra-elements-into-weyl-algebras)
18. [Example: LaTeX](example-latex)
19. [Example: Differential Rings of Differential Prime Ideals](example-differential-rings-of-differential-prime-ideals)
20. [Example: Magma Enhancement, Quotients of Quotients](example-magma-enhancement-quotients-of-quotients)
21. [Example: Linearizing Differential equations](example-linearizing-differential-equations)
22. [Example: Strictly and Weakly Increasing Sequences](example-strictly-and-weakly-increasing-sequences)
23. [Example: Homogeneous Differential Polynomials](example-homogeneous-differential-polynomials)
24. [Example: Compactified Jet Spaces of Projective Space](example-compactified-jet-spaces-of-projective-space)


# Examples


### Example: Instatiating Basic Objects

Here is how you instantiate the basic objects. 

```
AttachSpec("diffalg.spec");
Z:=Integers();
Q:=RationalField();

R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
f1:=x^2+Diff(y,2)*Diff(x,1)+t;
f2:=Diff(x,1)+Diff(y,3);
```


### Example: Linear Differential Equations and Weyl Algebra Element Sequences

We attach and setup as normal.
```
AttachSpec("diffalg.spec");
Z:=Integers();
Q:=RationalField();
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->0>;
A<t> := DifferentialRing(R, f, Q);
F:=FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
```

For every linear differential equations $u \in K\lbrace x_1,\ldots,x_n\rbrace$ there exists Weyl algebra elements $L_1,\ldots,L_n$ such that $u=L_1\cdot x+1 + \cdots + L_n x_n$. There is an intrinsic which when given a linear $u$ will return the sequence $(L_1,\ldots,L_n)$. 
The intrinsic is called `LinearOperators`.
```
u:=Diff(x,3)+2*Diff(y,1);
Ls:=LinearOperators(u);
u eq &+[Ls[i]@P.i : i in [1..Ngens(P)]];
Ls;
```
```
true
[
D^3,
2*D^1
]
```

### Example: Weyl Algebras

Create a AlgWeyl object.
```
Q:=Rationals();
P := PolynomialRing(Q);
f := map<P->P | a:->5*Derivative(a)>;
R := DifferentialRing(P, f,Q);
W := WeylAlgebra(R);
```
Create some elements to test things with.
```
x:=P.1;
x:=R!x;
E1 := elt(W, x);
E2 := elt(W, 20);
E1+E2;
```
```
$.1 + 20 d^0
```
Test the different ways to instantiate Weyl algebra elements and make sure they give the right thing back.
```
my_array:=AssociativeArray();
my_array[0]:=x;
E1arr:=elt(W,my_array);
E2tup := elt(W, [<20,0>]);
E1tup := elt(W, [<x,0>]);
dW:= elt(W,[<1,1>]);
two:=elt(W,2);
E2tup eq E2;
E1arr eq E1;
2*x*dW+0 eq 2*x*dW;
0+2*dW eq 2*dW;
```
```
true
true
true
true
```
Test that the operations of addition an multiplication are well-defined.
```
E3 := E1 + E2;
E4 := E1 * E2;
E3+1;
```
```
$.1 + 21 d^0
```
Test exponentiation and getting the derivation
```    
dW:=Derivation(W);
dW^2;
```
```
0 d^1+ 1 d^2
```
There are a couple other functions that aren't shown.

One can take `Eltseq()` of an element.
```
Q:=Rationals();
P := PolynomialRing(Q);
f := map<P->P | a:->5*Derivative(a)>;
R := DifferentialRing(P, f,Q);
x:=P.1;
W := WeylAlgebra(R);
dW:=elt(W,[<x,1>]);
Parent(dW) eq W;
```
```
true
```
Coercion from valid Eltseqs back into the WeylAlgElt types is supported. 

### Example: Weyl Algebra Division Algorithm Over A Field

Given Weyl algebra elements $A$ and $B$ in $K[\partial]$ where $K$ is a differential field we can find other Weyl algebra elements $Q$ and $R$ where the order of $R$ is less than the order of $A$ such that $B=QA+R$. This is left division of $B$ by $A$ and it proceeds in a fashion similar to the usual Euclidean algorithm.

```
WP<D>:=WeylAlgebra(P);
B:=1+t*D^2+2*D^5;
A:=1+t*D^3;
quo,rem:=Divide(B,A);
B eq quo*A+rem;
quo;
rem;
```
```
true
2/t*D^2
D^0+ (t^2 - 2)/t*D^2
```

### Example: Truncating to Polynomial Rings of Finite Order

All of this runs through Magma's RngMPol types so naturally there is a way to take the rth jet ring of a prolongation sequence and take the image of a differential polynomial in a polynomial ring. 

```
f:=x^3+t*Diff(x,1)^3+t^2*Diff(x,2)^3;
Type(f);
Type(Parent(f));
```
```
RngMPolProlSeqElt
RngMPolProlSeq
```
We convert to multivariate polynomial ring elements and multivariate polynomial rings using the command `Jet` with `Jet(P,-1)` being the base ring.
```
trace3:=Jet(f,3);
J3:=Jet(P,3);
trace3 in J3;
Parent(trace3) eq J3;
Type(trace3);
Type(J3);
```
```
true
true
RngMPolElt
RngMPol
```
There is also built in coercion for getting these elements back into RngMPol.
```
P!trace3 eq f;
```
```
true
```


### Example: Leading Monomials, Leaders, Separants, Initials, TopCoeff

There is some support for leading monomials, element sequences. We can also take the `P.[i,j]` to take the jth derivative of the ith variable. It also handles the product rule for coefficients. `Leader`,`Separant`,`Initial`, `LeadingTerm` are also implemented.

```
LeadingMonomial(f1);
P.[1,2];
f1 eq P!Eltseq(f1);
Diff(x*t^3);
```
```
Diff(x,1)*Diff(y,2)
Diff(x,2)
true
t^3*Diff(x,1) + 3*t^2*x
```

### Example: Eltseq and Coercion

We can take Eltseqs of element to get sequences corresponding to elements.
We can also coerce those sequences to get back our elements. 

```
Eltseq(f1);
f1 eq P!Eltseq(f1);
```
```
[
<1, [
<[ 1, 1 ], 1>,
<[ 2, 2 ], 1>
]>,
<1, [
<[ 1, 0 ], 2>
]>,
<t, [
<[ 1, 0 ], 0>
]>
]
true
```



### Example: Evaluation of Differential Polynomials

We can evaluate differential polynomials at other differential polynomials. 

```
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
ff:=t*Diff(x,2)*Diff(y,2);
P2<u,v,w>:=PolynomialRingProlSeq(F,3);
f1:=u+t*Diff(v,1)+w;
f2:=v+Diff(u,1)+w;
seq:=[f1,f2];
Evaluate(ff,seq);
```
```
t*Diff(u,2)*Diff(u,3) + t^2*Diff(u,3)*Diff(v,3) + 2*t*Diff(v,2)*Diff(u,3) + t*Diff(w,2)*Diff(u,3) + t*Diff(u,2)*Diff(v,2) + t*Diff(u,2)*Diff(w,2) + t^2*Diff(v,2)*Diff(v,3) + t^2*Diff(w,2)*Diff(v,3) + 2*t*Diff(v,2)^2 + 3*t*Diff(v,2)*Diff(w,2) + t*Diff(w,2)^2
```

### Example: Specialization of Coefficients of Differential Polynomials

Given differential polynomials with coefficients in a type where Evaluate makes sense (RngMPol or RngMPolProlSeq) we can specialize the coefficients of differential polynomials. 

```
R<s,t>:=PolynomialRing(Q,2);
f := map<R->R|f:->Derivative(f,t)>;
A<s,t> := DifferentialRing(R, f, Q);
P<x,y>:=PolynomialRingProlSeq(A,2: term_order:=<"dblocks",[[1,2]]>);
ff:=(t^2)*Diff(x,1)*Diff(y,1)+Diff(x,4)+s*Diff(x,1)*Diff(y,2)^2+t;
seq1:=[1,2];
ff;
Specialize(ff,seq1);
```
```
Diff(x,4) + s*Diff(x,1)*Diff(y,2)^2 + t^2*Diff(x,1)*Diff(y,1) + t
Diff(x,4) + Diff(x,1)*Diff(y,2)^2 + 4*Diff(x,1)*Diff(y,1) + 2
```

### Example: Polynomial Pseudodivision

Pseudodivision is implemented for polynomial rings (RngMPol)

```
Q:=RationalField();
R<x,y>:=PolynomialRing(Q,2);
f:=x^2+2*x*y^2+3;
g:=y^4+y^2+2*y*x^2+2;

quo,rem,sep:=PseudoDivide(f,g,x);
sep*f-quo*g eq rem;
```
```
true
```

### Example: Ritt's Division Algorithm

The Ritt reduction algorithm based on polynomial pseudodivision is also implemented. The quotient here is an element of a Weyl algebra. 

Given a basic setup 
```
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
WP<D>:=WeylAlgebra(P);
```
We can divide an element f by g with in a single step of completely reduce it. The call IsRittReduced will return true or false depending on if the leader of g or non-trivial derivative of the leader of g appears in f. In the case it does, it returns the number of derivatives that need to be taken. In the case that it is ritt reduced the number of derivatives that needs to be taken will be returned as -1.
```
f:=Diff(x,1)+Diff(y,3);
g:=x^2+Diff(y,2)*Diff(x,1)+t;
quo,rem,sep:=RittDivideStep(f,g);
sep*f - quo@g eq rem;
quo,rem,sep:=RittDivide(f,g);
sep*f-quo@g eq rem;
IsRittReduced(rem,g);
```
```
true
true
true
-1
```
`RittDivide` is also implemented for autoreduced sets. The following is such an example. In earlier versions we didn't run through the reduction process multiple times (which surprisingly runs most of the time) which led to bugs. Also, some authors (not Ritt) like to stage the reduction process by first reducing to the point where the remainder is in the same minimal jet ring containing all the elements of the autoreduced sequence we are dividing by. Once this happens one can use pseudoreduction of standard Groebner algorithms to determine membership.

I haven't implemented the Groebner version, but that seems like the "right" thing to do so perhaps I will add a Groebner option later for `RittDivideStaged`.
```
f := Diff(y,3) + Diff(x,1);
G :=[Diff(x,1)*Diff(y,2) + x^2 + t,-1*x^2*Diff(x,2) -t*Diff(x,2) -1*Diff(x,1)^3 + 2*x*Diff(x,1)^2 + Diff(x,1)];
Quo0,Rem0,Sep0:=RittDivide(f,G :partial:=true);
Quo1,Rem1,Sep1:=RittDivide(Rem0,G);
Quo2,Rem2,Sep2:=RittDivideStaged(f,G);
Rem2 eq Rem1;

Quo3,Rem3,Sep3:=RittDivide(f,G);
Rem3 eq Rem2;
```

```
true
true
```

### Example: Element Comparison and Sorting

We also have some support for sorting. We have defined `lt`,`le`,`gt`, and `ge`. Since we can't fuck with `Sort` we have defined `Sorted` for our elements. The elements which are minimal, meaning the smaller leading polynomial will appear first. 

```
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
f:=Diff(x,1)+Diff(y,3);
g:=x^2+Diff(y,2)*Diff(x,1)+t;
F0:=[f,g];
Sorted(F0);
F1:=match_orders(F0);
Sort([f`elt: f in F1]);
g lt f;
```
```
[
Diff(x,1)*Diff(y,2) + x^2 + $.1,
Diff(y,3) + Diff(x,1)
]
[
Diff(x,1)*Diff(y,2) + x^2 + $.1,
Diff(y,3) + Diff(x,1)
]
true
```

### Example: Characteristic Sets and Pseudodivision for Polynomial Rings

We have implemented some ancient algorithms by digging into the bowels of singular (which Macaulay2 is based off of). There are some references in the source code. 

```
AttachSpec("diffalg.spec");
Z:=Integers();
Q:=RationalField();
```

```
R<x1,x2,x3,x4>:=PolynomialRing(Q,4);
F1:=x4^4+x1*x4^2-x2*x4-x1*x2*x4-x1*x2+3*x2;
F2:=x1*x4+x3-x1*x2;
F3:=x3*x4-2*x2^2-x1*x2-1;
q,r,s:=PseudoDivide(F1,F2,Leader(F2));
q0,r0,s0:=PseudoDivide(F1,F2);
q0 eq q and r0 eq r and s0 eq s;
s*F1 eq q*F2+r;
IsPseudoReduced(r,F2);
Degree(r,Leader(F2));
Degree(F2,Leader(F2));
```
```
true
true
true
0
1
```
I had to debug pseudodivision a little so I'm going to add one of the things that was giving me trouble.
```
f:=2*x2^3 - 2*x2^2*x4 - x2*x3*x4 + x2*x3 + x2 + x3*x4^2 - x4;
g:=1/2*x2^2*x4 + 3/2*x2^2 - 1/2*x2*x3*x4 - 1/2*x2*x3 + 1/2*x2*x4^4 - 1/2*x3*x4^2 + 1/2*x4;
u:=x2;
quo,rem,sep:=PseudoDivideStep(f,g,u);
sep*f eq quo*g+rem;
```
```
true
```

A triangular set is one which has distinct leaders. This is an old-school way of finding prime ideals. This is comparible to the the function `BestAutoreducedSet` on `RngMPol`.
```
S:=[F1,F2,F3];
BasicTriangularSet(S);
```

```
[
-x1*x2 - 2*x2^2 + x3*x4 - 1
]
```

We have a method for producing very basic characteristic sets. In this particular example there are three elements of the characteristic set. 
```
C:=CharacteristicSet(S);
#C eq #{Leader(c) : c in C}; //leaders are distinct
IsTriangular(C);
IsTriangularNoSort(C);
```
```
true
true
true
```

### Example: Characteristic Sets and Pseudodivision for RngMPolProlSeq

```
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[2,1]]>);
```

```
p1:=y^2-1;
p2:=(y+1)*x-1;
G0:=Sorted([p1,p2]);
MinimalAutoreducedSub(G0) eq [p2];

//unsorted it will give an error;
//MinimalAutoreducedSub([p1,p2]);
```
```
true
```

The main algorithm checks for `CharacteristicSet` checks to see if `NiceAutoreduced` is stable. The steps of nice autoreduced are also implements. At each stage we have that the differential ideal generated by elements of the output are contained in the differential ideal generated by the elements of the input and that the differential ideal of the input is contained in the initial and separant saturation of the differential ideal generated by the output. 
```
A0:=NiceAutoreduced(G0);
A1:=NiceAutoreduced(Sorted(G0 cat A0));
A0 eq A1;
A:=CharacteristicSet(G0);
A eq A0;
```
```
true
true
```

This is an easy example where the characteristic set is equal to the full ideal is equal to the ideal generated by the characteristic set. In general we will just have that [A] subset I subset Sat([A]) where saturation is with respect to the initials and separants. 
```
char_set:=[2*x + -1, 1/2*y + -1/2];
R0:=Jet(P,0);
G:=[Jet(f,0) : f in char_set];
I0:=ideal<R0|G>;
I1:=ideal<R0|[Jet(p,0) : p in G0]>;
I0 subset I1;
GroebnerBasis(I1) eq GroebnerBasis(I0);
```
```
true
true
```


### Example: The Rosenfeld-Groebner Algorithm

The diffalg package has support for the Rosenfeld-Groebner algorithm which allows us to compute decompositions of prime ideals. 

First some terminology. In what follows R is the ring of differential polynomials.

Defn. By a saturation ideal associated to equations an inquations I mean Sat_{ineqns}([eqns]) which is the saturation of the differential ideal generated by the equations by the multiplicative set generated by the inequation. 

Defn. A sequence (f1,...,fr) initial-regular (resp separant-regular) if the initials (resp separants) of f_{i+1} are nonzero divisors in  R/[f1,...,fi].

The algorithm produced a sequence of equations and inequations which have the property the equations are autoreduced and both initial-regular and separant-regular. The Characteristic series for data defining a saturation ideal Sat_{ineqns}([eqns]) will be a sequence of data defining saturation ideals which are autoreduced, initial-regular and separant-regular whose intersection is the radical the given saturation ideal. 

The implementation is broken into two parts: The algorithm in `CharacteristicSeriesRaw` is essentially  Algorithm 1 from Golubitsky,Kondratieva,Maza,Ovchinnikov,Bounds for algorithms in differential algebra, Journal of Symbolic Algebra, which is linked to here: http://arxiv.org/abs/math/0702470v1

We introduce a function `clean_up` (whose name will probably change which converts) removed the redundant and trivial outputs of `CharacteristicSeriesRaw`. The function `CharacteristicSeries` is the composition of the two. 

We do the example from section 3.4.1 of Boulier's notes here: https://hal.science/hal-02378197/document.
```
AttachSpec("diffalg.spec");
Z:=Integers();
Q:=RationalField();
 R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1],[2]]>);
f1:=Diff(x,2)+y;
f2:=Diff(x,1)^2+y;
clean:=CharacteristicSeries([f1,f2]);
#clean;
clean[1];
clean[2];
```

```
2
[
[
1/2*Diff(y,1)^2 + 2*y^3,
y*Diff(x,1) + -1/2*Diff(y,1)
],
[
y,
Diff(y,1)
]
]
[
[
y,
2*Diff(x,1)
],
[]
]
```
Here is another example from before where there are no derivatives. This is consistent with the previous operation.
```
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[2,1]]>);
p1:=y^2-1;
p2:=(y+1)*x-1;
G0:=Sorted([p1,p2]);
char_series:=CharacteristicSeries([p1,p2]);
char_series;
```

```
[
[
[
2*x + -1,
1/2*y + -1/2
],
[]
]
]
```

### Example: Ollivier's Division Algorithm


There is support for Ollivier's Reduction Algorithm from Standard Bases of Differential Ideals. The intrinsic `OllivierDivide` uses `OllivierDivideStep` and is his reduction algorithm. It is an important ingredient of his Groebner basis algorithm. The setup is the usual one.
```
R<t>:=PolynomialRing(Q,1);
ff := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, ff, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[2,1]]>);
WP<D>:=WeylAlgebra(P);
```

Here is an example call of `OllivierDivide` where we divide f by g. The output will be a Weyl algebra element and a differential polynomial which is the remainder.
```
g:=Diff(x,1)^2+y;
f:=Diff(g,1)*Diff(g,2)^2+Diff(g,1)*g^2+2;
Quo,Rem:=OllivierDivide(f,g);
f eq Quo@g+Rem;
Quo;
```
```
true
4*Diff(x,1)^2*Diff(x,3)^2 + 8*Diff(x,1)*Diff(x,2)^2*Diff(x,3) + 4*Diff(x,1)*Diff(y,2)*Diff(x,3) + 4*Diff(x,2)^4 + 4*Diff(x,2)^2*Diff(y,2) + Diff(y,2)^2 + Diff(x,1)^4 + 2*y*Diff(x,1)^2 + y^2*D^1
```

We can check that this complicated quotient is related to a more simple looking expression that we used to cook up the division.
```
Quo2:=(Diff(g,2)^2+g^2)*D;
Rem eq f-Quo2@g;
```
```
true
```

We can in fact check that these two elements of the Weyl algebra are equal.
```
Quo eq Quo2;
```
```
true
````

Here was an example that is technically difficult for various reasons. In the process of doing the computation RittDivision requires multiple iterations. Also, some extra code to handle "leading monomials","leaders", and "initials" of differential polynomials of degree zero.  

```
f:=Diff(x,1)+Diff(y,3);
g:=x^2+Diff(y,2)*Diff(x,1)+t;
#CharacteristicSeries([f,g]);
```
```
1
```

### Example: Evaluation of Free Algebra Elements into Weyl Algebras

```
R<t>:=PolynomialRing(Q,1);
ff := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, ff, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[2,1]]>);
WP<D>:=WeylAlgebra(P);
```

I define a little function for commutators for this example.
```
function comm(a,b)
    return a*b - b*a;
end function;
```

We can check that when we evaluate a free algebra element to the the Weyl algebra commutators map to derivatives.
Some comparison functions had to be written to do this type of comparison.
```
F<du,xu,yu> := FreeAlgebra(Q, 3);
g :=comm(du,comm(du,xu))*comm(du,yu);
seq:=[D,WP!x,WP!y];

Evaluate(g,seq) eq Diff(x,2)*Diff(y,1);
```
```
true
```

### Example: LaTeX



Differential polynomial ring elements 
```
g:=Diff(x,1)*Diff(y,2) + x^2 + t;
Latex(g);
```
```
\partial(x)\partial^2(y)+\partial(x)\partial^2(y)+x^{2}+t
```

Weyl algebra elements where D is the named variable (which can be retrieved as a sequence of length one from Names)
```
opr:=x*D+Diff(y,1)*D^0;
opr;
latex_weyl(opr);
```
```
Diff(y,1)*D^0+ x*D^1
\partial(y)+xD^1
```
### Example: Magma Enhancement, Quotients of Quotients 

This little bit addressed some deficiencies in Magma's RngMPol implementation. Magma complains about taking dual numbers of basic rings, which is something we need to do. 
```
B<aa,bb>:=PolynomialRing(Q,2);
I:=ideal<B|aa^2+bb^2-1>;
A:=quo<B|I>;

A1<t>:=PolynomialRing(A,1);
quo<A1|t^2>;
```

Magma also complains about taking quotients of polynomial rings
```
B1<xx>:=PolynomialRing(Q,2);
P1<tt>:=PolynomialRing(B1,2);
A2:=quo<P1|tt^2>;
```

Next, I will go through the functions `Quot`,`Quot0`,and `FlattenPolynomialRing` which can help with these tasks. It isn't pretty but it works. It's all basically the isomorphism theorems from Dummit and Foote.

```
B1<xx,yy>:=PolynomialRing(Q,2);
P1<tt,ss>:=PolynomialRing(B1,2);
B2<uu,vv,ww>:=PolynomialRing(P1,3);
Pflat,map_flat:=FlattenPolynomialRing(B2);
assert Type(Pflat) eq RngMPol;
assert Rank(Pflat) eq Rank(B1)+Rank(P1)+Rank(B2);
```
Support for quotients of polynomial rings over polynomial rings.

```
B1<xx,yy>:=PolynomialRing(Q,2);
P1<tt,ss>:=PolynomialRing(B1,2);
seq:=[tt^2];

A,map_to_A:=Quot(P1,seq);
f:=tt^2+xx*ss+yy;
assert f in P1;
assert map_to_A(f) in A;
```
Support for quotients of polynomial rings over general rings. 

```
B<aa,bb>:=PolynomialRing(Q,2);
I:=ideal<B|aa^2+bb^2-1>;
A<abar,bbar>:=quo<B|I>;
PA<tt>:=PolynomialRing(A,1);
seq:=[(abar)*tt^2];
PA_quo<abar1,bbar1,tt1>:=Quot0(PA,seq);
assert abar1*tt1^2 eq 0;
```

### Example: Differential Rings of Differential Prime Ideals

```
R<t>:=PolynomialRing(Q,1);
ff := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, ff, Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
```

```
f:=Diff(x,1)+Diff(y,3);
g:=x^2+Diff(y,2)*Diff(x,1)+t;
Cs,Is:=CharacteristicSeries([f,g]);
sys:=Cs[1];
eqns:=sys[1];
ineqns:=sys[2];
pp:=JetIdeal(eqns,ineqns);
assert IsPrime(pp);
assert Dimension(pp) le JacobiBound([f,g]);
```
The above passes and there is no interesting output. 

We can compute the dimension
```
A:=DifferentialRing(eqns,ineqns); //Give a quotient of J2
Dimension(pp);
```
```
4 [ 2, 4, 5, 6 ]
```


We can compare it to the Jacobi bound of our original equations.

```
JacobiBound([f,g]);
```
```
4 1
```

We can form the JetIdeal directly. 
```
sys:=Cs[1];
I:=JetIdeal(sys[1],sys[2]);
A<x0,y0,x1,y1,x2,y2>,delta:=DifferentialRing(sys[1],sys[2]);
Diff(x1+x2^2+y2);
```
```
-6*x1^10 + 28*x0*x1^9 + -44*x0^2*x1^8 + (-4*t + 12)*x1^8 + 24*x0^3*x1^7 + (8*t - 32)*x0*x1^7 + 20*x0^2*x1^6 + (4*t - 6)*x1^6 + -1*x0^4*x1^5 + -2*t*x0^2*x1^5 + 4*x0*x1^5 + -t^2*x1^5 + 2*x0^5*x1^4 + 4*t*x0^3*x1^4 + 2*t^2*x0*x1^4 + -1*x0^6*x1^3 + (-3*t + 1)*x0^4*x1^3 + (-3*t^2 + 2*t)*x0^2*x1^3 + (-t^3 + t^2)*x1^3
```

We can check explicitly that I is a differential ideal with our
derivation.
This is done by checking that derivatives of the generators explicitly.
You can also see that our generators vanish. (Note that to evaluate at f directly one would need to take a derivative of x2 )
```
assert &and[delta(g) in I : g in Generators(I)];
A!Jet(g,2);
```
```
0
```

You can also take the field of fractions to get the residue field which is a differential field. 
```
kappa_pp:=FieldOfFractions(A);
```

### Example: Linearizing Differential equations



Given some differential equations we can linearize them at a generic point of reduced irreducible differential algebraic variety specified by a characteristic set. (WARNING: This is currently bugged and in package-dimension.mag)

```
R<t>:=PolynomialRing(Q,1);
der:=map<R->R|f:->R!0>;
A:=DifferentialRing(R,der,Q);
F<t> := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);

f:=Diff(x,1)+Diff(y,3);
g:=x^2+Diff(y,2)*Diff(x,1)+t;
eqns:=[f,g];

Cs:=CharacteristicSeries(eqns);
sys:=Cs[1];
lin_eqns:=Linearize(eqns,sys[1],sys[2]);
lin_eqns;
```
```
[
Diff(x1,1),
Diff(x,1)*Diff(y1,2) + Diff(y,2)*Diff(x,1)*Diff(x1,1) + 2*x*x1
]
```

### Example: Strictly and Weakly Increasing Sequences

First, Sit-Reinhart, Etesse, and Merker-Chen have use bijections between strictly increasing and weakly increasing sequences of integers and differentially homogeneous polynomials. Consider a sequence of integers $a_1,\ldots,a_s$. We say a sequence is strictly increasin if $a_1<a_2<\ldots<a_s$ and it is weakly increasing or non-decreasing if $a_1 \leq a_1 \leq \ldots \leq a_s$. 
We have some functionality for testing sequences and producing sequences. 
```
seqs:=StrictSeqs(3,5);
myseq:=seqs[5];
myseq;
IsStrictSeq(myseq);
IsWeakSeq(myseq);
```
```
true
true
```

There is a bijection between strictly and weakly increasing sequences and `StrictToWeak` and `WeakToStrict` instantiate that bijection.
We also have the ability to take a week sequence and then exponentiate a differential polynomial with respect to the weak sequence.
If $a_1,\ldots,a_s$ is a non-decreasing sequence then $x^{(a_1,\ldots,a_n)}$ is defined to be $x^{(a_1)}x^{(a_2)}\cdots x^{(a_s)}$. 
For each monomial, we can associate a weight to it. The weight of a monomial, the weight of a strictly increasing sequence, and the weight of a weakly increasing sequence are all defined to be the same thing which is the sum of the entries of the weakly increasing sequence.
```
weak_seq:=StrictToWeak(myseq);
mon:=x^weak_seq;
Weight(mon) eq WeightWeak(weak_seq);
WeightStrict(myseq) eq WeightWeak(weak_seq);
```
```
true
true
```
There is support fo the empty sequence. This was causing some bugs in an early version of this so its important that this case works.
```
x^[] eq 1;
```
```
true
```
We can extract the weak sequence from a given monomial using the command `WeakSeqs`. 
```
mon:=(x^weak_seq)*y;
mon eq &*[P.i^WeakSeqs(mon)[i] : i in [1..Ngens(P)]];
```
```
true 
```

Note that because of the bijection between monomials and weakly increasing sequences there is a bijection between monomial orderings and orderings on weakly increasing sequences. It is convenient to make an inductive definition for weakly increasing sequences. If $(a_1,\ldots,a_n)$ and $(b_1,\ldots,b_m)$ are weakly increasing sequences then we say that $(a_1,\ldots,a_n)<(b_1,\ldots,b_m)$ where provided that 1) $a_n<b_m$ or 2) $a_n=b_m$ and $(a_1,\ldots,a_{n-1})<(b_1,\ldots,b_{m-1})$. In this setup we use the convention that the empty sequence is less than everything. This gives a good inductive algorithm for checking this particular term order. See Chen-Merker Theorem 3.4.


### Example: Homogeneous Differential Polynomials

A differential polynomial $f(x_1,\ldots,x_n) \in K\lbrace x_1,\ldots,x_n\rbrace$ is called differentially homogeneous if and only if there exists some integer $d$ such that $f(\lambda x_1,\ldots,\lambda x_n) = \lambda^d f(x_1,\ldots,x_n)$.
This package has some support for differentially homogeneous polynomials. 

There is a subring $V \subset K\lbrace x_0,\ldots,x_n\rbrace$ of differential homogeneous polynomials which is graded by degree. 
The Kolchin-Schmitt conjecture (now a Theorem of Etesse) says that $V_d$ has dimension $(n+1)^d$ as a $K$-vector space. 
The basis for these differentially homogeneous polynomials are the Rienhart-Wronskians which are generalizations of Wronskians. 
For example $W(x_0,t x_0, x_1,t^2 x_1)\vert_{t=0}$ is such a Wronskian.

The file `test-homog-01.ipynb` in `./test-homog` contains the examples below. 

From the `./test-homog` folder we run 
```
AttachSpec("../diffalg.spec");
Z:=Integers();
Q:=RationalField();
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A<t> := DifferentialRing(R, f, Q);
F<t>:=FieldOfFractions(A);
P<x0,x1,x2,x3>:=PolynomialRingProlSeq(F,4: term_order:=<"dblocks",[[1,2,3,4]]>);
```

There is quite a bit of functions added for working with partitions. This supplements the already nice library Magma has for YoungTableaux.


```
d:=4;
N:=2;
#UnorderedPartitionsWithZero(d,N);
```
```
5
```
`AdmissibleStrictSeqss` corresponds to homogenous polynomials of degree $d$ in $N$ variables. There will always be $N^d$ of them. This is Etesse's Theorem which recently proved the Schmidt-Kolchin Conjecture.
```
#AdmissibleStrictSeqss(d,N);
```
```
16
```

Using further work of Etesse we can determine a set of algebra generators for the graded ring of homogeneous polynomials in $N$ variables of order up to $d$. The function `GeneratingSequences(d,N)` generates those sequences of degree $d$ in $N$ variables that will give generators.
```
alphas:=GeneratingSequences(d,N);
#alphas;
```
```
4
```

In this particular example, these generating sequences correspond to 4 Wronskians.
Note here that we are using Etesse's notation. There is also some other code for working in Chen-Merker coordinates. 

```
alpha1:=alphas[1];
alpha2:=alphas[2];
alpha3:=alphas[3];
alpha4:=alphas[4];

Wronsk(alpha1,[x0,x1]);
Wronsk(alpha2,[x0,x1]);
Wronsk(alpha3,[x0,x1]);
Wronsk(alpha4,[x0,x1]);
```
```
-2*x1^3*Diff(x0,3) + 2*x0*x1^2*Diff(x1,3) + 6*x1^2*Diff(x1,1)*Diff(x0,2) + 6*x1^2*Diff(x0,1)*Diff(x1,2) + -12*x0*x1*Diff(x1,1)*Diff(x1,2) + -12*x1*Diff(x0,1)*Diff(x1,1)^2 + 12*x0*Diff(x1,1)^3
-2*x0^2*x1*Diff(x0,3) + 2*x0^3*Diff(x1,3) + 12*x0*x1*Diff(x0,1)*Diff(x0,2) + -6*x0^2*Diff(x1,1)*Diff(x0,2) + -6*x0^2*Diff(x0,1)*Diff(x1,2) + -12*x1*Diff(x0,1)^3 + 12*x0*Diff(x0,1)^2*Diff(x1,1)
-2*x1^2*Diff(x0,1)*Diff(x0,3) + 2*x0*x1*Diff(x1,1)*Diff(x0,3) + 2*x0*x1*Diff(x0,1)*Diff(x1,3) + -2*x0^2*Diff(x1,1)*Diff(x1,3) + 3*x1^2*Diff(x0,2)^2 + -6*x0*x1*Diff(x0,2)*Diff(x1,2) + 3*x0^2*Diff(x1,2)^2 + -6*x1*Diff(x0,1)*Diff(x1,1)*Diff(x0,2) + 6*x0*Diff(x1,1)^2*Diff(x0,2) + 6*x1*Diff(x0,1)^2*Diff(x1,2) + -6*x0*Diff(x0,1)*Diff(x1,1)*Diff(x1,2)
2*x0*x1^2*Diff(x0,3) + -2*x0^2*x1*Diff(x1,3) + -6*x1^2*Diff(x0,1)*Diff(x0,2) + 6*x0^2*Diff(x1,1)*Diff(x1,2) + 12*x1*Diff(x0,1)^2*Diff(x1,1) + -12*x0*Diff(x0,1)*Diff(x1,1)^2
```

We now discuss the Chen-Merker implemetation a bit. This is deprecated and may be deleted. Given a sequence of strictly increasing sequences $\alpha = (\alpha_1,\ldots,\alpha_s)$ and a sequence of differentially homogeneous polynmomials $f=(f_1,\ldots,f_s)$ we are going to make a Reinhart-Wronskian $W(\alpha,f)$ which is going to be a determinant of a certain $L\times L$ matrix.
If $l=(l_1,\ldots,l_s)$ are the length sequences of the $(\alpha_1,\ldots,\alpha_s)$ we have $L = \sum_{i=1}^s l_i$. 
We are going to get a matrix which is $L\times L$. 

The matrix for the Reinhard-Wronskian is made up of $s+1$ blocks. 
We need to make blocks `WronskPiece(alphas[i],variables[i])` where `variable[i] = xi`.

In Chen-Merker they start at $N$ and then work down $N$,$N-1$,$N-2$,...,$1$, then get to the special one.
To talk about the special block I need to tell you what $s_1$ is and what $M$ is. 
The variable $M$ is the maximum order that appears in any of the previous blocks.
The variable $s_1$ is the sum of all the previous lengths: $s_1 = \sum_{i=1}^s l_i$.
The new block makes a bunch of `[WronskCol(i,x0) i in [s1...M]]`

### Example: Compactified Jet Spaces of Projective Space

Let $V^{(r)}$ denote the subring of $K[x_0,\ldots,x_N]^{(r)}$ consisting of homogeneous differential polynomials. We have implemented $Proj(V^{(r)})$ which is a compactification of $J^r(\mathbb{P}^N)$. The initialization is the standard one were we attach the package and define `Z` and `Q` to be the integers and rationals respectively. This automatically keeps track of the weights of the Wronskians and the weights between them.

```
R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A<t> := DifferentialRing(R, f, Q);
F<t>:=FieldOfFractions(A);
P<x0,x1>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1],[2]]>);
```
```
r:=2;
vars:=[P.i : i in [1..Ngens(P)]];
X:=CompactifiedJetSpace(r,vars);
X;
```
```
Scheme over F defined by
w[3]^2 + -1/2*w[2]*w[4] + -1/2*w[1]*w[5]
```
Many of Magma's built-in functions for projective varieties don't work out of the box here as of Summer 2025. So we have defined a `StandardEmbedding` function which maps any scheme in a weighted projective space to a projective space by taking all of the monomials of degree d where d is the least common multiples of the weights of the variables and then embeds it into $\mathbb{P}^m$ for some $m$. The output will return the scheme theoretic closure of the image, the map that defined by these monomials, and the linear series object corresponding to those monomials (for which magma has a built-in morphism function). 

```
time X1,phi,L:=StandardEmbedding(X);
```
```
Time: 3.600
```


