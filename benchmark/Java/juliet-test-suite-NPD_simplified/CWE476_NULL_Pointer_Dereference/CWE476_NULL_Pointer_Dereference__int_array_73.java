/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE476_NULL_Pointer_Dereference__int_array_73a.java
Label Definition File: CWE476_NULL_Pointer_Dereference.label.xml
Template File: sources-sinks-73a.tmpl.java
*/
/*
 * @description
 * CWE: 476 Null Pointer Dereference
 * BadSource:  Set data to null
 * GoodSource: Set data to a non-null value
 * Sinks:
 *    GoodSink: add check to prevent possibility of null dereference
 *    BadSink : possibility of null dereference
 * Flow Variant: 73 Data flow: data passed in a LinkedList from one method to another in different source files in the same package
 *
 * */

package testcases.CWE476_NULL_Pointer_Dereference;

import testcasesupport.*;
import java.util.LinkedList;

public class CWE476_NULL_Pointer_Dereference__int_array_73a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        int [] data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        LinkedList<int []> dataLinkedList = new LinkedList<int []>();
        dataLinkedList.add(0, data);
        dataLinkedList.add(1, data);
        dataLinkedList.add(2, data);
        CWE476_NULL_Pointer_Dereference__int_array_73b_badSink(dataLinkedList  );
    }

    public void good() throws Throwable
    {
        goodG2B();
        goodB2G();
    }

    /* goodG2B() - use GoodSource and BadSink */
    private void goodG2B() throws Throwable
    {
        int [] data;

        /* FIX: hardcode data to non-null */
        data = new int[5];

        LinkedList<int []> dataLinkedList = new LinkedList<int []>();
        dataLinkedList.add(0, data);
        dataLinkedList.add(1, data);
        dataLinkedList.add(2, data);
        CWE476_NULL_Pointer_Dereference__int_array_73b_goodG2BSink(dataLinkedList  );
    }

    /* goodB2G() - use BadSource and GoodSink */
    private void goodB2G() throws Throwable
    {
        int [] data;

        /* POTENTIAL FLAW: data is null */
        data = null;

        LinkedList<int []> dataLinkedList = new LinkedList<int []>();
        dataLinkedList.add(0, data);
        dataLinkedList.add(1, data);
        dataLinkedList.add(2, data);
        CWE476_NULL_Pointer_Dereference__int_array_73b_goodB2GSink(dataLinkedList  );
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

    public void CWE476_NULL_Pointer_Dereference__int_array_73b_badSink(LinkedList<int []> dataLinkedList ) throws Throwable
    {
        int [] data = dataLinkedList.remove(2);
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.length);
    }
    /* goodG2B() - use GoodSource and BadSink */
    public void CWE476_NULL_Pointer_Dereference__int_array_73b_goodG2BSink(LinkedList<int []> dataLinkedList ) throws Throwable
    {
        int [] data = dataLinkedList.remove(2);
        /* POTENTIAL FLAW: null dereference will occur if data is null */
        IO.writeLine("" + data.length);
    }
    /* goodB2G() - use BadSource and GoodSink */
    public void CWE476_NULL_Pointer_Dereference__int_array_73b_goodB2GSink(LinkedList<int []> dataLinkedList ) throws Throwable
    {
        int [] data = dataLinkedList.remove(2);
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