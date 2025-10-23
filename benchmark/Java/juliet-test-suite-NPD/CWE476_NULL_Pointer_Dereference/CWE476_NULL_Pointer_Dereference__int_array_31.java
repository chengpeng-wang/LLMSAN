/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__int_array_31.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-31.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 31 Data flow: make a copy of data within the same method
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;

public class CWE476_NULL_Pointer_Dereference__int_array_31 extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        int [] dataCopy;
        {
            int [] data;

            /* POTENTIAL FLAW: data is null */
            data = null;

            dataCopy = data;
        }
        {
            int [] data = dataCopy;

            /* POTENTIAL FLAW: null dereference will occur if data is null */
            IO.writeLine("" + data.length);

        }
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {
        int [] dataCopy;
        {
            int [] data;

            /* FIX: hardcode data to non-null */
            data = new int[5];

            dataCopy = data;
        }
        {
            int [] data = dataCopy;

            /* POTENTIAL FLAW: null dereference will occur if data is null */
            IO.writeLine("" + data.length);

        }
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {
        int [] dataCopy;
        {
            int [] data;

            /* POTENTIAL FLAW: data is null */
            data = null;

            dataCopy = data;
        }
        {
            int [] data = dataCopy;

            /* FIX: validate that data is non-null */
            if (data != null)
            {
                IO.writeLine("" + data.length);
            }
            else
            {
                IO.writeLine("data is null");
            }

        }
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
