/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE78_OS_Command_Injection__connect_tcp_54a.java
Label Definition File: CWE78_OS_Command_Injection.label.xml
Template File: sources-sink-54a.tmpl.java
*/
/*
 * @description
 * CWE: 78 OS Command Injection
 * BadSource: connect_tcp Read data using an outbound tcp connection
 * GoodSource: A hardcoded string
 * Sinks: exec
 *    BadSink : dynamic command execution with Runtime.getRuntime().exec()
 * Flow Variant: 54 Data flow: data passed as an argument from one method through three others to a fifth; all five functions are in different classes in the same package
 *
 * */

package testcases.CWE78_OS_Command_Injection;

import testcasesupport.*;

import javax.servlet.http.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

import java.util.logging.Level;

public class CWE78_OS_Command_Injection__connect_tcp_54a extends AbstractTestCase
{
    public void bad() throws Throwable
    {
        String data;

        data = ""; /* Initialize data */

        /* Read data using an outbound tcp connection */
        {
            Socket socket = null;
            BufferedReader readerBuffered = null;
            InputStreamReader readerInputStream = null;

            try
            {
                /* Read data using an outbound tcp connection */
                socket = new Socket("host.example.org", 39544);

                /* read input from socket */

                readerInputStream = new InputStreamReader(socket.getInputStream(), "UTF-8");
                readerBuffered = new BufferedReader(readerInputStream);

                /* POTENTIAL FLAW: Read data using an outbound tcp connection */
                data = readerBuffered.readLine();
            }
            catch (IOException exceptIO)
            {
                IO.logger.log(Level.WARNING, "Error with stream reading", exceptIO);
            }
            finally
            {
                /* clean up stream reading objects */
                try
                {
                    if (readerBuffered != null)
                    {
                        readerBuffered.close();
                    }
                }
                catch (IOException exceptIO)
                {
                    IO.logger.log(Level.WARNING, "Error closing BufferedReader", exceptIO);
                }

                try
                {
                    if (readerInputStream != null)
                    {
                        readerInputStream.close();
                    }
                }
                catch (IOException exceptIO)
                {
                    IO.logger.log(Level.WARNING, "Error closing InputStreamReader", exceptIO);
                }

                /* clean up socket objects */
                try
                {
                    if (socket != null)
                    {
                        socket.close();
                    }
                }
                catch (IOException exceptIO)
                {
                    IO.logger.log(Level.WARNING, "Error closing Socket", exceptIO);
                }
            }
        }

        CWE78_OS_Command_Injection__connect_tcp_54b_badSink(data );
    }

    public void good() throws Throwable
    {
        goodG2B();
    }

    /* goodG2B() - use goodsource and badsink */
    private void goodG2B() throws Throwable
    {
        String data;

        /* FIX: Use a hardcoded string */
        data = "foo";

        CWE78_OS_Command_Injection__connect_tcp_54b_goodG2BSink(data );
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
    public void CWE78_OS_Command_Injection__connect_tcp_54c_badSink(String data ) throws Throwable
    {
        CWE78_OS_Command_Injection__connect_tcp_54d_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE78_OS_Command_Injection__connect_tcp_54c_goodG2BSink(String data ) throws Throwable
    {
        CWE78_OS_Command_Injection__connect_tcp_54d_goodG2BSink(data );
    }
    public void CWE78_OS_Command_Injection__connect_tcp_54b_badSink(String data ) throws Throwable
    {
        CWE78_OS_Command_Injection__connect_tcp_54c_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE78_OS_Command_Injection__connect_tcp_54b_goodG2BSink(String data ) throws Throwable
    {
        CWE78_OS_Command_Injection__connect_tcp_54c_goodG2BSink(data );
    }
    public void CWE78_OS_Command_Injection__connect_tcp_54e_badSink(String data ) throws Throwable
    {
        String osCommand;
        if(System.getProperty("os.name").toLowerCase().indexOf("win") >= 0)
        {
            /* running on Windows */
            osCommand = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        }
        else
        {
            /* running on non-Windows */
            osCommand = "/bin/ls ";
        }
        /* POTENTIAL FLAW: command injection */
        Process process = Runtime.getRuntime().exec(osCommand + data);
        process.waitFor();
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE78_OS_Command_Injection__connect_tcp_54e_goodG2BSink(String data ) throws Throwable
    {
        String osCommand;
        if(System.getProperty("os.name").toLowerCase().indexOf("win") >= 0)
        {
            /* running on Windows */
            osCommand = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        }
        else
        {
            /* running on non-Windows */
            osCommand = "/bin/ls ";
        }
        /* POTENTIAL FLAW: command injection */
        Process process = Runtime.getRuntime().exec(osCommand + data);
        process.waitFor();
    }
    public void CWE78_OS_Command_Injection__connect_tcp_54d_badSink(String data ) throws Throwable
    {
        CWE78_OS_Command_Injection__connect_tcp_54e_badSink(data );
    }
    /* goodG2B() - use goodsource and badsink */
    public void CWE78_OS_Command_Injection__connect_tcp_54d_goodG2BSink(String data ) throws Throwable
    {
        CWE78_OS_Command_Injection__connect_tcp_54e_goodG2BSink(data );
    }
}