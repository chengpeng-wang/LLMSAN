/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE369_Divide_by_Zero__int_zero_divide_68a.java
Label Definition File: CWE369_Divide_by_Zero__int.label.xml
Template File: sources-sinks-68a.tmpl.java
*/
/*
 * @description
 * CWE: 369 Divide by zero
 * BadSource: zero Set data to a hardcoded value of zero
 * GoodSource: A hardcoded non-zero, non-min, non-max, even number
 * Sinks: divide
 *    GoodSink: Check for zero before dividing
 *    BadSink : Dividing by a value that may be zero
 * Flow Variant: 68 Data flow: data passed as a member variable in the "a" class, which is used by a method in another class in the same package
 *
 * */

package testcases.CWE369_Divide_by_Zero.s04;
import testcasesupport.*;

import javax.servlet.http.*;

public class CWE369_Divide_by_Zero__int_zero_divide_68a extends AbstractTestCase
{
    public static int data;

    public void bad() throws Throwable
    {

        data = 0; /* POTENTIAL FLAW: data is set to zero */

        CWE369_Divide_by_Zero__int_zero_divide_68b_badSink();
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {

        /* FIX: Use a hardcoded number that won't cause underflow, overflow, divide by zero, or loss-of-precision issues */
        data = 2;

        CWE369_Divide_by_Zero__int_zero_divide_68b_goodG2BSink();
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {

        data = 0; /* POTENTIAL FLAW: data is set to zero */

        CWE369_Divide_by_Zero__int_zero_divide_68b_goodB2GSink();
    }

    /* Below is the main(). It is only used when building this testcase on
     * its own for testing or for building a binary to use in testing binary
     * analysis tools. It is not used when compiling all the testcases as one
     * application, which is how source code analysis tools are tested.
     */
    public static void main(String[] args) throws ClassNotFoundException,
           InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
    public void CWE369_Divide_by_Zero__int_zero_divide_68b_badSink() throws Throwable
    {
        int data = CWE369_Divide_by_Zero__int_zero_divide_68a.data;
        /* POTENTIAL FLAW: Zero denominator will cause an issue.  An integer division will
        result in an exception. */
        IO.writeLine("bad: 100/" + data + " = " + (100 / data) + "\n");
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__int_zero_divide_68b_goodG2BSink() throws Throwable
    {
        int data = CWE369_Divide_by_Zero__int_zero_divide_68a.data;
        /* POTENTIAL FLAW: Zero denominator will cause an issue.  An integer division will
        result in an exception. */
        IO.writeLine("bad: 100/" + data + " = " + (100 / data) + "\n");
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__int_zero_divide_68b_goodB2GSink() throws Throwable
    {
        int data = CWE369_Divide_by_Zero__int_zero_divide_68a.data;
        /* FIX: test for a zero denominator */
        if (data != 0)
        {
            IO.writeLine("100/" + data + " = " + (100 / data) + "\n");
        }
        else
        {
            IO.writeLine("This would result in a divide by zero");
        }
    }
}