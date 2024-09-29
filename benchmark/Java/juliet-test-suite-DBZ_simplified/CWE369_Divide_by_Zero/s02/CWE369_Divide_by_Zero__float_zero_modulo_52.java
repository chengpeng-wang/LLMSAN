/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE369_Divide_by_Zero__float_zero_modulo_52a.java
Label Definition File: CWE369_Divide_by_Zero__float.label.xml
Template File: sources-sinks-52a.tmpl.java
*/
/*
 * @description
 * CWE: 369 Divide by zero
 * BadSource: zero Set data to a hardcoded value of zero
 * GoodSource: A hardcoded non-zero number (two)
 * Sinks: modulo
 *    GoodSink: Check for zero before modulo
 *    BadSink : Modulo by a value that may be zero
 * Flow Variant: 52 Data flow: data passed as an argument from one method to another to another in three different classes in the same package
 *
 * */

package testcases.CWE369_Divide_by_Zero.s02;
import testcasesupport.*;

public class CWE369_Divide_by_Zero__float_zero_modulo_52a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        float data;

        data = 0.0f; /* POTENTIAL FLAW: data is set to zero */

        CWE369_Divide_by_Zero__float_zero_modulo_52b_badSink(data );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {
        float data;

        /* FIX: Use a hardcoded number that won't a divide by zero */
        data = 2.0f;

        CWE369_Divide_by_Zero__float_zero_modulo_52b_goodG2BSink(data );
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {
        float data;

        data = 0.0f; /* POTENTIAL FLAW: data is set to zero */

        CWE369_Divide_by_Zero__float_zero_modulo_52b_goodB2GSink(data );
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
    public void CWE369_Divide_by_Zero__float_zero_modulo_52b_badSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_zero_modulo_52c_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__float_zero_modulo_52b_goodG2BSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_zero_modulo_52c_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__float_zero_modulo_52b_goodB2GSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_zero_modulo_52c_goodB2GSink(data );
    }
    public void CWE369_Divide_by_Zero__float_zero_modulo_52c_badSink(float data ) throws Throwable
    {
        /* POTENTIAL FLAW: Possibly modulo by zero */
        int result = (int)(100.0 % data);
        IO.writeLine(result);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__float_zero_modulo_52c_goodG2BSink(float data ) throws Throwable
    {
        /* POTENTIAL FLAW: Possibly modulo by zero */
        int result = (int)(100.0 % data);
        IO.writeLine(result);
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__float_zero_modulo_52c_goodB2GSink(float data ) throws Throwable
    {
        /* FIX: Check for value of or near zero before modulo */
        if (Math.abs(data) > 0.000001)
        {
            int result = (int)(100.0 % data);
            IO.writeLine(result);
        }
        else
        {
            IO.writeLine("This would result in a modulo by zero");
        }
    }
}