for %%i in (.\app\UI\*.ui) do (
"C:\Users\huiyeruzhou\AppData\Local\Programs\Python\Python37\Scripts\pyuic5.exe" %%i -o .\app\View\%%~niUI.py)