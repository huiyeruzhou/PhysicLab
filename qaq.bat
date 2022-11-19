for %%i in (.\UI\*.ui) do (
"C:\Users\huiyeruzhou\AppData\Local\Programs\Python\Python37\Scripts\pyuic5.exe" %%i -o .\UI\%%~niUI.py)