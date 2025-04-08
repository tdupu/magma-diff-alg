ABOUT:
There are two implementations of differential polynomials in the package. There is one that uses differential monomials (`RngDiffPol`) and one based on pronlongations sequences which are essentially collections of polynomial rings with inclusion and derivations between them (`RngMPolProlSeq`). 

Each of these two types has a corresponding element tupe with an `Elt` appended to the end. Currently, `RngDiffPol` is only implemented with a constant base but `RngMPolProlSeq` can have a base which is a differential ring. 

Also term order associated with block rankings are implemented in the prolongation sequences version. 


EXAMPLE:
Here is how you instantiate the basic objects. 

```
AttachSpec("diffalg.spec");
Z:=Integers();
Q:=RationalField();

R<t>:=PolynomialRing(Q,1);
f := map<R->R|f:->Derivative(f,t)>;
A := DifferentialRing(R, f, Q);
F := FieldOfFractions(A);
P<x,y>:=PolynomialRingProlSeq(F,2: term_order:=<"dblocks",[[1,2]]>);
f1:=x^2+Diff(y,2)*Diff(x,1)+t;
f2:=Diff(x,1)+Diff(y,3);
```


EXAMPLE:
There is some support for leading monomials, element sequences. We can also take the P.[i,j] to take the jth derivative of the ith variable. It also handles the product rule for coefficients. 
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


EXAMPLE:
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

EXAMPLE:
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

EXAMPLE:
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

EXAMPLE:
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

EXAMPLE: 
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

EXAMPLE:
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
