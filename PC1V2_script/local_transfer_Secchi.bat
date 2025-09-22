
@ECHO OFF
:: This command prevents the commands themselves from being displayed in the command prompt.
:: This makes the output cleaner.

:: English comments are preceded by "REM" or "::"

REM ====================================================================
REM                  SCRIPT TO MOVE FILES
REM ====================================================================

REM --------------------------------------------------------------------
REM                      *** CONFIGURATION ***
REM Set the variables for the source and destination folders.
REM IMPORTANT: Do not add a backslash (\) at the end of the folder paths.
REM --------------------------------------------------------------------

SET "SourceSecchi=C:\Users\Seatronic\Documents\Data_Lexplore\PC1V2_shared_folder\Data\Secchi"
SET "DestinationSecchi=C:\Users\Seatronic\Documents\Data_Lexplore\Secchi\Data"

REM --------------------------------------------------------------------
REM                         *** EXECUTION ***
REM The following command moves all files (*.*) from the source folder
REM to the destination folder.
REM --------------------------------------------------------------------

ECHO Moving files from "%SourceSecchi%" to "%DestinationSecchi%"...

MOVE "%SourceSecchi%\*.csv" "%DestinationSecchi%"
MOVE "%SourceSecchi%\*.txt" "%DestinationSecchi%"

ECHO.
ECHO Operation completed.
ECHO.

REM --------------------------------------------------------------------
REM                            *** END ***
REM The PAUSE command keeps the window open until you press a key.
REM This allows you to see the result of the operation.
REM --------------------------------------------------------------------


rem PAUSE
