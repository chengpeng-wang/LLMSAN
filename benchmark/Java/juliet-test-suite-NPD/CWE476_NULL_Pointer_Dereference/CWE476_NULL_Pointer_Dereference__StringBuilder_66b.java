/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__StringBuilder_66b.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-66b.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 66 Data flow: data passed in an array from one method to another in different source files in the same package
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;

public class CWE476_NULL_Pointer_Dereference__StringBuilder_66b
{
    public void badSink(StringBuilder dataArray[] ) throws Throwable
    {
        StringBuilder data = dataArray[2];

        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.length());

    }

    /* goodG2B() - use goodsource and badsink */
    public void goodG2BSink(StringBuilder dataArray[] ) throws Throwable
    {
        StringBuilder data = dataArray[2];

        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.length());

    }

    /* goodB2G() - use badsource and goodsink */
    public void goodB2GSink(StringBuilder dataArray[] ) throws Throwable
    {
        StringBuilder data = dataArray[2];

        /* FIX: validate that data is non-null */
        if (data != null)
        {
            IO.writeLine("" + data.length());
        }
        else
        {
            IO.writeLine("data is null");
        }

    }
}
