name: Daily Heat Index Push

on:
  workflow_dispatch:  # 手動觸發
  schedule:
    - cron: '0 1,3,5,7 * * *'  # 台灣時間 9:00、11:00、13:00、15:00 執行（UTC+8）

jobs:
  push:
    runs-on: ubuntu-latest

    steps:
    - name: 下載程式碼
      uses: actions/checkout@v3

    - name: 安裝 Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: 安裝套件
      run: |
        pip install line-bot-sdk

    - name: Run LINE text message test
      env:
        CHANNEL_SECRET: ${{ secrets.CHANNEL_SECRET }}
        CHANNEL_ACCESS_TOKEN: ${{ secrets.CHANNEL_ACCESS_TOKEN }}
        GROUP_ID: ${{ secrets.GROUP_ID }}
      run: python main_text.py
