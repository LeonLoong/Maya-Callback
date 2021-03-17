@echo off
A:
cd A:\Demo\Global\Other\xmlStarlet-1.6.1\

set USERINFO=%USERPROFILE%\Demo\Datas\Demo\User_Info.xml;

:Query_Project_Name
set "Project="
for /F "delims=" %%f in ('xml sel -t -v /DATA/USERS/USER/Project %USERINFO%') do (
	set "Project=%%f"
	goto Query_Software_Version
)

:Query_Software_Version
set "Version="
for /F "delims=" %%f in ('xml sel -t -v /DATA/USERS/USER/Software %USERINFO%') do (
	set "Version=%%f"
	goto Query_Department_Code
)

:Query_Department_Code
set "Department="
for /F "delims=" %%f in ('xml sel -t -v /DATA/USERS/USER/Department %USERINFO%') do (
	set "Department=%%f"
	goto Setup
)

:Setup
set PIXELLINEPROJECTCODE=%Project%;
set PYTHONPATH=A:\Demo\Project\%Project%\Maya\scripts\;
set MAYA_SHELF_PATH=A:\Demo\Project\%Project%\Maya\shelves\%Department%;
"C:\Program Files\Autodesk\Maya%Version%\bin\maya.exe" %*
