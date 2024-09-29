/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE369_Divide_by_Zero__int_zero_divide_72a.java
Label Definition File: CWE369_Divide_by_Zero__int.label.xml
Template File: sources-sinks-72a.tmpl.java
*/
/*
 * @description
 * CWE: 369 Divide by zero
 * BadSource: zero Set data to a hardcoded value of zero
 * GoodSource: A hardcoded non-zero, non-min, non-max, even number
 * Sinks: divide
 *    GoodSink: Check for zero before dividing
 *    BadSink : Dividing by a value that may be zero
 * Flow Variant: 72 Data flow: data passed in a Vector from one method to another in different source files in the same package
 *
 * */

package testcases.CWE369_Divide_by_Zero.s04;
import testcasesupport.*;
import java.util.Vector;

import javax.servlet.http.*;

public class CWE369_Divide_by_Zero__int_zero_divide_72a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        int data;

        data = 0; /* POTENTIAL FLAW: data is set to zero */

        Vector<Integer> dataVector = new Vector<Integer>(5);
        dataVector.add(0, data);
        dataVector.add(1, data);
        dataVector.add(2, data);
        CWE369_Divide_by_Zero__int_zero_divide_72b_badSink(dataVector  );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use GoodSource and BadSink */
    private void goodG2B() throws Throwable
    {
        int data;

        /* FIX: Use a hardcoded number that won't cause underflow, overflow, divide by zero, or loss-of-precision issues */
        data = 2;

        Vector<Integer> dataVector = new Vector<Integer>(5);
        dataVector.add(0, data);
        dataVector.add(1, data);
        dataVector.add(2, data);
        CWE369_Divide_by_Zero__int_zero_divide_72b_goodG2BSink(dataVector  );
    }

    /* goodB2G() - use BadSource and GoodSink */
    private void goodB2G() throws Throwable
    {
        int data;

        data = 0; /* POTENTIAL FLAW: data is set to zero */

        Vector<Integer> dataVector = new Vector<Integer>(5);
        dataVector.add(0, data);
        dataVector.add(1, data);
        dataVector.add(2, data);
        CWE369_Divide_by_Zero__int_zero_divide_72b_goodB2GSink(dataVector  );
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

    public void CWE369_Divide_by_Zero__int_zero_divide_72b_badSink(Vector<Integer> dataVector ) throws Throwable
    {
        int data = dataVector.remove(2);
        /* POTENTIAL FLAW: Zero denominator will cause an issue.  An integer division will
        result in an exception. */
        IO.writeLine("bad: 100/" + data + " = " + (100 / data) + "\n");
    }
    /* goodG2B() - use GoodSource and BadSink */
    public void CWE369_Divide_by_Zero__int_zero_divide_72b_goodG2BSink(Vector<Integer> dataVector ) throws Throwable
    {
        int data = dataVector.remove(2);
        /* POTENTIAL FLAW: Zero denominator will cause an issue.  An integer division will
        result in an exception. */
        IO.writeLine("bad: 100/" + data + " = " + (100 / data) + "\n");
    }
    /* goodB2G() - use BadSource and GoodSink */
    public void CWE369_Divide_by_Zero__int_zero_divide_72b_goodB2GSink(Vector<Integer> dataVector ) throws Throwable
    {
        int data = dataVector.remove(2);
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