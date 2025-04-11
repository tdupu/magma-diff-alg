### About magma-diffalg

(NOTE: This file can be edited with Typora or the github editor) 

There are two implementations of differential polynomials in the package. There is one that uses differential monomials (`RngDiffPol`) and one based on pronlongations sequences which are essentially collections of polynomial rings with inclusion and derivations between them (`RngMPolProlSeq`). 

Each of these two types has a corresponding element tupe with an `Elt` appended to the end. Currently, `RngDiffPol` is only implemented with a constant base but `RngMPolProlSeq` can have a base which is a differential ring. 

Also term order associated with block rankings are implemented in the prolongation sequences version. 

TODO: Add links to each of the topics with a title
https://github.com/tdupu/magma-diff-alg/blob/master/README.md#example-specialization-of-coefficients-of-differential-polynomials


###### Example: Instatiating Basic Objects

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

###### Example: Truncating to Polynomial Rings of Finite Order

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


###### Example: Leading Monomials, Leaders, Separants, Initials, TopCoeff

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

###### Example: Eltseq and Coercion

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



###### Example: Evaluation of Differential Polynomials

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

###### Example: Specialization of Coefficients of Differential Polynomials

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

###### Example: Polynomial Pseudodivision

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

###### Example: Ritt's Division Algorithm

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
`RittDivide` is also implemented for autoreduced sets.  


###### Example: Element Comparison and Sorting

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

###### Example: Characteristic Sets and Pseudodivision for Polynomial Rings

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
