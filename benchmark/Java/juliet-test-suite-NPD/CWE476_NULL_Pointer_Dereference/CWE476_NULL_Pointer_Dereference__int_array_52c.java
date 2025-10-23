/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__int_array_52c.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-52c.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 52 Data flow: data passed as an argument from one method to another to another in three different classes in the same package
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;

public class CWE476_NULL_Pointer_Dereference__int_array_52c
{
    public void badSink(int [] data ) throws Throwable
    {

        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.length);

    }

    /* goodG2B() - use goodsource and badsink */
    public void goodG2BSink(int [] data ) throws Throwable
    {

        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.length);

    }

    /* goodB2G() - use badsource and goodsink */
    public void goodB2GSink(int [] data ) throws Throwable
    {

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
