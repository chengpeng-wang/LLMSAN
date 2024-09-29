/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE369_Divide_by_Zero__float_Environment_divide_53a.java
Label Definition File: CWE369_Divide_by_Zero__float.label.xml
Template File: sources-sinks-53a.tmpl.java
*/
/*
 * @description
 * CWE: 369 Divide by zero
 * BadSource: Environment Read data from an environment variable
 * GoodSource: A hardcoded non-zero number (two)
 * Sinks: divide
 *    GoodSink: Check for zero before dividing
 *    BadSink : Dividing by a value that may be zero
 * Flow Variant: 53 Data flow: data passed as an argument from one method through two others to a fourth; all four functions are in different classes in the same package
 *
 * */

package testcases.CWE369_Divide_by_Zero.s01;
import testcasesupport.*;

import java.util.logging.Level;

public class CWE369_Divide_by_Zero__float_Environment_divide_53a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        float data;

        data = -1.0f; /* Initialize data */

        /* get environment variable ADD */
        /* POTENTIAL FLAW: Read data from an environment variable */
        {
            String stringNumber = System.getenv("ADD");
            if (stringNumber != null)
            {
                try
                {
                    data = Float.parseFloat(stringNumber.trim());
                }
                catch (NumberFormatException exceptNumberFormat)
                {
                    IO.logger.log(Level.WARNING, "Number format exception parsing data from string", exceptNumberFormat);
                }
            }
        }

        CWE369_Divide_by_Zero__float_Environment_divide_53b_badSink(data );
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

        CWE369_Divide_by_Zero__float_Environment_divide_53b_goodG2BSink(data );
    }

    /* goodB2G() - use badsource and goodsink */
    private void goodB2G() throws Throwable
    {
        float data;

        data = -1.0f; /* Initialize data */

        /* get environment variable ADD */
        /* POTENTIAL FLAW: Read data from an environment variable */
        {
            String stringNumber = System.getenv("ADD");
            if (stringNumber != null)
            {
                try
                {
                    data = Float.parseFloat(stringNumber.trim());
                }
                catch (NumberFormatException exceptNumberFormat)
                {
                    IO.logger.log(Level.WARNING, "Number format exception parsing data from string", exceptNumberFormat);
                }
            }
        }

        CWE369_Divide_by_Zero__float_Environment_divide_53b_goodB2GSink(data );
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

    public void CWE369_Divide_by_Zero__float_Environment_divide_53d_badSink(float data ) throws Throwable
    {
        /* POTENTIAL FLAW: Possibly divide by zero */
        int result = (int)(100.0 / data);
        IO.writeLine(result);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__float_Environment_divide_53d_goodG2BSink(float data ) throws Throwable
    {
        /* POTENTIAL FLAW: Possibly divide by zero */
        int result = (int)(100.0 / data);
        IO.writeLine(result);
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__float_Environment_divide_53d_goodB2GSink(float data ) throws Throwable
    {
        /* FIX: Check for value of or near zero before dividing */
        if (Math.abs(data) > 0.000001)
        {
            int result = (int)(100.0 / data);
            IO.writeLine(result);
        }
        else
        {
            IO.writeLine("This would result in a divide by zero");
        }
    }
    public void CWE369_Divide_by_Zero__float_Environment_divide_53b_badSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_Environment_divide_53c_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__float_Environment_divide_53b_goodG2BSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_Environment_divide_53c_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__float_Environment_divide_53b_goodB2GSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_Environment_divide_53c_goodB2GSink(data );
    }
    public void CWE369_Divide_by_Zero__float_Environment_divide_53c_badSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_Environment_divide_53d_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE369_Divide_by_Zero__float_Environment_divide_53c_goodG2BSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_Environment_divide_53d_goodG2BSink(data );
    }
    /* goodB2G() - use badsource and goodsink */
    public void CWE369_Divide_by_Zero__float_Environment_divide_53c_goodB2GSink(float data ) throws Throwable
    {
        CWE369_Divide_by_Zero__float_Environment_divide_53d_goodB2GSink(data );
    }
}