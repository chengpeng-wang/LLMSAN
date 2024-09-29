/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE80_XSS__Servlet_getCookies_Servlet_53a.java
Label Definition File: CWE80_XSS__Servlet.label.xml
Template File: sources-sink-53a.tmpl.java
*/
/*
 * @description
 * CWE: 80 Cross Site Scripting (XSS)
 * BadSource: getCookies_Servlet Read data from the first cookie using getCookies()
 * GoodSource: A hardcoded string
 * Sinks:
 *    BadSink : Display of data in web page without any encoding or validation
 * Flow Variant: 53 Data flow: data passed as an argument from one method through two others to a fourth; all four functions are in different classes in the same package
 *
 * */

package testcases.CWE80_XSS.s01;
import testcasesupport.*;

import javax.servlet.http.*;


public class CWE80_XSS__Servlet_getCookies_Servlet_53a extends AbstractTestCaseServlet
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

        CWE80_XSS__Servlet_getCookies_Servlet_53b_badSink(data , request, response);
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

        CWE80_XSS__Servlet_getCookies_Servlet_53b_goodG2BSink(data , request, response);
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
    public void CWE80_XSS__Servlet_getCookies_Servlet_53b_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__Servlet_getCookies_Servlet_53c_badSink(data , request, response);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__Servlet_getCookies_Servlet_53b_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__Servlet_getCookies_Servlet_53c_goodG2BSink(data , request, response);
    }
    public void CWE80_XSS__Servlet_getCookies_Servlet_53c_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__Servlet_getCookies_Servlet_53d_badSink(data , request, response);
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__Servlet_getCookies_Servlet_53c_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        CWE80_XSS__Servlet_getCookies_Servlet_53d_goodG2BSink(data , request, response);
    }
    public void CWE80_XSS__Servlet_getCookies_Servlet_53d_badSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        if (data != null)
        {
            /* POTENTIAL FLAW: Display of data in web page without any encoding or validation */
            response.getWriter().println("<br>bad(): data = " + data);
        }
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE80_XSS__Servlet_getCookies_Servlet_53d_goodG2BSink(String data , HttpServletRequest request, HttpServletResponse response) throws Throwable
    {
        if (data != null)
        {
            /* POTENTIAL FLAW: Display of data in web page without any encoding or validation */
            response.getWriter().println("<br>bad(): data = " + data);
        }
    }
}