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
