### How to build for Windows 10

Since you are currently on macOS, you cannot directly generate a Windows `.exe` file.
However, I have prepared everything you need to build it easily on a Windows machine.

1.  **Copy this entire project folder** to a Windows 10/11 computer.
2.  Ensure **Python 3.9** or newer is installed on that Windows machine.
3.  Double-click the `build_windows.bat` file.

The script will automatically:
*   Create a virtual environment.
*   Install all necessary libraries (PyQt5, Spleeter, etc.).
*   Compile the application into a standalone `.exe`.

The final application will appear in the `dist` folder.
