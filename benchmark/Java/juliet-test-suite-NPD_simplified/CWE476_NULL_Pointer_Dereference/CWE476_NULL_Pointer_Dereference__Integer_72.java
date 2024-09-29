/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__Integer_72a.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-72a.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 72 Data flow: data passed in a Vector from one method to another in different source files in the same package
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;
import java.util.Vector;

public class CWE476_NULL_Pointer_Dereference__Integer_72a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        Vector<Integer> dataVector = new Vector<Integer>(5);
        dataVector.add(0, data);
        dataVector.add(1, data);
        dataVector.add(2, data);
        CWE476_NULL_Pointer_Dereference__Integer_72b_badSink(dataVector  );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use GoodSource and BadSink */
    private void goodG2B() throws Throwable
    {
        Integer data;

        /* FIX: hardcode data to non-null */
        data = Integer.valueOf(5);

        Vector<Integer> dataVector = new Vector<Integer>(5);
        dataVector.add(0, data);
        dataVector.add(1, data);
        dataVector.add(2, data);
        CWE476_NULL_Pointer_Dereference__Integer_72b_goodG2BSink(dataVector  );
    }

    /* goodB2G() - use BadSource and GoodSink */
    private void goodB2G() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        Vector<Integer> dataVector = new Vector<Integer>(5);
        dataVector.add(0, data);
        dataVector.add(1, data);
        dataVector.add(2, data);
        CWE476_NULL_Pointer_Dereference__Integer_72b_goodB2GSink(dataVector  );
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

    public void CWE476_NULL_Pointer_Dereference__Integer_72b_badSink(Vector<Integer> dataVector ) throws Throwable
    {
        Integer data = dataVector.remove(2);
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());
    }
    /* goodG2B() - use GoodSource and BadSink */
    public void CWE476_NULL_Pointer_Dereference__Integer_72b_goodG2BSink(Vector<Integer> dataVector ) throws Throwable
    {
        Integer data = dataVector.remove(2);
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());
    }
    /* goodB2G() - use BadSource and GoodSink */
    public void CWE476_NULL_Pointer_Dereference__Integer_72b_goodB2GSink(Vector<Integer> dataVector ) throws Throwable
    {
        Integer data = dataVector.remove(2);
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