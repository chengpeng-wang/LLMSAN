/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__Integer_42.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-42.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 42 Data flow: data returned from one method to another in the same class
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;

public class CWE476_NULL_Pointer_Dereference__Integer_42 extends AbstractTestCase
{
    private Integer badSource() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        return data;
    }

    public void bad() throws Throwable
    {
        Integer data = badSource();

        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());

    }

    /* goodG2B() - use goodsource and badsink */
    private Integer goodG2BSource() throws Throwable
    {
        Integer data;

        /* FIX: hardcode data to non-null */
        data = Integer.valueOf(5);

        return data;
    }

    private void goodG2B() throws Throwable
    {
        Integer data = goodG2BSource();

        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());

    }

    /* goodB2G() - use badsource and goodsink */
    private Integer goodB2GSource() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        return data;
    }

    private void goodB2G() throws Throwable
    {
        Integer data = goodB2GSource();

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

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
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
}
