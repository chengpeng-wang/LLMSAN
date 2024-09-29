/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54a.java
Label Definition File: CWE80_XSS__CWE182_Servlet.label.xml
Template File: sources-sink-54a.tmpl.java
*/
/*
 * @description
 * CWE: 80 Cross Site Scripting (XSS)
 * BadSource: getCookies_Servlet Read data from the first cookie using getCookies()
 * GoodSource: A hardcoded string
 * Sinks:
 *    BadSink : Display of data in web page after using replaceAll() to remove script tags, which will still allow XSS (CWE 182: Collapse of Data into Unsafe Value)
 * Flow Variant: 54 Data flow: data passed as an argument from one method through three others to a fifth; all five functions are in different classes in the same package
 *
 * */

package testcases.CWE80_XSS.s01;
import testcasesupport.*;

import javax.servlet.http.*;


public class CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54a extends AbstractTestCaseServlet
{
    public void bad(HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        String data;

        data = ""; /* initialize data in case there are no cookies */

        /* Read data from cookies */
        {
            Cookie cookieSources[] = request.getCookies();
            if (cookieSources != null)
            {
                /* POTENTIAL FLAW: Read data from the first cookie value */
                data = cookieSources[0].getValue();
            }
        }

        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54b_badSink(data , request, response);
    }

    public void good(HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        goodG2B(request, response);
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B(HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        String data;

        /* FIX: Use a hardcoded string */
        data = "foo";

        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54b_goodG2BSink(data , request, response);
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
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54c_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54d_badSink(data , request, response);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54c_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54d_goodG2BSink(data , request, response);
    }
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54b_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54c_badSink(data , request, response);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54b_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54c_goodG2BSink(data , request, response);
    }
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54e_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        if (data != null)
        {
            /* POTENTIAL FLAW: Display of data in web page after using replaceAll() to remove script tags, which will still allow XSS with strings like <scr<script>ipt> (CWE 182: Collapse of Data into Unsafe Value) */
            response.getWriter().println("<br>bad(): data = " + data.replaceAll("(<script>)", ""));
        }
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54e_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        if (data != null)
        {
            /* POTENTIAL FLAW: Display of data in web page after using replaceAll() to remove script tags, which will still allow XSS with strings like <scr<script>ipt> (CWE 182: Collapse of Data into Unsafe Value) */
            response.getWriter().println("<br>bad(): data = " + data.replaceAll("(<script>)", ""));
        }
    }
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54d_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54e_badSink(data , request, response);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54d_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__CWE182_Servlet_getCookies_Servlet_54e_goodG2BSink(data , request, response);
    }
}