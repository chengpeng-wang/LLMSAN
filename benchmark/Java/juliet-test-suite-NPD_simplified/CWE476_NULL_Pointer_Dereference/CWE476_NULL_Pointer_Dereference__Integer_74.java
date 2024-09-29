/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__Integer_74a.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-74a.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 74 Data flow: data passed in a HashMap from one method to another in different source files in the same package
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;
import java.util.HashMap;

public class CWE476_NULL_Pointer_Dereference__Integer_74a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        HashMap<Integer,Integer> dataHashMap = new HashMap<Integer,Integer>();
        dataHashMap.put(0, data);
        dataHashMap.put(1, data);
        dataHashMap.put(2, data);
        CWE476_NULL_Pointer_Dereference__Integer_74b_badSink(dataHashMap  );
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

        HashMap<Integer,Integer> dataHashMap = new HashMap<Integer,Integer>();
        dataHashMap.put(0, data);
        dataHashMap.put(1, data);
        dataHashMap.put(2, data);
        CWE476_NULL_Pointer_Dereference__Integer_74b_goodG2BSink(dataHashMap  );
    }

    /* goodB2G() - use BadSource and GoodSink */
    private void goodB2G() throws Throwable
    {
        Integer data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        HashMap<Integer,Integer> dataHashMap = new HashMap<Integer,Integer>();
        dataHashMap.put(0, data);
        dataHashMap.put(1, data);
        dataHashMap.put(2, data);
        CWE476_NULL_Pointer_Dereference__Integer_74b_goodB2GSink(dataHashMap  );
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
    public void CWE476_NULL_Pointer_Dereference__Integer_74b_badSink(HashMap<Integer,Integer> dataHashMap ) throws Throwable
    {
        Integer data = dataHashMap.get(2);
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());
    }
    /* goodG2B() - use GoodSource and BadSink */
    public void CWE476_NULL_Pointer_Dereference__Integer_74b_goodG2BSink(HashMap<Integer,Integer> dataHashMap ) throws Throwable
    {
        Integer data = dataHashMap.get(2);
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.toString());
    }
    /* goodB2G() - use BadSource and GoodSink */
    public void CWE476_NULL_Pointer_Dereference__Integer_74b_goodB2GSink(HashMap<Integer,Integer> dataHashMap ) throws Throwable
    {
        Integer data = dataHashMap.get(2);
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