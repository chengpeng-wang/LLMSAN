/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__Integer_53a.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-53a.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 53 Data flow: data passed as an argument from one method through two others to a fourth; all four functions are in different classes in the same package
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;

public class CWE476_NULL_Pointer_Dereference__Integer_53a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        CWE476_NULL_Pointer_Dereference__Integer_53b_badSink(data );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {
        Integer data;

        /* FIX: hardcode data to non-null */
        data = Integer.valueOf(5);

        CWE476_NULL_Pointer_Dereference__Integer_53b_goodG2BSink(data );
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        CWE476_NULL_Pointer_Dereference__Integer_53b_goodB2GSink(data );
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

    public void CWE476_NULL_Pointer_Dereference__Integer_53c_badSink(Integer data ) throws Throwable
    {
        CWE476_NULL_Pointer_Dereference__Integer_53d_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE476_NULL_Pointer_Dereference__Integer_53c_goodG2BSink(Integer data ) throws Throwable
    {
        CWE476_NULL_Pointer_Dereference__Integer_53d_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE476_NULL_Pointer_Dereference__Integer_53c_goodB2GSink(Integer data ) throws Throwable
    {
        CWE476_NULL_Pointer_Dereference__Integer_53d_goodB2GSink(data );
    }
    public void CWE476_NULL_Pointer_Dereference__Integer_53b_badSink(Integer data ) throws Throwable
    {
        CWE476_NULL_Pointer_Dereference__Integer_53c_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE476_NULL_Pointer_Dereference__Integer_53b_goodG2BSink(Integer data ) throws Throwable
    {
        CWE476_NULL_Pointer_Dereference__Integer_53c_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE476_NULL_Pointer_Dereference__Integer_53b_goodB2GSink(Integer data ) throws Throwable
    {
        CWE476_NULL_Pointer_Dereference__Integer_53c_goodB2GSink(data );
    }
    public void CWE476_NULL_Pointer_Dereference__Integer_53d_badSink(Integer data ) throws Throwable
    {
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE476_NULL_Pointer_Dereference__Integer_53d_goodG2BSink(Integer data ) throws Throwable
    {
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE476_NULL_Pointer_Dereference__Integer_53d_goodB2GSink(Integer data ) throws Throwable
    {
        /* FIX: validate that data is non-null */
        if (data != null)
        {
            IO.writeLine("" + data.toString());
        }
        else
        {
            IO.writeLine("data is null");
        }
    }
}