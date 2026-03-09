name: Hedgehog Sentinel EXE Generator

on: [push]

jobs:
  build_windows:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller

    - name: Create EXE (The Hedgehog Core)
      run: |
        pyinstaller --onefile --windowed --name "Hedgehog_Sentinel" main.py

    - name: Deliver EXE
      uses: actions/upload-artifact@v4
      with:
        name: Hedgehog-Sentinel-Windows
        path: dist/Hedgehog_Sentinel.exe
