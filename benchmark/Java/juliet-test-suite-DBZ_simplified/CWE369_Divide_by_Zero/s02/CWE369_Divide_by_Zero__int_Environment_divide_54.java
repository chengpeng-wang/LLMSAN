/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE369_Divide_by_Zero__int_Environment_divide_54a.java
Label Definition File: CWE369_Divide_by_Zero__int.label.xml
Template File: sources-sinks-54a.tmpl.java
*/
/*
 * @description
 * CWE: 369 Divide by zero
 * BadSource: Environment Read data from an environment variable
 * GoodSource: A hardcoded non-zero, non-min, non-max, even number
 * Sinks: divide
 *    GoodSink: Check for zero before dividing
 *    BadSink : Dividing by a value that may be zero
 * Flow Variant: 54 Data flow: data passed as an argument from one method through three others to a fifth; all five functions are in different classes in the same package
 *
 * */

package testcases.CWE369_Divide_by_Zero.s02;
import testcasesupport.*;

import javax.servlet.http.*;

import java.util.logging.Level;

public class CWE369_Divide_by_Zero__int_Environment_divide_54a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        int data;

        data = Integer.MIN_VALUE; /* Initialize data */

        /* get environment variable ADD */
        /* POTENTIAL FLAW: Read data from an environment variable */
        {
            String stringNumber = System.getenv("ADD");
            if (stringNumber != null) // avoid NPD incidental warnings
            {
                try
                {
                    data = Integer.parseInt(stringNumber.trim());
                }
                catch(NumberFormatException exceptNumberFormat)
                {
                    IO.logger.log(Level.WARNING, "Number format exception parsing data from string", exceptNumberFormat);
                }
            }
        }

        CWE369_Divide_by_Zero__int_Environment_divide_54b_badSink(data );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {
        int data;

        /* FIX: Use a hardcoded number that won't cause underflow, overflow, divide by zero, or loss-of-precision issues */
        data = 2;

        CWE369_Divide_by_Zero__int_Environment_divide_54b_goodG2BSink(data );
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {
        int data;

        data = Integer.MIN_VALUE; /* Initialize data */

        /* get environment variable ADD */
        /* POTENTIAL FLAW: Read data from an environment variable */
        {
            String stringNumber = System.getenv("ADD");
            if (stringNumber != null) // avoid NPD incidental warnings
            {
                try
                {
                    data = Integer.parseInt(stringNumber.trim());
                }
                catch(NumberFormatException exceptNumberFormat)
                {
                    IO.logger.log(Level.WARNING, "Number format exception parsing data from string", exceptNumberFormat);
                }
            }
        }

        CWE369_Divide_by_Zero__int_Environment_divide_54b_goodB2GSink(data );
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
    public void CWE369_Divide_by_Zero__int_Environment_divide_54c_badSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54d_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54c_goodG2BSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54d_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54c_goodB2GSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54d_goodB2GSink(data );
    }
    public void CWE369_Divide_by_Zero__int_Environment_divide_54b_badSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54c_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54b_goodG2BSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54c_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54b_goodB2GSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54c_goodB2GSink(data );
    }
    public void CWE369_Divide_by_Zero__int_Environment_divide_54e_badSink(int data ) throws Throwable
    {
        /* POTENTIAL FLAW: Zero denominator will cause an issue.  An integer division will
        result in an exception. */
        IO.writeLine("bad: 100/" + data + " = " + (100 / data) + "\n");
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54e_goodG2BSink(int data ) throws Throwable
    {
        /* POTENTIAL FLAW: Zero denominator will cause an issue.  An integer division will
        result in an exception. */
        IO.writeLine("bad: 100/" + data + " = " + (100 / data) + "\n");
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54e_goodB2GSink(int data ) throws Throwable
    {
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
    public void CWE369_Divide_by_Zero__int_Environment_divide_54d_badSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54e_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54d_goodG2BSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54e_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__int_Environment_divide_54d_goodB2GSink(int data ) throws Throwable
    {
        CWE369_Divide_by_Zero__int_Environment_divide_54e_goodB2GSink(data );
    }
}