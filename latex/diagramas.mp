input metauml;
beginfig(1);
    Class.exp("Expression")()
    	("if_else(E1,E2)","succ()","pred()","is_zero()","apply(E)");
	Class.boolv("BoolValue")()
       ("if_else(E1,E2)");
    Class.abst("Abstraction")()
       ("apply(E)");
    Class.appl("Application")()
       ();
    Class.vari("Variable")()
       ();
    Class.zero("Zero")()
       ("pred()","is_zero()");
    Class.succ("Succ")()
       ("pred()","is_zero()");
    Class.pred("Pred")()
       ("succ()");
    Class.isz("IsZero")()
       ();
    Class.ifthen("IfThenElse")()
       ();

	topToBottom.midx(30)(exp,boolv);
	leftToRight.midy(10)(boolv,abst,appl,vari,zero);
    topToBottom.midx(10)(boolv,succ);
    leftToRight.midy(10)(succ,pred,isz,ifthen);
    drawObjects(exp,boolv,abst,appl,vari,zero,succ,pred,isz,ifthen);
    clink(inheritance)(boolv,exp);
    clink(inheritance)(abst,exp);
    clink(inheritance)(appl,exp);
    clink(inheritance)(vari,exp);
    clink(inheritance)(zero,exp);
    clink(inheritance)(succ,exp);
    clink(inheritance)(pred,exp);
    clink(inheritance)(isz,exp);
    clink(inheritance)(ifthen,exp);
endfig;
end