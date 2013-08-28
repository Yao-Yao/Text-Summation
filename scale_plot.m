x=0:1:100
plot(x,(x+1)./(x), x,1./sqrt(x), x,1./x)
x=10
text(x,(x+1)./(x),'(x+1)/(x)')
text(x,1./sqrt(x),'1/sqrt(x)')
text(x,1./x,'1/x')